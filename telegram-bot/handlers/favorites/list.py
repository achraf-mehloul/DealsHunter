"""
معالج عرض قائمة المفضلة
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from telegram_bot.database.models import Favorite, Product, get_session
from telegram_bot.keyboards.inline import get_products_keyboard

router = Router()

@router.message(F.text == "⭐ المفضلة")
@router.message(Command("favorites"))
async def show_favorites(message: Message):
    """
    عرض قائمة المنتجات المفضلة
    """
    try:
        user_id = message.from_user.id
        
        async with next(get_session()) as session:
            # جلب المنتجات المفضلة
            favorites = await session.execute(
                Favorite.__table__.select().where(Favorite.user_id == user_id)
            )
            favorite_products = []
            
            for fav in favorites:
                product = await session.get(Product, fav.product_id)
                if product:
                    favorite_products.append(product)
            
            if not favorite_products:
                await message.answer(
                    "⭐ **قائمة المفضلة**\n\n"
                    "لم تقم بإضافة أي منتجات إلى المفضلة بعد.\n\n"
                    "استخدم 🔍 بحث عن منتجات ثم اضغط على 💾 حفظ في المفضلة لإضافة منتجات.",
                    parse_mode="Markdown"
                )
                return
            
            # عرض أول منتج في القائمة
            first_product = favorite_products[0]
            keyboard = get_products_keyboard(favorite_products, current_index=0, is_favorites=True)
            
            caption = (
                f"⭐ **قائمة المفضلة**\n\n"
                f"📦 **{first_product.name}**\n\n"
                f"💵 **السعر:** ${first_product.price}\n"
                f"⭐ **التقييم:** {first_product.rating or 'غير متوفر'}\n"
                f"🛒 **الفئة:** {first_product.category or 'غير محدد'}\n"
                f"🚀 **Prime:** {'نعم' if first_product.prime_eligible else 'لا'}"
            )
            
            if first_product.image_url:
                await message.answer_photo(
                    photo=first_product.image_url,
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            else:
                await message.answer(
                    caption,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
                
    except Exception as e:
        logging.error(f"❌ خطأ في عرض المفضلة: {e}")
        await message.answer("❌ حدث خطأ في عرض قائمة المفضلة.")
