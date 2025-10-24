"""
معالج البحث عن المنتجات
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from amazon_core.services.amazon_service import AmazonService
from amazon_core.schemas.product_schemas import ProductSearch
from telegram_bot.states.search_states import SearchStates
from telegram_bot.keyboards.inline import get_search_filters_keyboard, get_products_keyboard

router = Router()

@router.message(F.text == "🔍 بحث عن منتجات")
@router.message(F.text.startswith("/search"))
async def start_search(message: Message, state: FSMContext):
    """
    بدء عملية البحث
    """
    await message.answer("🔍 أرسل كلمة البحث التي تريدها:")
    await state.set_state(SearchStates.waiting_for_query)

@router.message(SearchStates.waiting_for_query)
async def process_search_query(message: Message, state: FSMContext):
    """
    معالجة كلمة البحث
    """
    try:
        search_query = message.text.strip()
        
        if not search_query or len(search_query) < 2:
            await message.answer("❌ كلمة البحث يجب أن تكون على الأقل حرفين.")
            return
        
        await state.update_data(search_query=search_query)
        
        await message.answer(
            f"🔍 البحث عن: **{search_query}**\n\n"
            "هل تريد تطبيق فلاتر معينة على البحث؟",
            reply_markup=get_search_filters_keyboard(),
            parse_mode="Markdown"
        )
        
        await state.set_state(SearchStates.waiting_for_filters)
        
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة البحث: {e}")
        await message.answer("❌ حدث خطأ في البحث.")
        await state.clear()

@router.callback_query(SearchStates.waiting_for_filters, F.data == "search_without_filters")
async def search_without_filters(callback: CallbackQuery, state: FSMContext):
    """
    البحث بدون فلاتر
    """
    try:
        await callback.answer("🔍 جاري البحث...")
        
        data = await state.get_data()
        search_query = data.get("search_query")
        
        if not search_query:
            await callback.message.answer("❌ لم يتم العثور على كلمة البحث.")
            await state.clear()
            return
        
        # البحث باستخدام خدمة أمازون
        amazon_service = AmazonService()
        search_request = ProductSearch(
            query=search_query,
            page=1,
            page_size=5
        )
        
        products = await amazon_service.search_products(search_request)
        
        if not products:
            await callback.message.answer("❌ لم أجد منتجات تطابق بحثك.")
            await state.clear()
            return
        
        # عرض المنتج الأول مع لوحة التنقل
        first_product = products[0]
        keyboard = get_products_keyboard(products, current_index=0, search_query=search_query)
        
        caption = (
            f"📦 **{first_product.name}**\n\n"
            f"💵 **السعر:** ${first_product.price}\n"
            f"⭐ **التقييم:** {first_product.rating or 'غير متوفر'}\n"
            f"🛒 **الفئة:** {first_product.category or 'غير محدد'}\n"
            f"🚀 **Prime:** {'نعم' if first_product.prime_eligible else 'لا'}"
        )
        
        if first_product.image_url:
            await callback.message.answer_photo(
                photo=first_product.image_url,
                caption=caption,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            await callback.message.answer(
                caption,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        
        await state.clear()
        
    except Exception as e:
        logging.error(f"❌ خطأ في البحث بدون فلاتر: {e}")
        await callback.message.answer("❌ حدث خطأ في البحث.")
        await state.clear()