"""
معالج الملف الشخصي
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from telegram_bot.database.models import User, get_session

router = Router()

@router.message(Command("profile"))
async def cmd_profile(message: Message):
    """
    عرض الملف الشخصي للمستخدم
    """
    try:
        user_id = message.from_user.id
        
        async with next(get_session()) as session:
            user = await session.get(User, user_id)
            
            if user:
                profile_text = (
                    f"👤 **الملف الشخصي**\n\n"
                    f"🆔 المعرف: `{user.telegram_id}`\n"
                    f"👤 الاسم: {user.first_name} {user.last_name or ''}\n"
                    f"📛 اسم المستخدم: @{user.username or 'غير محدد'}\n"
                    f"🌐 اللغة: {user.language_code}\n"
                    f"🔔 الإشعارات: {'مفعّلة' if user.notifications_enabled else 'معطلة'}\n"
                    f"📅 تاريخ التسجيل: {user.created_at.strftime('%Y-%m-%d')}\n"
                    f"🔄 آخر تحديث: {user.updated_at.strftime('%Y-%m-%d')}"
                )
            else:
                profile_text = "❌ لم يتم العثور على بيانات حسابك."
        
        await message.answer(profile_text, parse_mode="Markdown")
        
    except Exception as e:
        logging.error(f"❌ خطأ في عرض الملف الشخصي: {e}")
        await message.answer("❌ حدث خطأ في عرض الملف الشخصي.")
