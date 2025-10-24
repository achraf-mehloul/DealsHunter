"""
لوحات مفاتيح المنتجات
Inline keyboards لعرض المنتجات وإدارتها
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Optional

def get_products_keyboard(
    products: List, 
    current_index: int = 0,
    search_query: str = "",
    page: int = 1,
    total_pages: int = 1
) -> InlineKeyboardMarkup:
    """
    إنشاء لوحة مفاتيح لعرض المنتجات مع التنقل
    
    Args:
        products: قائمة المنتجات
        current_index: الفهرس الحالي
        search_query: كلمة البحث
        page: الصفحة الحالية
        total_pages: إجمالي الصفحات
        
    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح
    """
    buttons = []
    
    if products:
        current_product = products[current_index]
        
        # أزرار المنتج الحالي
        buttons.append([
            InlineKeyboardButton(
                text="📦 عرض التفاصيل",
                callback_data=f"product_detail_{current_product.id}"
            )
        ])
        
        buttons.append([
            InlineKeyboardButton(
                text="💾 حفظ في المفضلة", 
                callback_data=f"product_save_{current_product.id}"
            ),
            InlineKeyboardButton(
                text="📤 مشاركة",
                callback_data=f"product_share_{current_product.id}"
            )
        ])
    
    # أزرار التنقل بين المنتجات
    nav_buttons = []
    
    if current_index > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ السابق",
                callback_data=f"nav_prev_{current_index - 1}"
            )
        )
    
    if current_index < len(products) - 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="التالي ➡️",
                callback_data=f"nav_next_{current_index + 1}"
            )
        )
    
    if nav_buttons:
        buttons.append(nav_buttons)
    
    # أزرار التنقل بين الصفحات
    if total_pages > 1:
        page_buttons = []
        
        if page > 1:
            page_buttons.append(
                InlineKeyboardButton(
                    text="◀️ الصفحة السابقة",
                    callback_data=f"nav_page_{page - 1}"
                )
            )
        
        page_buttons.append(
            InlineKeyboardButton(
                text=f"📄 {page}/{total_pages}",
                callback_data="current_page"
            )
        )
        
        if page < total_pages:
            page_buttons.append(
                InlineKeyboardButton(
                    text="الصفحة التالية ▶️",
                    callback_data=f"nav_page_{page + 1}"
                )
            )
        
        buttons.append(page_buttons)
    
    # زر البحث مرة أخرى
    if search_query:
        buttons.append([
            InlineKeyboardButton(
                text="🔍 بحث جديد",
                callback_data="new_search"
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_product_details_keyboard(product_id: int, user_id: int) -> InlineKeyboardMarkup:
    """
    إنشاء لوحة مفاتيح تفاصيل المنتج
    
    Args:
        product_id: معرف المنتج
        user_id: معرف المستخدم
        
    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="💾 إضافة إلى المفضلة",
                callback_data=f"favorite_add_{product_id}"
            ),
            InlineKeyboardButton(
                text="❌ إزالة من المفضلة", 
                callback_data=f"favorite_remove_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🛒 شراء الآن",
                url=f"https://amazon.com/dp/{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔔 تفعيل تنبيه السعر",
                callback_data=f"alert_price_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📤 مشاركة المنتج",
                callback_data=f"share_product_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ العودة للنتائج",
                callback_data="back_to_results"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
