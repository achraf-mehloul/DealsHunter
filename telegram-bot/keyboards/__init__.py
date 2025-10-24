"""
حزمة لوحات المفاتيح
تجمع جميع لوحات المفاتيح
"""

from .reply.main_menu import get_main_menu_keyboard
from .reply.quick_actions import get_quick_actions_keyboard

from .inline.products import (
    get_products_keyboard,
    get_product_details_keyboard
)
from .inline.pagination import get_pagination_keyboard
from .inline.filters import get_search_filters_keyboard

__all__ = [
    'get_main_menu_keyboard',
    'get_quick_actions_keyboard',
    'get_products_keyboard',
    'get_product_details_keyboard',
    'get_pagination_keyboard',
    'get_search_filters_keyboard'
]
