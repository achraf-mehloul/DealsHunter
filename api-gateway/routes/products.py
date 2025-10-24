"""
نقاط نهاية المنتجات
البحث عن المنتجات وعرض الإحصائيات
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from amazon_core.utils.config import config
from amazon_core.services.amazon_service import AmazonService
from amazon_core.schemas.product_schemas import ProductSearch, ProductResponse

logger = logging.getLogger(__name__)

router = APIRouter()

# نماذج البيانات
class ProductSearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    page: int = 1
    page_size: int = 10

class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class ProductAnalytics(BaseModel):
    total_products: int
    total_searches: int
    popular_categories: List[Dict[str, Any]]
    top_products: List[Dict[str, Any]]
    search_trends: List[Dict[str, Any]]

@router.post("/search", response_model=ProductListResponse)
async def search_products(
    search_request: ProductSearchRequest,
    user: dict = Depends()
):
    """
    البحث عن منتجات في أمازون
    """
    try:
        amazon_service = AmazonService()
        
        # تحويل الطلب إلى نموذج البحث
        search_model = ProductSearch(
            query=search_request.query,
            filters=search_request.filters,
            page=search_request.page,
            page_size=search_request.page_size
        )
        
        # البحث عن المنتجات
        products = await amazon_service.search_products(search_model)
        
        # حساب الإحصائيات
        total = len(products)
        total_pages = (total + search_request.page_size - 1) // search_request.page_size
        has_next = search_request.page < total_pages
        has_previous = search_request.page > 1
        
        return ProductListResponse(
            products=products,
            total=total,
            page=search_request.page,
            page_size=search_request.page_size,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous
        )
        
    except Exception as e:
        logger.error(f"Product search error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء البحث عن المنتجات")

@router.get("/", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    user: dict = Depends()
):
    """
    الحصول على قائمة المنتجات
    """
    try:
        # TODO: جلب المنتجات من قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        products_data = [
            ProductResponse(
                id=1,
                asin="B08N5WRWNW",
                name="Amazon Echo Dot (4th Gen)",
                price=49.99,
                original_price=59.99,
                currency="USD",
                image_url="https://images-na.ssl-images-amazon.com/images/I/714Rq4k05UL._SL1000_.jpg",
                product_url="https://amazon.com/dp/B08N5WRWNW",
                rating=4.7,
                review_count=25000,
                category="Electronics",
                availability="In Stock",
                prime_eligible=True,
                discount_percent=16.67,
                is_favorite=False,
                search_count=150,
                favorite_count=45,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z"
            )
        ]
        
        return ProductListResponse(
            products=products_data,
            total=1,
            page=page,
            page_size=page_size,
            total_pages=1,
            has_next=False,
            has_previous=False
        )
        
    except Exception as e:
        logger.error(f"Get products error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب المنتجات")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, user: dict = Depends()):
    """
    الحصول على بيانات منتج معين
    """
    try:
        # TODO: جلب المنتج من قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        if product_id == 1:
            return ProductResponse(
                id=1,
                asin="B08N5WRWNW",
                name="Amazon Echo Dot (4th Gen)",
                price=49.99,
                original_price=59.99,
                currency="USD",
                image_url="https://images-na.ssl-images-amazon.com/images/I/714Rq4k05UL._SL1000_.jpg",
                product_url="https://amazon.com/dp/B08N5WRWNW",
                rating=4.7,
                review_count=25000,
                category="Electronics",
                availability="In Stock",
                prime_eligible=True,
                discount_percent=16.67,
                is_favorite=False,
                search_count=150,
                favorite_count=45,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z"
            )
        else:
            raise HTTPException(status_code=404, detail="المنتج غير موجود")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get product error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب بيانات المنتج")

@router.get("/analytics", response_model=ProductAnalytics)
async def get_product_analytics(user: dict = Depends()):
    """
    الحصول على إحصائيات المنتجات
    """
    try:
        # TODO: جلب الإحصائيات من قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        return ProductAnalytics(
            total_products=5000,
            total_searches=15000,
            popular_categories=[
                {"category": "Electronics", "count": 1200},
                {"category": "Books", "count": 800},
                {"category": "Home", "count": 600}
            ],
            top_products=[
                {"name": "Amazon Echo Dot", "searches": 150},
                {"name": "iPhone Case", "searches": 120},
                {"name": "Programming Books", "searches": 100}
            ],
            search_trends=[
                {"date": "2024-01-01", "searches": 45},
                {"date": "2024-01-02", "searches": 52},
                {"date": "2024-01-03", "searches": 48}
            ]
        )
        
    except Exception as e:
        logger.error(f"Get product analytics error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب إحصائيات المنتجات")

@router.get("/popular", response_model=List[ProductResponse])
async def get_popular_products(
    limit: int = Query(10, ge=1, le=50),
    user: dict = Depends()
):
    """
    الحصول على المنتجات الأكثر شيوعاً
    """
    try:
        # TODO: جلب المنتجات الشائعة من قاعدة البيانات
        # هذا تنفيذ مؤقت
        
        return [
            ProductResponse(
                id=1,
                asin="B08N5WRWNW",
                name="Amazon Echo Dot (4th Gen)",
                price=49.99,
                original_price=59.99,
                currency="USD",
                image_url="https://images-na.ssl-images-amazon.com/images/I/714Rq4k05UL._SL1000_.jpg",
                product_url="https://amazon.com/dp/B08N5WRWNW",
                rating=4.7,
                review_count=25000,
                category="Electronics",
                availability="In Stock",
                prime_eligible=True,
                discount_percent=16.67,
                is_favorite=False,
                search_count=150,
                favorite_count=45,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z"
            )
        ]
        
    except Exception as e:
        logger.error(f"Get popular products error: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء جلب المنتجات الشائعة")
