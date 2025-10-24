"""
نظام التسجيل (Logging) المركزي
إعداد وتكوين نظام التسجيل للتطبيق
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from .config import config

def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    enable_file_logging: bool = True
) -> logging.Logger:
    """
    إعداد وتكوين نظام التسجيل
    
    Args:
        log_level: مستوى التسجيل (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: مسار ملف التسجيل
        enable_file_logging: تفعيل التسجيل في الملف
        
    Returns:
        كائن التسجيل الرئيسي
    """
    # تحديد مستوى التسجيل
    level = getattr(logging, log_level or config.LOG_LEVEL.upper(), logging.INFO)
    
    # إنشاء مجلد اللوغات إذا لم يكن موجوداً
    if enable_file_logging:
        log_path = Path(log_file or "logs/amazon_bot.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # تكوين نظام التسجيل
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            # Handler للملف
            *([logging.FileHandler(log_path, encoding='utf-8')] if enable_file_logging else []),
            # Handler للكونسول
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # إعداد تسجيل خاص لـ aiogram (تقليل الضوضاء)
    aiogram_logger = logging.getLogger('aiogram')
    aiogram_logger.setLevel(logging.WARNING)
    
    # إعداد تسجيل خاص لـ aiohttp (تقليل الضوضاء)
    aiohttp_logger = logging.getLogger('aiohttp')
    aiohttp_logger.setLevel(logging.WARNING)
    
    # إنشاء وتسجيل logger الرئيسي
    logger = logging.getLogger(__name__)
    logger.info(f"✅ نظام التسجيل جاهز - المستوى: {logging.getLevelName(level)}")
    
    if enable_file_logging:
        logger.info(f"📁 يتم التسجيل في الملف: {log_path}")
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    الحصول على كائن تسجيل باسم معين
    
    Args:
        name: اسم الموديل أو المكون
        
    Returns:
        كائن التسجيل
    """
    return logging.getLogger(name)

# إنشاء logger عام
logger = get_logger(__name__)