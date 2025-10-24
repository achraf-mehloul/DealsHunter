"""
نقاط نهاية التحليلات
الإحصائيات والتقارير
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List
from pydantic import BaseModel

from amazon_core.utils.config import config
from amazon_core.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)

router = APIRouter()

# نماذج البيانات
class DashboardStats(BaseModel):
    total_users: int
    active_users_today: int
    total_searches: int
    total_products: int
    total_notifications: int
    popular_searches: List[Dict[str, Any]]
    user_growth: List[Dict[str, Any]]

class UserAnalytics(BaseModel):
    period: str
    new_users: int
    active_users: int
    total_searches: int
    user_growth_rate: float

class ProductAnalytics(BaseModel):
    period: str
    total_products: int
    products_added: int
    total_searches: int
    popular_categories: List[Dict[str, Any]]

class SearchAnalytics(BaseModel):
    period: str
    total_searches: int
    unique_searches: int
    popular_queries: List[Dict[str, Any]]
    search_trends: List[Dict[str, Any]]

analytics_service = AnalyticsService()

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(user: dict = Depends()):
    """
    الحصول على إحصائيات لوحة التحكم
    """
    try:
        stats = await analytics_service.get_system_stats()
        
        return DashboardStats(
            total_users=stats.get('total_users', 0),
            active_users_today=stats.get('active_today', 0),
            total_searches=stats.get('total_searches', 0),
            total_products=stats.get('total_products', 0),
            total_notifications=stats.get('total_notifications_sent', 0),
            popular_searches=stats.get('popular_searches', []),
            user_growth=[
                {"date": "2024-01-01", "users": 100},
                {"date": "2024-01-02", "users": 120},
                {"date": "2024-01-03", "users": 150}
            ]
        )
        
    except Exception as e:
        logger.error(f"Get dashboard stats error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب إحصائيات اللوحة")

@router.get("/users", response_model=UserAnalytics)
async def get_user_analytics(
    period: str = Query("7d", regex="^(today|yesterday|7d|30d|90d|year)$"),
    user: dict = Depends()
):
    """
    الحصول على تحليلات المستخدمين
    """
    try:
        # TODO: جلب تحليلات المستخدمين من قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        return UserAnalytics(
            period=period,
            new_users=25,
            active_users=150,
            total_searches=1200,
            user_growth_rate=15.5
        )
        
    except Exception as e:
        logger.error(f"Get user analytics error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب تحليلات المستخدمين")

@router.get("/products", response_model=ProductAnalytics)
async def get_product_analytics(
    period: str = Query("7d", regex="^(today|yesterday|7d|30d|90d|year)$"),
    user: dict = Depends()
):
    """
    الحصول على تحليلات المنتجات
    """
    try:
        # TODO: جلب تحليلات المنتجات من قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        return ProductAnalytics(
            period=period,
            total_products=5000,
            products_added=50,
            total_searches=15000,
            popular_categories=[
                {"category": "Electronics", "count": 1200},
                {"category": "Books", "count": 800},
                {"category": "Home", "count": 600}
            ]
        )
        
    except Exception as e:
        logger.error(f"Get product analytics error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب تحليلات المنتجات")

@router.get("/searches", response_model=SearchAnalytics)
async def get_search_analytics(
    period: str = Query("7d", regex="^(today|yesterday|7d|30d|90d|year)$"),
    user: dict = Depends()
):
    """
    الحصول على تحليلات البحث
    """
    try:
        # TODO: جلب تحليلات البحث من قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        return SearchAnalytics(
            period=period,
            total_searches=15000,
            unique_searches=4500,
            popular_queries=[
                {"query": "iphone", "count": 150},
                {"query": "laptop", "count": 120},
                {"query": "books", "count": 100}
            ],
            search_trends=[
                {"date": "2024-01-01", "searches": 450},
                {"date": "2024-01-02", "searches": 520},
                {"date": "2024-01-03", "searches": 480}
            ]
        )
        
    except Exception as e:
        logger.error(f"Get search analytics error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب تحليلات البحث")

@router.get("/activity")
async def get_daily_activity(
    days: int = Query(7, ge=1, le=90),
    user: dict = Depends()
):
    """
    الحصول على النشاط اليومي
    """
    try:
        activity = await analytics_service.get_daily_activity(days)
        return {"activity": activity}
        
    except Exception as e:
        logger.error(f"Get daily activity error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب النشاط اليومي")
