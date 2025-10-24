"""
Handlers Package
حزمة معالجات الأوامر والرسائل
"""

from aiogram import Router

from .start import router as start_router
from .products import router as products_router
from .favorites import router as favorites_router
from .notifications import router as notifications_router
from .admin import router as admin_router

# جمع جميع الراوترات
routers = [
    start_router,
    products_router,
    favorites_router,
    notifications_router,
    admin_router,
]

__all__ = ['routers']
