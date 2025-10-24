"""
معالج فلاتر البحث
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram_bot.states.search_states import SearchStates
from telegram_bot.keyboards.inline import (
    get_price_filter_keyboard, 
    get_rating_filter_keyboard,
    get_category_filter_keyboard
)

router = Router()

@router.callback_query(SearchStates.waiting_for_filters, F.data.startswith("filter_"))
async def handle_filter_selection(callback: CallbackQuery, state: FSMContext):
    """
    معالج اختيار نوع الفلترة
    """
    try:
        filter_type = callback.data.replace("filter_", "")
        
        if filter_type == "price":
            await callback.message.edit_reply_markup(
                reply_markup=get_price_filter_keyboard()
            )
            await callback.answer("💰 اختر نطاق السعر")
            
        elif filter_type == "rating":
            await callback.message.edit_reply_markup(
                reply_markup=get_rating_filter_keyboard()
            )
            await callback.answer("⭐ اختر حد التقييم")
            
        elif filter_type == "category":
            await callback.message.edit_reply_markup(
                reply_markup=get_category_filter_keyboard()
            )
            await callback.answer("📦 اختر الفئة")
            
        elif filter_type == "prime":
            data = await state.get_data()
            current_filters = data.get("filters", {})
            current_filters["prime_only"] = not current_filters.get("prime_only", False)
            
            await state.update_data(filters=current_filters)
            
            status = "مفعّل" if current_filters["prime_only"] else "معطّل"
            await callback.answer(f"فلتر Prime {status}")
            
        elif filter_type == "discount":
            data = await state.get_data()
            current_filters = data.get("filters", {})
            current_filters["has_discount"] = not current_filters.get("has_discount", False)
            
            await state.update_data(filters=current_filters)
            
            status = "مفعّل" if current_filters["has_discount"] else "معطّل"
            await callback.answer(f"فلتر الخصم {status}")
            
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة الفلتر: {e}")
        await callback.answer("❌ حدث خطأ في معالجة الفلتر.")

@router.callback_query(F.data.startswith("price_"))
async def handle_price_filter(callback: CallbackQuery, state: FSMContext):
    """
    معالج فلترة السعر
    """
    try:
        price_range = callback.data.replace("price_", "")
        
        data = await state.get_data()
        current_filters = data.get("filters", {})
        
        if price_range == "0_25":
            current_filters["min_price"] = 0
            current_filters["max_price"] = 25
        elif price_range == "25_50":
            current_filters["min_price"] = 25
            current_filters["max_price"] = 50
        elif price_range == "50_100":
            current_filters["min_price"] = 50
            current_filters["max_price"] = 100
        elif price_range == "100_200":
            current_filters["min_price"] = 100
            current_filters["max_price"] = 200
        elif price_range == "200_plus":
            current_filters["min_price"] = 200
            current_filters["max_price"] = None
        
        await state.update_data(filters=current_filters)
        await callback.answer("✅ تم تطبيق فلتر السعر")
        
        # العودة للفلاتر الرئيسية
        await callback.message.edit_reply_markup(
            reply_markup=get_search_filters_keyboard()
        )
        
    except Exception as e:
        logging.error(f"❌ خطأ في فلترة السعر: {e}")
        await callback.answer("❌ حدث خطأ في تطبيق الفلتر.")
