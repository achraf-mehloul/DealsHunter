"""
معالج التنبيهات والإشعارات
"""

import logging
from aiogram import Router
from aiogram.types import Message

router = Router()

async def send_price_drop_alert(user_id: int, product, old_price: float, new_price: float):
    """
    إرسال تنبيه انخفاض السعر
    """
    try:
        from telegram_bot.bot import bot
        
        discount_percent = ((old_price - new_price) / old_price) * 100
        
        alert_text = (
            f"🎉 **انخفاض السعر!**\n\n"
            f"📦 **{product.name}**\n\n"
            f"💰 السعر القديم: ${old_price}\n"
            f"💵 السعر الجديد: ${new_price}\n"
            f"🎯 وفرت: {discount_percent:.1f}%\n\n"
            f"🛒 [اشتري الآن]({product.product_url})"
        )
        
        await bot.send_message(
            chat_id=user_id,
            text=alert_text,
            parse_mode="Markdown",
            disable_web_page_preview=False
        )
        
        logging.info(f"✅ تم إرسال تنبيه انخفاض السعر للمستخدم {user_id}")
        
    except Exception as e:
        logging.error(f"❌ خطأ في إرسال تنبيه السعر: {e}")

async def send_new_product_alert(user_id: int, product):
    """
    إرسال تنبيه منتج جديد
    """
    try:
        from telegram_bot.bot import bot
        
        alert_text = (
            f"🆕 **منتج جديد!**\n\n"
            f"📦 **{product.name}**\n\n"
            f"💵 السعر: ${product.price}\n"
            f"⭐ التقييم: {product.rating or 'غير متوفر'}\n"
            f"🛒 الفئة: {product.category or 'غير محدد'}\n\n"
            f"🛒 [عرض المنتج]({product.product_url})"
        )
        
        if product.image_url:
            await bot.send_photo(
                chat_id=user_id,
                photo=product.image_url,
                caption=alert_text,
                parse_mode="Markdown"
            )
        else:
            await bot.send_message(
                chat_id=user_id,
                text=alert_text,
                parse_mode="Markdown"
            )
        
        logging.info(f"✅ تم إرسال تنبيه منتج جديد للمستخدم {user_id}")
        
    except Exception as e:
        logging.error(f"❌ خطأ في إرسال تنبيه المنتج الجديد: {e}")
