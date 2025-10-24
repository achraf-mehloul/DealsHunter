"""
إعداد وتكوين الـ Dispatcher الرئيسي
تجمع جميع المكونات وتكوينها
"""

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from amazon_core.utils.config import config
from telegram_bot.handlers import routers
from telegram_bot.middlewares import register_middlewares

def setup_dispatcher() -> Dispatcher:
    """
    إعداد وتكوين الـ Dispatcher
    
    Returns:
        Dispatcher: كائن الـ Dispatcher المكون
    """
    # إعداد التخزين
    storage = RedisStorage.from_url(config.REDIS_URL)
    
    # إنشاء Dispatcher
    dp = Dispatcher(storage=storage)
    
    # تسجيل الـ Middlewares
    register_middlewares(dp)
    
    # تسجيل جميع الراوترات
    for router in routers:
        dp.include_router(router)
    
    return dp

# إنشاء Dispatcher عالمي
dp = setup_dispatcher()
