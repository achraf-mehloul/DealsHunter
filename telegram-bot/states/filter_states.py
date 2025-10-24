"""
حالات الفلترة
FSM states لإعدادات الفلترة المتقدمة
"""

from aiogram.fsm.state import State, StatesGroup

class FilterStates(StatesGroup):
    """حالات إعداد الفلاتر"""
    
    # فلاتر السعر
    setting_min_price = State()
    setting_max_price = State()
    
    # فلاتر التقييم
    setting_min_rating = State()
    
    # فلاتر الفئة
    choosing_category = State()
    
    # فلاتر متقدمة
    setting_advanced_filters = State()
