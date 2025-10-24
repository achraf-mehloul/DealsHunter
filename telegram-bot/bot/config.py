"""
إعدادات البوت الخاصة
تهيئة وإعدادات خاصة ببوت تليجرام
"""

import logging
from typing import Dict, Any

from amazon_core.utils.config import config

# إعدادات واجهات المستخدم
BOT_SETTINGS: Dict[str, Any] = {
    "max_products_per_page": config.MAX_PRODUCTS_PER_PAGE,
    "cache_timeout": config.CACHE_TIMEOUT,
    "request_timeout": config.REQUEST_TIMEOUT,
    "default_language": "ar",
    "supported_languages": ["ar", "en"],
    "admin_ids": config.ADMIN_IDS,
}

# نصوص البوت بالعربية
BOT_TEXTS: Dict[str, str] = {
    "welcome": "🎉 أهلاً وسهلاً بك في بوت أمازون!\n\n"
               "يمكنك البحث عن منتجات أمازون، حفظ المفضلة، واستقبال إشعارات العروض!",
    
    "help": "📖 **دليل استخدام البوت:**\n\n"
            "🔍 /search - البحث عن منتجات\n"
            "⭐ /favorites - عرض المفضلة\n"
            "🔔 /notifications - إدارة الإشعارات\n"
            "⚙️ /settings - الإعدادات\n"
            "👨‍💼 /admin - لوحة الإدارة (للمشرفين)",
    
    "start_search": "🔍 أرسل كلمة البحث التي تريدها:",
    "searching": "🔎 جاري البحث عن المنتجات...",
    "no_results": "❌ لم أجد منتجات تطابق بحثك",
    "product_saved": "✅ تم حفظ المنتج في المفضلة",
    "product_removed": "🗑️ تم إزالة المنتج من المفضلة",
    "error_occurred": "❌ حدث خطأ ما، الرجاء المحاولة لاحقاً",
}

# إعدادات لوحات المفاتيح
KEYBOARD_SETTINGS: Dict[str, Any] = {
    "page_size": 5,
    "max_buttons_per_row": 2,
    "cache_timeout": 300,
}

def validate_bot_config() -> bool:
    """
    التحقق من صحة إعدادات البوت
    
    Returns:
        bool: True إذا كانت الإعدادات صحيحة
    """
    try:
        if not config.BOT_TOKEN:
            logging.error("❌ BOT_TOKEN مفقود في الإعدادات")
            return False
        
        if not config.ADMIN_IDS:
            logging.warning("⚠️ لا توجد معرفات مشرفين محددة")
        
        logging.info("✅ إعدادات البوت صحيحة وجاهزة")
        return True
        
    except Exception as e:
        logging.error(f"❌ خطأ في التحقق من إعدادات البوت: {e}")
        return False

# التحقق من الإعدادات عند التحميل
if not validate_bot_config():
    raise RuntimeError("إعدادات البوت غير صحيحة. الرجاء التحقق من متغيرات البيئة.")
