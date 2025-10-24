"""
Middleware المصادقة
التحقق من صحة التوكنات والصلاحيات
"""

import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from amazon_core.utils.config import config

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """
    middleware للمصادقة والتحقق من الصلاحيات
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.public_paths = {
            '/',
            '/health',
            '/docs',
            '/redoc',
            '/openapi.json',
            '/api/auth/login',
            '/api/auth/refresh'
        }
    
    async def dispatch(self, request: Request, call_next):
        """
        معالجة كل طلب وارد
        """
        # تخطي المصادقة للمسارات العامة
        if request.url.path in self.public_paths:
            return await call_next(request)
        
        try:
            # التحقق من وجود token
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise HTTPException(status_code=401, detail="مطلوب مصادقة")
            
            # استخراج token
            if not auth_header.startswith('Bearer '):
                raise HTTPException(status_code=401, detail="صيغة token غير صحيحة")
            
            token = auth_header[7:]  # إزالة 'Bearer '
            
            # التحقق من صحة token
            user = await self.verify_token(token)
            if not user:
                raise HTTPException(status_code=401, detail="Token غير صالح")
            
            # إضافة بيانات المستخدم للطلب
            request.state.user = user
            
            # التحقق من الصلاحيات للمسارات المحمية
            if await self.requires_admin(request.url.path):
                if not user.get('is_admin'):
                    raise HTTPException(status_code=403, detail="غير مسموح بالوصول")
            
            return await call_next(request)
            
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"message": e.detail}
            )
        except Exception as e:
            logger.error(f"Auth middleware error: {e}")
            return JSONResponse(
                status_code=500,
                content={"message": "خطأ في المصادقة"}
            )
    
    async def verify_token(self, token: str) -> dict:
        """
        التحقق من صحة الـ token
        
        Args:
            token: الـ token المراد التحقق منه
            
        Returns:
            dict: بيانات المستخدم إذا كان الـ token صالح
        """
        try:
            # TODO: تنفيذ التحقق الفعلي من الـ token
            # هذا تنفيذ مؤقت للاختبار
            
            if token == "valid_admin_token":
                return {
                    "id": 1,
                    "email": "admin@amazonbot.com",
                    "is_admin": True,
                    "permissions": ["read", "write", "delete", "manage_users"]
                }
            elif token == "valid_user_token":
                return {
                    "id": 2,
                    "email": "user@example.com", 
                    "is_admin": False,
                    "permissions": ["read"]
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None
    
    async def requires_admin(self, path: str) -> bool:
        """
        التحقق إذا كان المسار يتطلب صلاحيات مشرف
        
        Args:
            path: المسار المطلوب
            
        Returns:
            bool: True إذا كان يتطلب صلاحيات مشرف
        """
        admin_paths = [
            '/api/users',
            '/api/analytics',
            '/api/settings',
            '/api/notifications/broadcast'
        ]
        
        return any(path.startswith(admin_path) for admin_path in admin_paths)
