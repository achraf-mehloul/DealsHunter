"""
لوحات مفاتيح الفلترة
Inline keyboards لإعدادات الفلترة
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_search_filters_keyboard() -> InlineKeyboardMarkup:
    """
    إنشاء لوحة مفاتيح فلاتر البحث
    
    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="💰 فلترة بالسعر",
                callback_data="filter_price"
            ),
            InlineKeyboardButton(
                text="⭐ فلترة بالتقييم",
                callback_data="filter_rating"
            )
        ],
        [
            InlineKeyboardButton(
                text="📦 فلترة بالفئة", 
                callback_data="filter_category"
            ),
            InlineKeyboardButton(
                text="🚀 Prime فقط",
                callback_data="filter_prime"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎯 العروض فقط",
                callback_data="filter_discount"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 بحث بدون فلاتر",
                callback_data="search_without_filters"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ إلغاء البحث",
                callback_data="cancel_search"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_price_filter_keyboard() -> InlineKeyboardMarkup:
    """
    إنشاء لوحة مفاتيح فلترة السعر
    
    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح
    """
    buttons = [
        [
            InlineKeyboardButton(text="$0 - $25", callback_data="price_0_25"),
            InlineKeyboardButton(text="$25 - $50", callback_data="price_25_50")
        ],
        [
            InlineKeyboardButton(text="$50 - $100", callback_data="price_50_100"),
            InlineKeyboardButton(text="$100 - $200", callback_data="price_100_200")
        ],
        [
            InlineKeyboardButton(text="$200+", callback_data="price_200_plus"),
            InlineKeyboardButton(text💰 سعر مخصص", callback_data="price_custom")
        ],
        [
            InlineKeyboardButton(text="⬅️ رجوع", callback_data="back_to_filters")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_rating_filter_keyboard() -> InlineKeyboardMarkup:
    """
    إنشاء لوحة مفاتيح فلترة التقييم
    
    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح
    """
    buttons = [
        [
            InlineKeyboardButton(text="⭐ 4.0+", callback_data="rating_4"),
            InlineKeyboardButton(text="⭐⭐ 4.5+", callback_data="rating_4.5")
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐ 5.0", callback_data="rating_5"),
            InlineKeyboardButton(text="⭐ أي تقييم", callback_data="rating_any")
        ],
        [
            InlineKeyboardButton(text="⬅️ رجوع", callback_data="back_to_filters")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_category_filter_keyboard() -> InlineKeyboardMarkup:
    """
    إنشاء لوحة مفاتيح فلترة الفئة
    
    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح
    """
    buttons = [
        [
            InlineKeyboardButton(text="📱 إلكترونيات", callback_data="category_electronics"),
            InlineKeyboardButton(text="👕 ملابس", callback_data="category_clothing")
        ],
        [
            InlineKeyboardButton(text="🏠 منزل", callback_data="category_home"),
            InInlineKeyboardButton(text="📚 كتب", callback_data="category_books")
        ],
        [
            InlineKeyboardButton(text="🎮 ألعاب", callback_data="category_games"),
            InlineKeyboardButton(text="💄 تجميل", callback_data="category_beauty")
        ],
        [
            InlineKeyboardButton(text="⬅️ رجوع", callback_data="back_to_filters")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
