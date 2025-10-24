"""
معالب البث الجماعي
"""

import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from telegram_bot.database.models import User, get_session
from amazon_core.utils.config import config

router = Router()

@router.message(Command("broadcast"))
async def broadcast_message(message: Message, command: CommandObject):
    """
    بث رسالة لجميع المستخدمين
    """
    try:
        # التحقق إذا كان المستخدم مشرف
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer("❌ هذا الأمر متاح للمشرفين فقط.")
            return
        
        if not command.args:
            await message.answer(
                "📢 **البث الجماعي**\n\n"
                "استخدم الأمر كالتالي:\n"
                "`/broadcast نص الرسالة`\n\n"
                "مثال:\n"
                "`/broadcast تم تحديث النظام إلى الإصدار الجديد`",
                parse_mode="Markdown"
            )
            return
        
        broadcast_text = command.args
        
        async with next(get_session()) as session:
            # جلب جميع المستخدمين
            users = await session.execute(User.__table__.select().where(User.is_active == True))
            users_list = users.fetchall()
            
            success_count = 0
            fail_count = 0
            
            for user in users_list:
                try:
                    await message.bot.send_message(
                        chat_id=user.telegram_id,
                        text=f"📢 **إشعار من الإدارة**\n\n{broadcast_text}",
                        parse_mode="Markdown"
                    )
                    success_count += 1
                except Exception as e:
                    logging.error(f"❌ فشل إرسال للمستخدم {user.telegram_id}: {e}")
                    fail_count += 1
            
            # إرسال تقرير البث
            report_text = (
                f"📊 **تقرير البث الجماعي**\n\n"
                f"✅ تم الإرسال بنجاح: {success_count}\n"
                f"❌ فشل في الإرسال: {fail_count}\n"
                f"📝 إجمالي المستهدفين: {len(users_list)}"
            )
            
            await message.answer(report_text, parse_mode="Markdown")
            
    except Exception as e:
        logging.error(f"❌ خطأ في البث الجماعي: {e}")
        await message.answer("❌ حدث خطأ في البث الجماعي.")
