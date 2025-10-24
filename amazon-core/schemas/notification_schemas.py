"""
نماذج بيانات الإشعارات
Pydantic schemas للتحقق من صحة بيانات الإشعارات
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    """أنواع الإشعارات"""
    PRICE_DROP = "price_drop"
    NEW_PRODUCT = "new_product"
    STOCK_ALERT = "stock_alert"
    SYSTEM_ALERT = "system_alert"
    PROMOTION = "promotion"

class NotificationStatus(str, Enum):
    """حالات الإشعار"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    READ = "read"

class NotificationBase(BaseModel):
    """النموذج الأساسي للإشعار"""
    title: str = Field(..., min_length=1, max_length=200, description="عنوان الإشعار")
    message: str = Field(..., min_length=1, max_length=1000, description="نص الإشعار")
    notification_type: NotificationType = Field(..., description="نوع الإشعار")
    data: Optional[Dict[str, Any]] = Field(None, description="بيانات إضافية")

class NotificationCreate(NotificationBase):
    """نموذج إنشاء إشعار جديد"""
    user_id: Optional[int] = Field(None, description="معرف المستخدم (إذا كان إشعار شخصي)")
    broadcast: bool = Field(False, description="هل هو إشعار جماعي")

class NotificationResponse(NotificationBase):
    """نموذج استجابة بيانات الإشعار"""
    id: int = Field(..., description="المعرف الفريد")
    user_id: Optional[int] = Field(None, description="معرف المستخدم")
    broadcast: bool = Field(..., description="هل هو إشعار جماعي")
    status: NotificationStatus = Field(..., description="حالة الإشعار")
    sent_at: Optional[datetime] = Field(None, description="وقت الإرسال")
    read_at: Optional[datetime] = Field(None, description="وقت القراءة")
    created_at: datetime = Field(..., description="وقت الإنشاء")
    
    class Config:
        """إعدادات Pydantic"""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class NotificationPreferences(BaseModel):
    """تفضيلات الإشعارات للمستخدم"""
    user_id: int
    price_drop_alerts: bool = Field(True, description="تنبيهات انخفاض الأسعار")
    new_product_alerts: bool = Field(True, description="تنبيهات المنتجات الجديدة")
    stock_alerts: bool = Field(True, description="تنبيهات التوفر")
    promotion_alerts: bool = Field(True, description="تنبيهات العروض")
    email_notifications: bool = Field(False, description="الإشعارات عبر البريد")
    telegram_notifications: bool = Field(True, description="الإشعارات عبر تليجرام")
    
    class Config:
        from_attributes = True
