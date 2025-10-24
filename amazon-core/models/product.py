"""
نموذج المنتج
تعريف جدول المنتجات في قاعدة البيانات
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, DECIMAL
from sqlalchemy.sql import func
from datetime import datetime

from .base import Base

class Product(Base):
    """نموذج المنتج"""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    asin = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(500), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    original_price = Column(DECIMAL(10, 2), nullable=True)
    currency = Column(String(10), default="USD")
    image_url = Column(Text, nullable=True)
    product_url = Column(Text, nullable=False)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, default=0)
    category = Column(String(200), nullable=True)
    availability = Column(String(100), nullable=True)
    prime_eligible = Column(Boolean, default=False)
    search_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product(asin={self.asin}, name={self.name}, price={self.price})>"
    
    @property
    def discount_percent(self):
        """حساب نسبة الخصم"""
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100, 2)
        return 0.0
    
    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            'id': self.id,
            'asin': self.asin,
            'name': self.name,
            'price': float(self.price) if self.price else None,
            'original_price': float(self.original_price) if self.original_price else None,
            'currency': self.currency,
            'image_url': self.image_url,
            'product_url': self.product_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'category': self.category,
            'availability': self.availability,
            'prime_eligible': self.prime_eligible,
            'discount_percent': self.discount_percent,
            'search_count': self.search_count,
            'favorite_count': self.favorite_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
