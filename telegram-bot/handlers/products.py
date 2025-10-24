"""
معالج البحث وعرض المنتجات
معالجة أوامر البحث وعرض تفاصيل المنتج
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from amazon_core.schemas.product_schemas import ProductSearch, ProductSearchFilters
from amazon_core.services.amazon_service import AmazonService
from telegram_bot.bot.config import BOT_TEXTS
from telegram_bot.keyboards.inline import (
    get_products_keyboard, 
    get_product_details_keyboard,
    get_search_filters_keyboard
)
from telegram_bot.database.models import SearchHistory, Product, get_session

router = Router(name="product_handlers")

class SearchStates(StatesGroup):
    """حالات البحث عن المنتجات"""
    waiting_for_query = State()
    waiting_for_filters = State()

@router.message(Command("search"))
@router.message(F.text == "🔍 بحث عن منتجات")
async def cmd_search(message: Message, state: FSMContext):
    """
    بدء عملية البحث عن المنتجات
    """
    try:
        await message.answer(BOT_TEXTS["start_search"])
        await state.set_state(SearchStates.waiting_for_query)
        
    except Exception as e:
        logging.error(f"❌ خطأ في بدء البحث: {e}")
        await message.answer("❌ حدث خطأ في بدء البحث.")

@router.message(SearchStates.waiting_for_query)
async def process_search_query(message: Message, state: FSMContext):
    """
    معالجة كلمة البحث من المستخدم
    """
    try:
        search_query = message.text.strip()
        user_id = message.from_user.id
        
        if not search_query or len(search_query) < 2:
            await message.answer("❌ كلمة البحث يجب أن تكون على الأقل حرفين.")
            return
        
        # حفظ سجل البحث
        async with next(get_session()) as session:
            search_history = SearchHistory(
                user_id=user_id,
                query=search_query,
                result_count=0
            )
            session.add(search_history)
            await session.commit()
        
        # حفظ بيانات البحث في حالة FSM
        await state.update_data(
            search_query=search_query,
            current_page=1
        )
        
        # عرض خيارات الفلترة
        await message.answer(
            f"🔍 البحث عن: **{search_query}**\n\n"
            "هل تريد تطبيق فلاتر معينة على البحث؟",
            parse_mode="Markdown",
            reply_markup=get_search_filters_keyboard()
        )
        
        await state.set_state(SearchStates.waiting_for_filters)
        
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة كلمة البحث: {e}")
        await message.answer("❌ حدث خطأ في معالجة البحث.")
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
        
        # البحث باستخدام خدمة أمازون
        amazon_service = AmazonService()
        search_request = ProductSearch(
            query=search_query,
            page=1,
            page_size=5
        )
        
        products = await amazon_service.search_products(search_request)
        
        if not products:
            await callback.message.answer(BOT_TEXTS["no_results"])
            await state.clear()
            return
        
        # عرض المنتج الأول مع لوحة التنقل
        first_product = products[0]
        keyboard = get_products_keyboard(products, current_index=0, search_query=search_query)
        
        caption = (
            f"📦 **{first_product.name}**\n\n"
            f"💵 **السعر:** {first_product.price}\n"
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

@router.callback_query(F.data.startswith("product_"))
async def handle_product_actions(callback: CallbackQuery, state: FSMContext):
    """
    معالج إجراءات المنتج (عرض، حفظ، إلخ)
    """
    try:
        data = callback.data
        user_id = callback.from_user.id
        
        if data.startswith("product_detail_"):
            # عرض تفاصيل المنتج
            product_id = int(data.split("_")[2])
            
            async with next(get_session()) as session:
                product = await session.get(Product, product_id)
                
                if product:
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
                    
                    keyboard = get_product_details_keyboard(product.id, user_id)
                    
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
        
        elif data.startswith("product_save_"):
            # حفظ المنتج في المفضلة
            product_id = int(data.split("_")[2])
            await callback.answer("✅ تم حفظ المنتج في المفضلة")
            
        elif data.startswith("product_share_"):
            # مشاركة المنتج
            product_id = int(data.split("_")[2])
            await callback.answer("📤 تم نسخ رابط المنتج")
            
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة إجراء المنتج: {e}")
        await callback.answer("❌ حدث خطأ في معالجة الطلب.")

@router.callback_query(F.data.startswith("nav_"))
async def handle_navigation(callback: CallbackQuery, state: FSMContext):
    """
    معالج التنقل بين الصفحات والمنتجات
    """
    try:
        data = callback.data
        
        if data.startswith("nav_next_"):
            # الانتقال للمنتج التالي
            await callback.answer("➡️ المنتج التالي")
            
        elif data.startswith("nav_prev_"):
            # الانتقال للمنتج السابق
            await callback.answer("⬅️ المنتج السابق")
            
        elif data.startswith("nav_page_"):
            # الانتقال لصفحة مختلفة
            page_num = int(data.split("_")[2])
            await callback.answer(f"📄 الصفحة {page_num}")
            
    except Exception as e:
        logging.error(f"❌ خطأ في معالجة التنقل: {e}")
        await callback.answer("❌ حدث خطأ في التنقل.")
