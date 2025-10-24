"""
معالج إعدادات المستخدم
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_bot.database.models import User, get_session
from telegram_bot.keyboards.inline import get_settings_keyboard

router = Router()

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """
    عرض إعدادات المستخدم
    """
    try:
        user_id = message.from_user.id
        
        async with next(get_session()) as session:
            user = await session.get(User, user_id)
            
            if user:
                settings_text = (
                    f"⚙️ **إعدادات حسابك**\n\n"
                    f"👤 الاسم: {user.first_name} {user.last_name or ''}\n"
                    f"🔔 الإشعارات: {'مفعّلة' if user.notifications_enabled else 'معطلة'}\n"
                    f"🌐 اللغة: {user.language_code}\n"
                    f"📅 تاريخ التسجيل: {user.created_at.strftime('%Y-%m-%d')}"
                )
            else:
                settings_text = "❌ لم يتم العثور على بيانات حسابك."
        
        await message.answer(
            settings_text,
            reply_markup=get_settings_keyboard(user_id),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logging.error(f"❌ خطأ في عرض الإعدادات: {e}")
        await message.answer("❌ حدث خطأ في عرض الإعدادات.")

@router.callback_query(F.data.startswith("settings_"))
async def handle_settings_callback(callback: CallbackQuery):
    """
    معالج تفاعلات الإعدادات
    """
    try:
        data = callback.data
        user_id = callback.from_user.id
        
        if data == "settings_toggle_notifications":
            # تبديل حالة الإشعارات
            async with next(get_session()) as session:
                user = await session.get(User, user_id)
                if user:
                    user.notifications_enabled = not user.notifications_enabled
                    await session.commit()
                    
                    status = "مفعّلة" if user.notifications_enabled else "معطلة"
                    await callback.answer(f"تم {status} الإشعارات")
                    
                    # تحديث الرسالة
                    settings_text = (
                        f"⚙️ **إعدادات حسابك**\n\n"
                        f"👤 الاسم: {user.first_name} {user.last_name or ''}\n"
                        f"🔔 الإشعارات: {'مفعّلة' if user.notifications_enabled else 'معطلة'}\n"
                        f"🌐 اللغة: {user.language_code}\n"
                        f"📅 تاريخ التسجيل: {user.created_at.strftime('%Y-%m-%d')}"
                    )
                    
                    await callback.message.edit_text(
                        settings_text,
                        reply_markup=get_settings_keyboard(user_id),
                        parse_mode="Markdown"
                    )
        
        elif data == "settings_change_language":
            await callback.answer("🚧 هذه الميزة قيد التطوير")
            
        elif data == "settings_help":
            await callback.message.answer(
                "📖 **دليل استخدام البوت:**\n\n"
                "🔍 /search - البحث عن منتجات\n"
                "⭐ /favorites - عرض المفضلة\n"
                "🔔 /notifications - إدارة الإشعارات\n"
                "👤 /profile - الملف الشخصي\n"
                "⚙️ /settings - الإعدادات",
                parse_mode="Markdown"
            )
            await callback.answer()
            
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة إعدادات الكallback: {e}")
        await callback.answer("❌ حدث خطأ في معالجة الطلب.")
