"""
حزمة الـ Middlewares
تجمع جميع الـ Middlewares
"""

from .auth import AuthMiddleware
from .throttling import ThrottlingMiddleware
from .analytics import AnalyticsMiddleware

def register_middlewares(dp):
    """
    تسجيل جميع الـ Middlewares في الـ Dispatcher
    """
    # ترتيب التسجيل مهم (من الأول إلى الأخير)
    dp.update.outer_middleware(ThrottlingMiddleware())
    dp.update.outer_middleware(AuthMiddleware())
    dp.update.outer_middleware(AnalyticsMiddleware())
