"""
الملف الرئيسي لتشغيل بوت تليجرام
المسؤول عن تهيئة وإدارة جميع مكونات البوت
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from amazon_core.utils.config import config
from amazon_core.utils.logger import setup_logging
from telegram_bot.handlers import routers
from telegram_bot.middlewares import register_middlewares
from telegram_bot.database import init_database

# إعداد النظام logging
setup_logging()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def bot_lifespan(dp: Dispatcher):
    """
    إدارة دورة حياة البوت
    - تنفيذ العمليات عند البدء
    - تنظيف الموارد عند الإيقاف
    """
    # عمليات البدء
    logger.info("🚀 بدء تشغيل بوت أمازون...")
    
    # تهيئة قاعدة البيانات
    await init_database()
    logger.info("✅ قاعدة البيانات جاهزة")
    
    try:
        yield
    finally:
        # عمليات التنظيف
        logger.info("🛑 إيقاف بوت أمازون...")
        # تنظيف الموارد هنا

async def main():
    """الدالة الرئيسية لتشغيل البوت"""
    
    # 🔹 تهيئة البوت مع الإعدادات الافتراضية
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        )
    )
    
    # 🔹 إعداد التخزين مع Redis
    storage = RedisStorage.from_url(config.REDIS_URL)
    
    # 🔹 إنشاء Dispatcher مع إدارة دورة الحياة
    dp = Dispatcher(storage=storage, lifespan=bot_lifespan)
    
    # 🔹 تسجيل Middlewares
    register_middlewares(dp)
    
    # 🔹 تسجيل جميع الراوترات
    for router in routers:
        dp.include_router(router)
        logger.debug(f"✅ تم تسجيل الراوتر: {router.name}")
    
    # 🔹 بدء استقبال التحديثات
    logger.info("✅ البوت جاهز لاستقبال الرسائل...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        logger.critical(f"❌ خطأ غير متوقع: {e}", exc_info=True)
        raise
