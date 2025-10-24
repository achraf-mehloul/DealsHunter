"""
حالات إدارة المستخدم
FSM states لإعدادات وتفضيلات المستخدم
"""

from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    """حالات إدارة المستخدم"""
    
    # إعدادات الإشعارات
    waiting_notification_preference = State()
    changing_language = State()
    
    # إدارة الملف الشخصي
    editing_profile = State()
    changing_username = State()
