"""
نماذج قاعدة البيانات المشتركة
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, JSON, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime

from .database import Base

class User(Base):
    """نموذج المستخدم"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    language_code = Column(String(10), default="ar")
    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)
    notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    rating = Column(DECIMAL(3, 2), nullable=True)
    review_count = Column(Integer, default=0)
    category = Column(String(200), nullable=True)
    availability = Column(String(100), nullable=True)
    prime_eligible = Column(Boolean, default=False)
    search_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Favorite(Base):
    """نموذج المفضلة"""
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    """نموذج الإشعار"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    data = Column(JSON, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
