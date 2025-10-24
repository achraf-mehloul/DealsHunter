"""
نماذج بيانات المنتج
Pydantic schemas للتحقق من صحة بيانات المنتج
"""

from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    """النموذج الأساسي للمنتج"""
    name: str = Field(..., min_length=1, max_length=500, description="اسم المنتج")
    asin: str = Field(..., min_length=10, max_length=10, description="ASIN المنتج")
    price: Decimal = Field(..., ge=0, description="السعر الحالي")
    original_price: Optional[Decimal] = Field(None, ge=0, description="السعر الأصلي")
    currency: str = Field("USD", description="العملة")
    image_url: Optional[HttpUrl] = Field(None, description="رابط الصورة")
    product_url: HttpUrl = Field(..., description="رابط المنتج في أمازون")
    rating: Optional[float] = Field(None, ge=0, le=5, description="التقييم")
    review_count: Optional[int] = Field(None, ge=0, description="عدد التقييمات")
    category: Optional[str] = Field(None, description="الفئة")
    availability: Optional[str] = Field(None, description="التوفر")
    prime_eligible: bool = Field(False, description="هل المنتج مؤهل لـ Prime")

class ProductSearchFilters(BaseModel):
    """فلاتر البحث عن المنتجات"""
    min_price: Optional[Decimal] = Field(None, ge=0, description="أقل سعر")
    max_price: Optional[Decimal] = Field(None, ge=0, description="أعلى سعر")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="أقل تقييم")
    category: Optional[str] = Field(None, description="الفئة")
    prime_only: bool = Field(False, description="المنتجات المؤهلة لـ Prime فقط")
    has_discount: bool = Field(False, description="المنتجات المخفضة فقط")
    
    @validator('max_price')
    def validate_price_range(cls, v, values):
        """التحقق من نطاق السعر"""
        if 'min_price' in values and values['min_price'] and v:
            if v < values['min_price']:
                raise ValueError('السعر الأقصى يجب أن يكون أكبر من أو يساوي السعر الأدنى')
        return v

class ProductSearch(BaseModel):
    """نموذج البحث عن المنتجات"""
    query: str = Field(..., min_length=1, max_length=200, description="كلمة البحث")
    filters: Optional[ProductSearchFilters] = Field(None, description="فلاتر البحث")
    page: int = Field(1, ge=1, description="رقم الصفحة")
    page_size: int = Field(10, ge=1, le=50, description="حجم الصفحة")

class ProductResponse(ProductBase):
    """نموذج استجابة بيانات المنتج"""
    id: int = Field(..., description="المعرف الفريد في قاعدة البيانات")
    discount_percent: Optional[float] = Field(None, description="نسبة الخصم")
    is_favorite: bool = Field(False, description="هل تم إضافته للمفضلة")
    search_count: int = Field(0, description="عدد مرات البحث عنه")
    favorite_count: int = Field(0, description="عدد الإضافات للمفضلة")
    created_at: datetime = Field(..., description="وقت الإضافة")
    updated_at: datetime = Field(..., description="وقت آخر تحديث")
    
    class Config:
        """إعدادات Pydantic"""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class ProductListResponse(BaseModel):
    """نموذج استجابة قائمة المنتجات"""
    products: List[ProductResponse] = Field(..., description="قائمة المنتجات")
    total_count: int = Field(..., description="إجمالي عدد المنتجات")
    current_page: int = Field(..., description="الصفحة الحالية")
    total_pages: int = Field(..., description="إجمالي عدد الصفحات")
    has_next: bool = Field(..., description="هل توجد صفحة تالية")
    has_previous: bool = Field(..., description="هل توجد صفحة سابقة")

class PriceHistory(BaseModel):
    """سجل تغير الأسعار"""
    product_id: int
    price: Decimal
    currency: str
    timestamp: datetime
    
    class Config:
        from_attributes = True
