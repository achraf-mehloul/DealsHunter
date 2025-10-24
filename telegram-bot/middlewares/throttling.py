"""
Middleware الحد من الرسائل
منع الإساءة والرسائل المتكررة
"""

import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

class ThrottlingMiddleware(BaseMiddleware):
    """
    middleware للحد من تكرار الرسائل
    """
    
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.users = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        التحقق من الحد الزمني بين الرسائل
        """
        # تطبيق فقط على الرسائل
        if not isinstance(event, Message):
            return await handler(event, data)
        
        user_id = event.from_user.id
        current_time = time.time()
        
        # التحقق من آخر وقت للمستخدم
        if user_id in self.users:
            last_time = self.users[user_id]
            if current_time - last_time < self.rate_limit:
                # المستخدم أرسل رسالة بسرعة كبيرة
                await event.answer("⏳ الرجاء الانتظار قليلاً بين الرسائل.")
                return
        
        # تحديث وقت آخر رسالة
        self.users[user_id] = current_time
        
        # تنظيف المستخدمين القدامى (كل ساعة)
        if current_time % 3600 < 1:
            self._clean_old_users(current_time)
        
        return await handler(event, data)
    
    def _clean_old_users(self, current_time: float):
        """
        تنظيف المستخدمين الذين لم يرسلوا رسائل منذ أكثر من ساعة
        """
        self.users = {
            user_id: last_time 
            for user_id, last_time in self.users.items() 
            if current_time - last_time < 3600
        }
