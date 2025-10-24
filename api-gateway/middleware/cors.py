"""
إعدادات CORS
التكوين لمشاركة الموارد بين المصادر
"""

from amazon_core.utils.config import config

def setup_cors():
    """
    إعداد إعدادات CORS
    
    Returns:
        dict: إعدادات CORS
    """
    # في بيئة التطوير، السماح بجميع المصادر
    if config.DEBUG:
        return {
            "allow_origins": ["*"],
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }
    
    # في بيئة الإنتاج، السماح بمصادر محددة فقط
    return {
        "allow_origins": [
            "https://youradmin.com",
            "https://admin.amazon-bot.com",
        ],
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": [
            "Authorization",
            "Content-Type",
            "X-Requested-With",
        ],
    }
