"""
Telegram Bot Package
حزمة بوت تليجرام الرئيسية
"""

__version__ = "1.0.0"
__author__ = "Amazon Bot Team"

from .bot.main import main
from .handlers import routers

__all__ = ['main', 'routers']
