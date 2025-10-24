"""
نماذج بيانات المستخدم
Pydantic schemas للتحقق من صحة بيانات المستخدم
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """أدوار المستخدمين"""
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserBase(BaseModel):
    """النموذج الأساسي للمستخدم"""
    telegram_id: int = Field(..., description="معرف تليجرام الفريد")
    username: Optional[str] = Field(None, description="اسم المستخدم في تليجرام")
    first_name: str = Field(..., min_length=1, max_length=100, description="الاسم الأول")
    last_name: Optional[str] = Field(None, max_length=100, description="الاسم الأخير")
    language_code: Optional[str] = Field("ar", description="لغة المستخدم")

class UserCreate(UserBase):
    """نموذج إنشاء مستخدم جديد"""
    role: UserRole = Field(UserRole.USER, description="دور المستخدم")
    
    @validator('telegram_id')
    def validate_telegram_id(cls, v):
        """التحقق من صحة معرف تليجرام"""
        if v <= 0:
            raise ValueError('معرف تليجرام يجب أن يكون رقم موجب')
        return v

class UserUpdate(BaseModel):
    """نموذج تحديث بيانات المستخدم"""
    username: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    language_code: Optional[str] = Field(None, max_length=10)
    is_active: Optional[bool] = Field(True)
    notifications_enabled: Optional[bool] = Field(True)

class UserResponse(UserBase):
    """نموذج استجابة بيانات المستخدم"""
    id: int = Field(..., description="المعرف الفريد في قاعدة البيانات")
    role: UserRole = Field(..., description="دور المستخدم")
    is_active: bool = Field(True, description="حالة المستخدم")
    notifications_enabled: bool = Field(True, description="تفعيل الإشعارات")
    created_at: datetime = Field(..., description="وقت الإنشاء")
    updated_at: datetime = Field(..., description="وقت آخر تحديث")
    
    class Config:
        """إعدادات Pydantic"""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserStats(BaseModel):
    """إحصائيات المستخدم"""
    user_id: int
    total_searches: int = Field(0, description="عدد عمليات البحث")
    total_favorites: int = Field(0, description="عدد المنتجات المفضلة")
    total_notifications: int = Field(0, description="عدد الإشعارات المستلمة")
    last_active: Optional[datetime] = Field(None, description="آخر نشاط")
    
    class Config:
        from_attributes = True
