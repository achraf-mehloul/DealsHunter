"""
نقطة الدخول الرئيسية للبوت
تشغيل البوت مع معالجة الأخطاء
"""

import asyncio
import logging
import signal
import sys
from contextlib import AsyncExitStack

from bot.main import main
from amazon_core.utils.logger import setup_logging

async def shutdown(signal_name: str, loop: asyncio.AbstractEventLoop):
    """
    إغلاق البوت بشكل آمن
    """
    logging.info(f"🛑 Received {signal_name}, shutting down...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def handle_exception(loop, context):
    """
    معالجة الاستثناءات غير المتوقعة
    """
    msg = context.get("exception", context["message"])
    logging.error(f"❌ Unexpected exception: {msg}")
    logging.info("👋 Shutting down...")

async def run_bot():
    """
    تشغيل البوت مع إدارة الموارد
    """
    async with AsyncExitStack() as stack:
        try:
            await main()
        except Exception as e:
            logging.critical(f"❌ Failed to start bot: {e}", exc_info=True)
            sys.exit(1)

if __name__ == "__main__":
    # إعداد التسجيل
    setup_logging()
    
    # إعداد معالجة الإشارات
    loop = asyncio.get_event_loop()
    signals = (signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s.__name__, loop))
        )
    
    # إعداد معالجة الاستثناءات
    loop.set_exception_handler(handle_exception)
    
    try:
        # تشغيل البوت
        loop.run_until_complete(run_bot())
    finally:
        loop.close()
        logging.info("👋 Bot shutdown complete.")
