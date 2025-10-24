"""
Amazon Core Package
النواة الأساسية لمشروع بوت أمازون
"""

__version__ = "1.0.0"
__author__ = "Amazon Bot Team"
__description__ = "Core functionality for Amazon Telegram Bot"

from .utils.config import config
from .utils.logger import setup_logging

# إعداد اللوغرات الافتراضي
setup_logging()

__all__ = ['config', 'setup_logging']
