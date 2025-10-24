"""
لوحة المفاتيح الرئيسية
Reply keyboard للقائمة الرئيسية
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    إنشاء لوحة المفاتيح الرئيسية
    
    Returns:
        ReplyKeyboardMarkup: لوحة المفاتيح الرئيسية
    """
    keyboard = [
        [
            KeyboardButton(text="🔍 بحث عن منتجات"),
            KeyboardButton(text="⭐ المفضلة")
        ],
        [
            KeyboardButton(text="🔔 الإشعارات"),
            KeyboardButton(text="⚙️ الإعدادات")
        ],
        [
            KeyboardButton(text="🏠 القائمة الرئيسية")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="اختر من القائمة..."
    )

def get_admin_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    إنشاء لوحة المفاتيح للمشرفين
    
    Returns:
        ReplyKeyboardMarkup: لوحة المفاتيح الإدارية
    """
    keyboard = [
        [
            KeyboardButton(text="📊 الإحصائيات"),
            KeyboardButton(text="👥 إدارة المستخدمين")
        ],
        [
            KeyboardButton(text="📢 بث إشعار"),
            KeyboardButton(text="⚙️ إعدادات البوت")
        ],
        [
            KeyboardButton(text="🏠 القائمة الرئيسية")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="اختر من القائمة الإدارية..."
    )
