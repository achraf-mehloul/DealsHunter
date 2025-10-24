"""
معالج أوامر البداية والإعدادات
معالجة أوامر /start, /help, /settings
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from amazon_core.utils.config import config
from telegram_bot.bot.config import BOT_TEXTS
from telegram_bot.keyboards.reply import get_main_menu_keyboard
from telegram_bot.keyboards.inline import get_settings_keyboard
from telegram_bot.database.models import User, get_session

router = Router(name="start_handlers")

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    معالج أمر /start
    ترحيب بالمستخدم وتسجيله في النظام
    """
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username
        
        logging.info(f"👤 مستخدم جديد: {user_id} - {first_name}")
        
        # حفظ/تحديث بيانات المستخدم في قاعدة البيانات
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
                # تحديث بيانات المستخدم إذا كانت متغيرة
                user.username = username
                user.first_name = first_name
                user.last_name = message.from_user.last_name
                await session.commit()
                logging.info(f"✅ تم تحديث بيانات المستخدم: {user_id}")
        
        # إرسال رسالة الترحيب
        welcome_text = BOT_TEXTS["welcome"].format(first_name=first_name)
        
        await message.answer(
            welcome_text,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة أمر /start: {e}")
        await message.answer(
            "❌ حدث خطأ أثناء بدء البوت. الرجاء المحاولة لاحقاً.",
            reply_markup=get_main_menu_keyboard()
        )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    معالج أمر /help
    عرض دليل استخدام البوت
    """
    try:
        await message.answer(
            BOT_TEXTS["help"],
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة أمر /help: {e}")
        await message.answer("❌ حدث خطأ في عرض المساعدة.")

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """
    معالج أمر /settings
    عرض إعدادات البوت
    """
    try:
        user_id = message.from_user.id
        
        # جلب إعدادات المستخدم من قاعدة البيانات
        async with next(get_session()) as session:
            user = await session.get(User, user_id)
            
            if user:
                settings_text = (
                    "⚙️ **إعدادات حسابك:**\n\n"
                    f"👤 الاسم: {user.first_name} {user.last_name or ''}\n"
                    f"🔔 الإشعارات: {'مفعّلة' if user.notifications_enabled else 'معطلة'}\n"
                    f"🌐 اللغة: {user.language_code}\n"
                    f"📅 تاريخ التسجيل: {user.created_at.strftime('%Y-%m-%d')}"
                )
            else:
                settings_text = "❌ لم يتم العثور على بيانات حسابك."
        
        await message.answer(
            settings_text,
            parse_mode="Markdown",
            reply_markup=get_settings_keyboard(user_id)
        )
        
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة أمر /settings: {e}")
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
                    await callback.message.edit_reply_markup(
                        reply_markup=get_settings_keyboard(user_id)
                    )
        
        elif data == "settings_change_language":
            await callback.answer("🚧 هذه الميزة قيد التطوير")
            
        elif data == "settings_help":
            await callback.message.answer(BOT_TEXTS["help"], parse_mode="Markdown")
            await callback.answer()
            
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة إعدادات الكallback: {e}")
        await callback.answer("❌ حدث خطأ في معالجة الطلب.")

@router.message(F.text == "🏠 القائمة الرئيسية")
async def main_menu_handler(message: Message):
    """
    معالج زر القائمة الرئيسية
    """
    try:
        await message.answer(
            "🏠 **القائمة الرئيسية**\n\n"
            "اختر أحد الخيارات التالية:",
            reply_markup=get_main_menu_keyboard()
        )
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة القائمة الرئيسية: {e}")
        await message.answer("❌ حدث خطأ في عرض القائمة.")

# معالجة الرسائل غير المعروفة
@router.message()
async def unknown_message_handler(message: Message):
    """
    معالج الرسائل غير المعروفة
    """
    await message.answer(
        "❓ لم أفهم طلبك.\n"
        "استخدم /help لعرض الأوامر المتاحة.",
        reply_markup=get_main_menu_keyboard()
    )
