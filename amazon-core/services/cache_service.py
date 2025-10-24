"""
خدمة التخزين المؤقت
إدارة التخزين المؤقت باستخدام Redis
"""

import json
import logging
from typing import Any, Optional, Union
from datetime import timedelta

import redis.asyncio as redis

from amazon_core.utils.config import config

class CacheService:
    """خدمة للتخزين المؤقت باستخدام Redis"""
    
    def __init__(self):
        self.redis_client = None
        self.is_connected = False
        
    async def connect(self):
        """الاتصال بـ Redis"""
        try:
            self.redis_client = redis.from_url(
                config.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
            self.is_connected = True
            logging.info("✅ Connected to Redis successfully")
        except Exception as e:
            logging.error(f"❌ Failed to connect to Redis: {e}")
            self.is_connected = False
    
    async def disconnect(self):
        """قطع الاتصال بـ Redis"""
        if self.redis_client:
            await self.redis_client.close()
            self.is_connected = False
    
    async def get(self, key: str) -> Optional[Any]:
        """
        الحصول على قيمة من التخزين المؤقت
        
        Args:
            key: المفتاح
            
        Returns:
            Optional[Any]: القيمة المخزنة
        """
        if not self.is_connected:
            return None
            
        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logging.error(f"Error getting cache key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """
        تخزين قيمة في التخزين المؤقت
        
        Args:
            key: المفتاح
            value: القيمة
            expire: وقت الانتهاء بالثواني
            
        Returns:
            bool: True إذا تم التخزين بنجاح
        """
        if not self.is_connected:
            return False
            
        try:
            serialized_value = json.dumps(value, default=str)
            await self.redis_client.setex(key, expire, serialized_value)
            return True
        except Exception as e:
            logging.error(f"Error setting cache key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        حذف قيمة من التخزين المؤقت
        
        Args:
            key: المفتاح
            
        Returns:
            bool: True إذا تم الحذف بنجاح
        """
        if not self.is_connected:
            return False
            
        try:
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            logging.error(f"Error deleting cache key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """
        التحقق من وجود مفتاح في التخزين المؤقت
        
        Args:
            key: المفتاح
            
        Returns:
            bool: True إذا كان المفتاح موجوداً
        """
        if not self.is_connected:
            return False
            
        try:
            return await self.redis_client.exists(key) > 0
        except Exception as e:
            logging.error(f"Error checking cache key {key}: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> bool:
        """
        مسح جميع المفاتيح التي تطابق النمط
        
        Args:
            pattern: نمط المفاتيح
            
        Returns:
            bool: True إذا تم المسح بنجاح
        """
        if not self.is_connected:
            return False
            
        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                await self.redis_client.delete(*keys)
            return True
        except Exception as e:
            logging.error(f"Error clearing cache pattern {pattern}: {e}")
            return False

# إنشاء نسخة عامة من الخدمة
cache_service = CacheService()
