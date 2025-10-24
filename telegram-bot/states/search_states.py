"""
حالات البحث
FSM states لعملية البحث عن المنتجات
"""

from aiogram.fsm.state import State, StatesGroup

class SearchStates(StatesGroup):
    """حالات البحث عن المنتجات"""
    
    # عملية البحث الأساسية
    waiting_for_query = State()
    waiting_for_filters = State()
    
    # البحث المتقدم
    setting_price_range = State()
    setting_category = State()
    setting_rating_filter = State()
