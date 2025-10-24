"""
لوحة المفاتيح السريعة
Reply keyboard للأوامر السريعة
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_quick_actions_keyboard() -> ReplyKeyboardMarkup:
    """
    إنشاء لوحة المفاتيح السريعة
    
    Returns:
        ReplyKeyboardMarkup: لوحة المفاتيح السريعة
    """
    keyboard = [
        [
            KeyboardButton(text="🔍 بحث سريع"),
            KeyboardButton(text="📈 العروض الحالية")
        ],
        [
            KeyboardButton(text="⭐ منتجاتي المفضلة"),
            KeyboardButton(text="🔔 إشعاراتي")
        ],
        [
            KeyboardButton(text="🆘 المساعدة"),
            KeyboardButton(text="⚡ الإعدادات السريعة")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="اختر أمراً سريعاً..."
    )

def get_search_actions_keyboard() -> ReplyKeyboardMarkup:
    """
    لوحة مفاتيح خاصة بالبحث
    
    Returns:
        ReplyKeyboardMarkup: لوحة مفاتيح البحث
    """
    keyboard = [
        [
            KeyboardButton(text="💰 فلترة بالسعر"),
            KeyboardButton(text="⭐ فلترة بالتقييم")
        ],
        [
            KeyboardButton(text="📦 فلترة بالفئة"),
            KeyboardButton(text="🚀 منتجات Prime فقط")
        ],
        [
            KeyboardButton(text="🔍 بحث جديد"),
            KeyboardButton(text="🏠 القائمة الرئيسية")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="اختر نوع الفلترة..."
    )
