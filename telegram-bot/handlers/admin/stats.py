"""
معالج إحصائيات المشرف
"""

import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from telegram_bot.database.models import User, Product, get_session
from amazon_core.utils.config import config

router = Router()

@router.message(Command("stats"))
async def show_stats(message: Message):
    """
    عرض إحصائيات النظام للمشرفين
    """
    try:
        # التحقق إذا كان المستخدم مشرف
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer("❌ هذا الأمر متاح للمشرفين فقط.")
            return
        
        async with next(get_session()) as session:
            # جلب الإحصائيات
            total_users = await session.execute(User.__table__.count())
            total_products = await session.execute(Product.__table__.count())
            active_users = await session.execute(
                User.__table__.count().where(User.is_active == True)
            )
            
            stats_text = (
                "📊 **إحصائيات النظام**\n\n"
                f"👥 **إجمالي المستخدمين:** {total_users.scalar()}\n"
                f"✅ **المستخدمين النشطين:** {active_users.scalar()}\n"
                f"📦 **إجمالي المنتجات:** {total_products.scalar()}\n"
                f"🤖 **حالة البوت:** 🟢 يعمل\n"
                f"🔄 **آخر تحديث:** {message.date.strftime('%Y-%m-%d %H:%M')}"
            )
            
            await message.answer(stats_text, parse_mode="Markdown")
            
    except Exception as e:
        logging.error(f"❌ خطأ في عرض الإحصائيات: {e}")
        await message.answer("❌ حدث خطأ في عرض الإحصائيات.")
