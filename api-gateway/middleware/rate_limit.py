"""
Middleware الحد من الطلبات
منع الإساءة والهجمات
"""

import time
from collections import defaultdict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from amazon_core.utils.config import config

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    middleware للحد من عدد الطلبات
    """
    
    def __init__(self, app, max_requests: int = 100, window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        """
        معالجة كل طلب وارد
        """
        # تخطي الحد للمسارات العامة
        if request.url.path in ['/', '/health', '/docs', '/redoc']:
            return await call_next(request)
        
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # تنظيف الطلبات القديمة
        self.clean_old_requests(client_ip, current_time)
        
        # التحقق من تجاوز الحد
        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={
                    "message": "تم تجاوز الحد المسموح للطلبات",
                    "retry_after": self.window
                }
            )
        
        # تسجيل الطلب الحالي
        self.requests[client_ip].append(current_time)
        
        return await call_next(request)
    
    def get_client_ip(self, request: Request) -> str:
        """
        الحصول على IP العميل
        
        Args:
            request: كائن الطلب
            
        Returns:
            str: IP العميل
        """
        # المحاولة من X-Forwarded-For (خلف proxy)
        if "x-forwarded-for" in request.headers:
            return request.headers["x-forwarded-for"].split(",")[0].strip()
        
        # المحاولة من X-Real-IP
        if "x-real-ip" in request.headers:
            return request.headers["x-real-ip"]
        
        # الاستخدام المباشر
        return request.client.host
    
    def clean_old_requests(self, client_ip: str, current_time: float):
        """
        تنظيف الطلبات القديمة
        
        Args:
            client_ip: IP العميل
            current_time: الوقت الحالي
        """
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < self.window
            ]
