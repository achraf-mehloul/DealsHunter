"""
معالج تفاصيل المنتج
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from telegram_bot.database.models import Product, Favorite, get_session
from telegram_bot.keyboards.inline import get_product_details_keyboard

router = Router()

@router.callback_query(F.data.startswith("product_detail_"))
async def show_product_details(callback: CallbackQuery):
    """
    عرض تفاصيل المنتج
    """
    try:
        product_id = int(callback.data.split("_")[2])
        user_id = callback.from_user.id
        
        async with next(get_session()) as session:
            product = await session.get(Product, product_id)
            
            if product:
                # التحقق إذا كان المنتج في المفضلة
                favorite = await session.get(Favorite, (user_id, product_id))
                
                details_text = (
                    f"📦 **{product.name}**\n\n"
                    f"💵 **السعر الحالي:** ${product.price}\n"
                    f"💰 **السعر الأصلي:** ${product.original_price or product.price}\n"
                    f"🎯 **الخصم:** {product.discount_percent}%\n"
                    f"⭐ **التقييم:** {product.rating or 'غير متوفر'}\n"
                    f"📊 **عدد التقييمات:** {product.review_count}\n"
                    f"🛒 **الفئة:** {product.category or 'غير محدد'}\n"
                    f"📦 **التوفر:** {product.availability or 'غير معروف'}\n"
                    f"🚀 **Prime:** {'نعم' if product.prime_eligible else 'لا'}\n"
                    f"🆔 **ASIN:** {product.asin}"
                )
                
                keyboard = get_product_details_keyboard(product.id, user_id, bool(favorite))
                
                if product.image_url:
                    await callback.message.answer_photo(
                        photo=product.image_url,
                        caption=details_text,
                        reply_markup=keyboard,
                        parse_mode="Markdown"
                    )
                else:
                    await callback.message.answer(
                        details_text,
                        reply_markup=keyboard,
                        parse_mode="Markdown"
                    )
                
                await callback.answer()
            else:
                await callback.answer("❌ المنتج غير موجود")
        
    except Exception as e:
        logging.error(f"❌ خطأ في عرض تفاصيل المنتج: {e}")
        await callback.answer("❌ حدث خطأ في عرض التفاصيل.")

@router.callback_query(F.data.startswith("favorite_"))
async def handle_favorite_action(callback: CallbackQuery):
    """
    معالج إضافة/إزالة من المفضلة
    """
    try:
        action = callback.data.split("_")[1]
        product_id = int(callback.data.split("_")[2])
        user_id = callback.from_user.id
        
        async with next(get_session()) as session:
            if action == "add":
                # إضافة للمفضلة
                favorite = Favorite(
                    user_id=user_id,
                    product_id=product_id
                )
                session.add(favorite)
                await session.commit()
                await callback.answer("✅ تم إضافة المنتج إلى المفضلة")
                
            elif action == "remove":
                # إزالة من المفضلة
                favorite = await session.get(Favorite, (user_id, product_id))
                if favorite:
                    await session.delete(favorite)
                    await session.commit()
                    await callback.answer("🗑️ تم إزالة المنتج من المفضلة")
            
    except Exception as e:
        logging.error(f"❌ خطأ في إدارة المفضلة: {e}")
        await callback.answer("❌ حدث خطأ في إدارة المفضلة.")
