"""
أدوات مساعدة للتطبيق
وظائف مساعدة عامة لمعالجة البيانات والتنسيق
"""

import re
import json
import asyncio
from typing import Any, Dict, List, Optional, Union
from decimal import Decimal
from datetime import datetime, timedelta

async def format_price(price: Union[float, int, str, Decimal], currency: str = "USD") -> str:
    """
    تنسيق السعر مع العملة بشكل مناسب
    
    Args:
        price: السعر
        currency: العملة (USD, EUR, etc.)
        
    Returns:
        السعر المنسق
    """
    try:
        if price is None:
            return "غير متوفر"
        
        # تحويل إلى Decimal للدقة
        price_decimal = Decimal(str(price))
        
        # تنسيق بناءً على العملة
        currency_symbols = {
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "SAR": "ر.س",
            "AED": "د.إ"
        }
        
        symbol = currency_symbols.get(currency, currency)
        
        # تنسيق الأرقام
        if price_decimal == price_decimal.to_integral():
            formatted_price = f"{price_decimal:.0f}"
        else:
            formatted_price = f"{price_decimal:.2f}"
        
        return f"{symbol}{formatted_price}"
        
    except (ValueError, TypeError) as e:
        return "غير متوفر"

def validate_email(email: str) -> bool:
    """
    التحقق من صحة البريد الإلكتروني
    
    Args:
        email: البريد الإلكتروني
        
    Returns:
        bool: True إذا كان البريد صحيح
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def safe_int(value: Any, default: int = 0) -> int:
    """
    تحويل آمن إلى عدد صحيح
    
    Args:
        value: القيمة المراد تحويلها
        default: القيمة الافتراضية في حالة الخطأ
        
    Returns:
        العدد الصحيح
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value: Any, default: float = 0.0) -> float:
    """
    تحويل آمن إلى عدد عشري
    
    Args:
        value: القيمة المراد تحويلها
        default: القيمة الافتراضية في حالة الخطأ
        
    Returns:
        العدد العشري
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    تقصير النص إذا تجاوز الطول المسموح
    
    Args:
        text: النص الأصلي
        max_length: الطول الأقصى
        suffix: النهاية التي تضاف للنص المقصوص
        
    Returns:
        النص المقصوص
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def parse_filters(filters_str: str) -> Dict[str, Any]:
    """
    تحويل نص الفلاتر إلى قاموس
    
    Args:
        filters_str: نص الفلاتر (JSON)
        
    Returns:
        قاموس الفلاتر
    """
    try:
        return json.loads(filters_str) if filters_str else {}
    except json.JSONDecodeError:
        return {}

def format_filters(filters_dict: Dict[str, Any]) -> str:
    """
    تحويل قاموس الفلاتر إلى نص JSON
    
    Args:
        filters_dict: قاموس الفلاتر
        
    Returns:
        نص الفلاتر (JSON)
    """
    return json.dumps(filters_dict, ensure_ascii=False)

async def send_notification(message: str, notification_type: str = "info") -> bool:
    """
    إرسال إشعار (يمكن توسيعه لإرسال إشعارات حقيقية)
    
    Args:
        message: نص الرسالة
        notification_type: نوع الإشعار (info, warning, error, success)
        
    Returns:
        bool: True إذا تم الإرسال بنجاح
    """
    # حالياً تطبع فقط، يمكن إضافة خدمات إشعارات حقيقية لاحقاً
    print(f"[{notification_type.upper()}] {message}")
    return True

def calculate_discount_percentage(original_price: float, current_price: float) -> float:
    """
    حساب نسبة الخصم
    
    Args:
        original_price: السعر الأصلي
        current_price: السعر الحالي
        
    Returns:
        نسبة الخصم
    """
    if not original_price or not current_price or original_price <= current_price:
        return 0.0
    
    discount = ((original_price - current_price) / original_price) * 100
    return round(discount, 2)

def is_valid_url(url: str) -> bool:
    """
    التحقق من صحة الرابط
    
    Args:
        url: الرابط المراد التحقق منه
        
    Returns:
        bool: True إذا كان الرابط صحيح
    """
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))

class Timer:
    """أداة قياس الوقت"""
    
    def __init__(self):
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start(self):
        """بدء القياس"""
        self.start_time = datetime.now()
        return self
    
    def stop(self) -> float:
        """
        إيقاف القياس وإرجاع المدة بالثواني
        
        Returns:
            المدة بالثواني
        """
        self.end_time = datetime.now()
        if self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def __enter__(self):
        """الدخول في context manager"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """الخروج من context manager"""
        self.stop()

# إنشاء instances عامة
timer = Timer()
