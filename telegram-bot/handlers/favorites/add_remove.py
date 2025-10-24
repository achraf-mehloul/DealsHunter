"""
معالج إضافة وإزالة المفضلة
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from telegram_bot.database.models import Favorite, get_session

router = Router()

@router.callback_query(F.data.startswith("favorite_add_"))
async def add_to_favorites(callback: CallbackQuery):
    """
    إضافة منتج إلى المفضلة
    """
    try:
        product_id = int(callback.data.split("_")[2])
        user_id = callback.from_user.id
        
        async with next(get_session()) as session:
            # التحقق إذا كان المنتج مضاف بالفعل
            existing_favorite = await session.get(Favorite, (user_id, product_id))
            
            if not existing_favorite:
                favorite = Favorite(
                    user_id=user_id,
                    product_id=product_id
                )
                session.add(favorite)
                await session.commit()
                
                await callback.answer("✅ تم إضافة المنتج إلى المفضلة")
            else:
                await callback.answer("⚠️ المنتج مضاف بالفعل إلى المفضلة")
                
    except Exception as e:
        logging.error(f"❌ خطأ في إضافة المفضلة: {e}")
        await callback.answer("❌ حدث خطأ في إضافة المنتج إلى المفضلة")

@router.callback_query(F.data.startswith("favorite_remove_"))
async def remove_from_favorites(callback: CallbackQuery):
    """
    إزالة منتج من المفضلة
    """
    try:
        product_id = int(callback.data.split("_")[2])
        user_id = callback.from_user.id
        
        async with next(get_session()) as session:
            favorite = await session.get(Favorite, (user_id, product_id))
            
            if favorite:
                await session.delete(favorite)
                await session.commit()
                
                await callback.answer("🗑️ تم إزالة المنتج من المفضلة")
            else:
                await callback.answer("⚠️ المنتج غير موجود في المفضلة")
                
    except Exception as e:
        logging.error(f"❌ خطأ في إزالة المفضلة: {e}")
        await callback.answer("❌ حدث خطأ في إزالة المنتج من المفضلة")
