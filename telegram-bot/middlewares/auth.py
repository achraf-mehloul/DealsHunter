"""
Middleware المصادقة
التحقق من هوية المستخدمين والصلاحيات
"""

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from telegram_bot.database.models import User as DBUser, get_session

class AuthMiddleware(BaseMiddleware):
    """
    middleware للمصادقة وإدارة المستخدمين
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        معالجة كل حدث وارد
        """
        # الحصول على بيانات المستخدم من التحديث
        telegram_user: User = data.get("event_from_user")
        
        if not telegram_user:
            return await handler(event, data)
        
        try:
            # البحث عن المستخدم في قاعدة البيانات أو إنشائه
            async with next(get_session()) as session:
                db_user = await session.get(DBUser, telegram_user.id)
                
                if not db_user:
                    # إنشاء مستخدم جديد
                    db_user = DBUser(
                        telegram_id=telegram_user.id,
                        username=telegram_user.username,
                        first_name=telegram_user.first_name,
                        last_name=telegram_user.last_name,
                        language_code=telegram_user.language_code or "ar"
                    )
                    session.add(db_user)
                    await session.commit()
                    logging.info(f"✅ Created new user: {telegram_user.id}")
                
                # تحديث بيانات المستخدم إذا لزم الأمر
                if (db_user.username != telegram_user.username or 
                    db_user.first_name != telegram_user.first_name):
                    db_user.username = telegram_user.username
                    db_user.first_name = telegram_user.first_name
                    db_user.last_name = telegram_user.last_name
                    await session.commit()
                
                # إضافة المستخدم إلى بيانات الحدث
                data["db_user"] = db_user
                
        except Exception as e:
            logging.error(f"❌ Auth middleware error: {e}")
            # الاستمرار حتى في حالة الخطأ (لا نمنع المستخدم)
        
        return await handler(event, data)
