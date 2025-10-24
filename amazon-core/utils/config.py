"""
إعدادات التطبيق المركزية
المسؤول عن تحميل وإدارة متغيرات البيئة والإعدادات
"""

import os
import logging
from typing import Optional, List
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class Config:
    """فئة الإعدادات المركزية للتطبيق"""
    
    # 🔹 إعدادات تليجرام بوت
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: List[int] = list(map(int, os.getenv("ADMIN_IDS", "123456789").split(",")))
    
    # 🔹 إعدادات Amazon API
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_ASSOCIATE_TAG: str = os.getenv("AWS_ASSOCIATE_TAG", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    # 🔹 إعدادات قاعدة البيانات
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///amazon_bot.db")
    
    # 🔹 إعدادات Redis للتخزين المؤقت
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    
    # 🔹 إعدادات الخادم
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # 🔹 إعدادات التطبيق
    MAX_PRODUCTS_PER_PAGE: int = int(os.getenv("MAX_PRODUCTS_PER_PAGE", "10"))
    CACHE_TIMEOUT: int = int(os.getenv("CACHE_TIMEOUT", "300"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    def validate_config(self) -> bool:
        """
        التحقق من صحة الإعدادات المطلوبة
        
        Returns:
            bool: True إذا كانت جميع الإعدادات صحيحة
        Raises:
            ValueError: إذا كانت هناك إعدادات مفقودة
        """
        required_settings = {
            "BOT_TOKEN": self.BOT_TOKEN,
            "AWS_ACCESS_KEY_ID": self.AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": self.AWS_SECRET_ACCESS_KEY,
            "AWS_ASSOCIATE_TAG": self.AWS_ASSOCIATE_TAG,
        }
        
        missing_settings = []
        for key, value in required_settings.items():
            if not value:
                missing_settings.append(key)
        
        if missing_settings:
            error_msg = f"❌ الإعدادات المطلوبة مفقودة: {', '.join(missing_settings)}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        logging.info("✅ جميع الإعدادات صحيحة وجاهزة للتشغيل")
        return True
    
    def get_database_config(self) -> dict:
        """إرجاع إعدادات قاعدة البيانات"""
        return {
            "url": self.DATABASE_URL,
            "echo": self.DEBUG,
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "connect_args": {"check_same_thread": False} if "sqlite" in self.DATABASE_URL else {}
        }
    
    def get_redis_config(self) -> dict:
        """إرجاع إعدادات Redis"""
        redis_config = {
            "url": self.REDIS_URL,
            "encoding": "utf-8",
            "decode_responses": True,
        }
        
        if self.REDIS_PASSWORD:
            redis_config["password"] = self.REDIS_PASSWORD
            
        return redis_config
    
    def __repr__(self) -> str:
        """تمثيل نصي للإعدادات (بدون معلومات حساسة)"""
        return f"Config(DEBUG={self.DEBUG}, LOG_LEVEL='{self.LOG_LEVEL}')"

# إنشاء نسخة عالمية من الإعدادات
config = Config()

# التحقق من الإعدادات عند التحميل
try:
    config.validate_config()
except ValueError as e:
    logging.warning(f"تحذير في الإعدادات: {e}")