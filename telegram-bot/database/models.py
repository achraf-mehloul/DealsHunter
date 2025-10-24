"""
نماذج قاعدة البيانات
تعريف الجداول والعلاقات في قاعدة البيانات
"""

import logging
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, 
    Boolean, DateTime, Text, ForeignKey, JSON, DECIMAL
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime

from amazon_core.utils.config import config

# قاعدة النماذج
Base = declarative_base()

# محرك قاعدة البيانات
engine = create_engine(**config.get_database_config())

# جلسة قاعدة البيانات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    
    # العلاقات
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"

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
    
    # العلاقات
    favorites = relationship("Favorite", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(asin={self.asin}, name={self.name}, price={self.price})>"
    
    @property
    def discount_percent(self):
        """حساب نسبة الخصم"""
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100, 2)
        return 0.0

class Favorite(Base):
    """نموذج المنتجات المفضلة"""
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    user = relationship("User", back_populates="favorites")
    product = relationship("Product", back_populates="favorites")
    
    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, product_id={self.product_id})>"

class Notification(Base):
    """نموذج الإشعارات"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for broadcast
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    data = Column(JSON, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification(user_id={self.user_id}, title={self.title})>"

class SearchHistory(Base):
    """سجل البحث"""
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query = Column(String(200), nullable=False)
    filters = Column(JSON, nullable=True)
    result_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    user = relationship("User")

class PriceHistory(Base):
    """سجل تغير الأسعار"""
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(10), default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    product = relationship("Product")

async def init_database():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("✅ تم تهيئة قاعدة البيانات بنجاح")
    except Exception as e:
        logging.error(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
        raise

def get_session():
    """الحصول على جلسة قاعدة البيانات"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
