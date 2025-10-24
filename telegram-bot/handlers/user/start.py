"""
معالج أمر /start
"""

import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from telegram_bot.database.models import User, get_session
from telegram_bot.keyboards.reply import get_main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    معالج أمر /start - ترحيب بالمستخدم وتسجيله
    """
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username
        
        logging.info(f"👤 مستخدم جديد: {user_id} - {first_name}")
        
        # حفظ/تحديث بيانات المستخدم
        async with next(get_session()) as session:
            user = await session.get(User, user_id)
            
            if not user:
                user = User(
                    telegram_id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=message.from_user.last_name,
                    language_code=message.from_user.language_code or "ar"
                )
                session.add(user)
                await session.commit()
                logging.info(f"✅ تم تسجيل مستخدم جديد: {user_id}")
            else:
                # تحديث البيانات
                user.username = username
                user.first_name = first_name
                user.last_name = message.from_user.last_name
                await session.commit()
        
        # رسالة الترحيب
        welcome_text = (
            f"🎉 أهلاً وسهلاً بك {first_name} في بوت أمازون!\n\n"
            "يمكنك البحث عن منتجات أمازون، حفظ المفضلة، واستقبال إشعارات العروض!\n\n"
            "🔍 /search - البحث عن منتجات\n"
            "⭐ /favorites - عرض المفضلة\n"
            "🔔 /notifications - إدارة الإشعارات\n"
            "⚙️ /settings - الإعدادات"
        )
        
        await message.answer(
            welcome_text,
            reply_markup=get_main_menu_keyboard()
        )
        
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة /start: {e}")
        await message.answer("❌ حدث خطأ أثناء بدء البوت. الرجاء المحاولة لاحقاً.")