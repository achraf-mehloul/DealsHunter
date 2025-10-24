"""
معالج الاشتراك في الإشعارات
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from telegram_bot.database.models import User, get_session

router = Router()

@router.message(Command("notifications"))
async def manage_notifications(message: Message):
    """
    إدارة إعدادات الإشعارات
    """
    try:
        user_id = message.from_user.id
        
        async with next(get_session()) as session:
            user = await session.get(User, user_id)
            
            if user:
                status = "مفعّلة" if user.notifications_enabled else "معطّلة"
                notifications_text = (
                    f"🔔 **إدارة الإشعارات**\n\n"
                    f"الحالة الحالية: **{status}**\n\n"
                    "يمكنك تفعيل أو تعطيل الإشعارات التالية:\n"
                    "• 📉 تنبيهات انخفاض الأسعار\n"
                    "• 🆕 إشعارات المنتجات الجديدة\n"
                    "• 📦 تنبيهات تغير المخزون\n"
                    "• 🎉 عروض وتخفيضات"
                )
                
                await message.answer(notifications_text, parse_mode="Markdown")
            else:
                await message.answer("❌ لم يتم العثور على بيانات حسابك.")
                
    except Exception as e:
        logging.error(f"❌ خطأ في إدارة الإشعارات: {e}")
        await message.answer("❌ حدث خطأ في إدارة الإشعارات.")
