"""
بوابة API الرئيسية
تطبيق FastAPI الرئيسي للتطبيق
"""

import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from amazon_core.utils.config import config
from amazon_core.utils.logger import setup_logging

from middleware.auth import AuthMiddleware
from middleware.rate_limit import RateLimitMiddleware
from middleware.cors import setup_cors

from routes import auth, users, products, notifications, analytics

# إعداد النظام logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    إدارة دورة حياة التطبيق
    """
    # بدء التطبيق
    logger.info("🚀 Starting Amazon Bot API Gateway...")
    
    # تهيئة الخدمات
    await initialize_services()
    
    yield
    
    # إيقاف التطبيق
    logger.info("🛑 Stopping Amazon Bot API Gateway...")
    await shutdown_services()

async def initialize_services():
    """تهيئة الخدمات"""
    try:
        # TODO: تهيئة اتصالات قاعدة البيانات
        # TODO: تهيئة خدمة التخزين المؤقت
        logger.info("✅ Services initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        raise

async def shutdown_services():
    """إيقاف الخدمات"""
    try:
        # TODO: إغلاق اتصالات قاعدة البيانات
        # TODO: إغلاق خدمة التخزين المؤقت
        logger.info("✅ Services shutdown successfully")
    except Exception as e:
        logger.error(f"❌ Error during services shutdown: {e}")

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Amazon Bot API Gateway",
    description="بوابة API لنظام بوت أمازون",
    version="1.0.0",
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None,
    lifespan=lifespan
)

# إعداد الـ Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=setup_cors()["allow_origins"],
    allow_credentials=True,
    allow_methods=setup_cors()["allow_methods"],
    allow_headers=setup_cors()["allow_headers"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(AuthMiddleware)
app.add_middleware(RateLimitMiddleware)

# تسجيل routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
async def root():
    """
    نقطة النهاية الرئيسية
    """
    return {
        "message": "مرحباً بك في بوابة API لنظام بوت أمازون",
        "version": "1.0.0",
        "status": "يعمل",
        "docs": "/docs" if config.DEBUG else "غير متاحة في production"
    }

@app.get("/health")
async def health_check():
    """
    فحص صحة التطبيق
    """
    try:
        # TODO: فحص اتصال قاعدة البيانات
        # TODO: فحص خدمة التخزين المؤقت
        
        return {
            "status": "healthy",
            "database": "connected",  # TODO: التحقق الفعلي
            "cache": "connected",     # TODO: التحقق الفعلي
            "timestamp": "2024-01-01T00:00:00Z"  # TODO: وقت حقيقي
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/api/status")
async def api_status():
    """
    حالة API
    """
    return {
        "api": "running",
        "version": "1.0.0",
        "environment": "development" if config.DEBUG else "production",
        "features": {
            "authentication": True,
            "users_management": True,
            "products_search": True,
            "notifications": True,
            "analytics": True
        }
    }

# معالجة الأخطاء
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "المورد غير موجود"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "حدث خطأ داخلي في الخادم"}
    )

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower()
    )
