"""
Middleware التحليلات
تتبع إحصائيات استخدام البوت
"""

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from telegram_bot.database.models import get_session

class AnalyticsMiddleware(BaseMiddleware):
    """
    middleware لتتبع إحصائيات الاستخدام
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        تسجيل إحصائيات الاستخدام
        """
        try:
            user = data.get("db_user")
            
            if isinstance(event, Message) and user:
                # تسجيل رسالة المستخدم
                await self._log_message(event, user)
            
            elif isinstance(event, CallbackQuery) and user:
                # تسجيل تفاعل الكallback
                await self._log_callback(event, user)
                
        except Exception as e:
            logging.error(f"❌ Analytics middleware error: {e}")
            # لا نوقف العملية في حالة خطأ التحليلات
        
        return await handler(event, data)
    
    async def _log_message(self, message: Message, user):
        """
        تسجيل رسالة المستخدم
        """
        # يمكن توسيعه لتسجيل تفاصيل أكثر في قاعدة البيانات
        logging.info(
            f"📨 Message from {user.telegram_id} ({user.username}): "
            f"{message.text or message.caption or 'Media'}"
        )
    
    async def _log_callback(self, callback: CallbackQuery, user):
        """
        تسجيل تفاعل الكallback
        """
        logging.info(
            f"🔄 Callback from {user.telegram_id} ({user.username}): "
            f"{callback.data}"
        )
