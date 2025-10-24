"""
لوحات مفاتيح التقسيم
Inline keyboards للتنقل بين الصفحات
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional

def get_pagination_keyboard(
    current_page: int,
    total_pages: int,
    callback_prefix: str = "page",
    include_navigation: bool = True
) -> InlineKeyboardMarkup:
    """
    إنشاء لوحة مفاتيح للتقسيم الصفحي
    
    Args:
        current_page: الصفحة الحالية
        total_pages: إجمالي الصفحات
        callback_prefix: بادئة الـ callback
        include_navigation: تضمين أزرار التنقل
        
    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح
    """
    buttons = []
    
    if include_navigation:
        # أزرار التنقل
        nav_buttons = []
        
        if current_page > 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="⏪ الأولى",
                    callback_data=f"{callback_prefix}_1"
                )
            )
            nav_buttons.append(
                InlineKeyboardButton(
                    text="◀️ السابقة", 
                    callback_data=f"{callback_prefix}_{current_page - 1}"
                )
            )
        
        nav_buttons.append(
            InlineKeyboardButton(
                text=f"📄 {current_page}/{total_pages}",
                callback_data="current_page"
            )
        )
        
        if current_page < total_pages:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="التالية ▶️",
                    callback_data=f"{callback_prefix}_{current_page + 1}"
                )
            )
            nav_buttons.append(
                InlineKeyboardButton(
                    text="الأخيرة ⏩",
                    callback_data=f"{callback_prefix}_{total_pages}"
                )
            )
        
        buttons.append(nav_buttons)
    
    # أزرار الصفحات السريعة (للعرض فقط إذا كان العدد معقول)
    if total_pages <= 10:
        page_buttons = []
        start_page = max(1, current_page - 2)
        end_page = min(total_pages, current_page + 2)
        
        for page_num in range(start_page, end_page + 1):
            if page_num == current_page:
                page_buttons.append(
                    InlineKeyboardButton(
                        text=f"• {page_num} •",
                        callback_data="current_page"
                    )
                )
            else:
                page_buttons.append(
                    InlineKeyboardButton(
                        text=str(page_num),
                        callback_data=f"{callback_prefix}_{page_num}"
                    )
                )
        
        if page_buttons:
            buttons.append(page_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_simple_pagination_keyboard(
    has_prev: bool,
    has_next: bool, 
    prev_callback: str = "prev_page",
    next_callback: str = "next_page"
) -> InlineKeyboardMarkup:
    """
    إنشاء لوحة مفاتيح تقسيم مبسطة
    
    Args:
        has_prev: هل توجد صفحة سابقة
        has_next: هل توجد صفحة تالية
        prev_callback: callback للصفحة السابقة
        next_callback: callback للصفحة التالية
        
    Returns:
        InlineKeyboardMarkup: لوحة المفاتيح
    """
    buttons = []
    
    if has_prev or has_next:
        row = []
        
        if has_prev:
            row.append(
                InlineKeyboardButton(
                    text="◀️ السابقة",
                    callback_data=prev_callback
                )
            )
        
        if has_next:
            row.append(
                InlineKeyboardButton(
                    text="التالية ▶️",
                    callback_data=next_callback
                )
            )
        
        buttons.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
