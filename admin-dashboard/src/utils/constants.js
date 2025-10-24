/**
 * الثوابت العامة للتطبيق
 */

// أدوار المستخدمين
export const USER_ROLES = {
  SUPER_ADMIN: 'super_admin',
  ADMIN: 'admin',
  MODERATOR: 'moderator',
  VIEWER: 'viewer'
};

// صلاحيات المستخدمين
export const PERMISSIONS = {
  // الصلاحيات العامة
  READ: 'read',
  WRITE: 'write',
  DELETE: 'delete',
  
  // الصلاحيات الخاصة
  MANAGE_USERS: 'manage_users',
  MANAGE_PRODUCTS: 'manage_products',
  MANAGE_NOTIFICATIONS: 'manage_notifications',
  VIEW_ANALYTICS: 'view_analytics',
  MANAGE_SETTINGS: 'manage_settings'
};

// تعيين الصلاحيات للأدوار
export const ROLE_PERMISSIONS = {
  [USER_ROLES.SUPER_ADMIN]: [
    PERMISSIONS.READ,
    PERMISSIONS.WRITE,
    PERMISSIONS.DELETE,
    PERMISSIONS.MANAGE_USERS,
    PERMISSIONS.MANAGE_PRODUCTS,
    PERMISSIONS.MANAGE_NOTIFICATIONS,
    PERMISSIONS.VIEW_ANALYTICS,
    PERMISSIONS.MANAGE_SETTINGS
  ],
  [USER_ROLES.ADMIN]: [
    PERMISSIONS.READ,
    PERMISSIONS.WRITE,
    PERMISSIONS.DELETE,
    PERMISSIONS.MANAGE_USERS,
    PERMISSIONS.MANAGE_PRODUCTS,
    PERMISSIONS.MANAGE_NOTIFICATIONS,
    PERMISSIONS.VIEW_ANALYTICS
  ],
  [USER_ROLES.MODERATOR]: [
    PERMISSIONS.READ,
    PERMISSIONS.WRITE,
    PERMISSIONS.MANAGE_PRODUCTS,
    PERMISSIONS.MANAGE_NOTIFICATIONS
  ],
  [USER_ROLES.VIEWER]: [
    PERMISSIONS.READ,
    PERMISSIONS.VIEW_ANALYTICS
  ]
};

// أنواع الإشعارات
export const NOTIFICATION_TYPES = {
  PRICE_DROP: 'price_drop',
  NEW_PRODUCT: 'new_product',
  STOCK_ALERT: 'stock_alert',
  SYSTEM_ALERT: 'system_alert',
  PROMOTION: 'promotion',
  USER_ACTION: 'user_action'
};

// حالات الإشعارات
export const NOTIFICATION_STATUS = {
  PENDING: 'pending',
  SENT: 'sent',
  FAILED: 'failed',
  READ: 'read'
};

// فئات المنتجات
export const PRODUCT_CATEGORIES = {
  ELECTRONICS: 'electronics',
  CLOTHING: 'clothing',
  HOME: 'home',
  BOOKS: 'books',
  BEAUTY: 'beauty',
  SPORTS: 'sports',
  TOYS: 'toys',
  AUTOMOTIVE: 'automotive',
  OTHER: 'other'
};

// أسماء فئات المنتجات بالعربية
export const PRODUCT_CATEGORY_NAMES = {
  [PRODUCT_CATEGORIES.ELECTRONICS]: 'إلكترونيات',
  [PRODUCT_CATEGORIES.CLOTHING]: 'ملابس',
  [PRODUCT_CATEGORIES.HOME]: 'منزل',
  [PRODUCT_CATEGORIES.BOOKS]: 'كتب',
  [PRODUCT_CATEGORIES.BEAUTY]: 'تجميل',
  [PRODUCT_CATEGORIES.SPORTS]: 'رياضة',
  [PRODUCT_CATEGORIES.TOYS]: 'ألعاب',
  [PRODUCT_CATEGORIES.AUTOMOTIVE]: 'سيارات',
  [PRODUCT_CATEGORIES.OTHER]: 'أخرى'
};

// فلاتر البحث
export const SEARCH_FILTERS = {
  PRICE_RANGE: 'price_range',
  CATEGORY: 'category',
  RATING: 'rating',
  PRIME_ONLY: 'prime_only',
  DISCOUNT_ONLY: 'discount_only'
};

// فترات الزمنية للتحليلات
export const TIME_PERIODS = {
  TODAY: 'today',
  YESTERDAY: 'yesterday',
  LAST_7_DAYS: '7d',
  LAST_30_DAYS: '30d',
  LAST_90_DAYS: '90d',
  THIS_YEAR: 'year'
};

// أسماء الفترات الزمنية بالعربية
export const TIME_PERIOD_NAMES = {
  [TIME_PERIODS.TODAY]: 'اليوم',
  [TIME_PERIODS.YESTERDAY]: 'أمس',
  [TIME_PERIODS.LAST_7_DAYS]: 'آخر 7 أيام',
  [TIME_PERIODS.LAST_30_DAYS]: 'آخر 30 يوم',
  [TIME_PERIODS.LAST_90_DAYS]: 'آخر 90 يوم',
  [TIME_PERIODS.THIS_YEAR]: 'هذه السنة'
};

// إعدادات البوت
export const BOT_SETTINGS = {
  DEFAULT_LANGUAGE: 'ar',
  SUPPORTED_LANGUAGES: ['ar', 'en'],
  MAX_PRODUCTS_PER_PAGE: 10,
  CACHE_TIMEOUT: 300,
  REQUEST_TIMEOUT: 30
};

// رسائل الأخطاء
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'خطأ في الاتصال بالخادم',
  UNAUTHORIZED: 'غير مصرح بالدخول',
  FORBIDDEN: 'غير مسموح بالوصول',
  NOT_FOUND: 'لم يتم العثور على المورد',
  VALIDATION_ERROR: 'خطأ في البيانات المدخلة',
  SERVER_ERROR: 'خطأ في الخادم',
  UNKNOWN_ERROR: 'حدث خطأ غير متوقع'
};

// رسائل النجاح
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'تم تسجيل الدخول بنجاح',
  LOGOUT_SUCCESS: 'تم تسجيل الخروج بنجاح',
  SAVE_SUCCESS: 'تم الحفظ بنجاح',
  DELETE_SUCCESS: 'تم الحذف بنجاح',
  UPDATE_SUCCESS: 'تم التحديث بنجاح',
  CREATE_SUCCESS: 'تم الإنشاء بنجاح'
};

// الألوان للتطبيق
export const COLORS = {
  PRIMARY: '#3B82F6',
  SUCCESS: '#10B981',
  WARNING: '#F59E0B',
  ERROR: '#EF4444',
  INFO: '#6B7280',
  
  // ألوان الرسوم البيانية
  CHART_COLORS: [
    '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
    '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
  ]
};

// القيم الافتراضية
export const DEFAULTS = {
  PAGE_SIZE: 20,
  ITEMS_PER_PAGE: [10, 20, 50, 100],
  DEBOUNCE_DELAY: 300,
  AUTO_SAVE_DELAY: 1000
};

export default {
  USER_ROLES,
  PERMISSIONS,
  ROLE_PERMISSIONS,
  NOTIFICATION_TYPES,
  PRODUCT_CATEGORIES,
  SEARCH_FILTERS,
  TIME_PERIODS,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  COLORS,
  DEFAULTS
};
