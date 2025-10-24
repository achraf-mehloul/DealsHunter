/**
 * دوال التنسيق
 * تنسيق البيانات والعروض المختلفة
 */

/**
 * تنسيق التاريخ
 */
export const formatDate = (date, options = {}) => {
  if (!date) return '-';
  
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC'
  };
  
  const mergedOptions = { ...defaultOptions, ...options };
  
  try {
    return new Date(date).toLocaleDateString('ar-SA', mergedOptions);
  } catch (error) {
    console.error('Error formatting date:', error);
    return '-';
  }
};

/**
 * تنسيق الوقت
 */
export const formatTime = (date, options = {}) => {
  if (!date) return '-';
  
  const defaultOptions = {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC'
  };
  
  const mergedOptions = { ...defaultOptions, ...options };
  
  try {
    return new Date(date).toLocaleTimeString('ar-SA', mergedOptions);
  } catch (error) {
    console.error('Error formatting time:', error);
    return '-';
  }
};

/**
 * تنسيق التاريخ والوقت
 */
export const formatDateTime = (date) => {
  if (!date) return '-';
  
  try {
    const datePart = formatDate(date);
    const timePart = formatTime(date);
    return `${datePart} - ${timePart}`;
  } catch (error) {
    console.error('Error formatting datetime:', error);
    return '-';
  }
};

/**
 * تنسيق العملة
 */
export const formatCurrency = (amount, currency = 'USD') => {
  if (amount === null || amount === undefined) return '-';
  
  try {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  } catch (error) {
    console.error('Error formatting currency:', error);
    return `${amount} ${currency}`;
  }
};

/**
 * تنسيق الأرقام
 */
export const formatNumber = (number, options = {}) => {
  if (number === null || number === undefined) return '-';
  
  const defaultOptions = {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  };
  
  const mergedOptions = { ...defaultOptions, ...options };
  
  try {
    return new Intl.NumberFormat('ar-SA', mergedOptions).format(number);
  } catch (error) {
    console.error('Error formatting number:', error);
    return number.toString();
  }
};

/**
 * تنسيق النسبة المئوية
 */
export const formatPercentage = (value, decimals = 2) => {
  if (value === null || value === undefined) return '-';
  
  try {
    return new Intl.NumberFormat('ar-SA', {
      style: 'percent',
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(value / 100);
  } catch (error) {
    console.error('Error formatting percentage:', error);
    return `${value}%`;
  }
};

/**
 * تقصير النص
 */
export const truncateText = (text, maxLength = 50, suffix = '...') => {
  if (!text) return '';
  
  if (text.length <= maxLength) {
    return text;
  }
  
  return text.substring(0, maxLength - suffix.length) + suffix;
};

/**
 * تنسيق حجم الملف
 */
export const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 B';
  
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  
  return `${Math.round(bytes / Math.pow(1024, i) * 100) / 100} ${sizes[i]}`;
};

/**
 * تنسيق المدة الزمنية
 */
export const formatDuration = (seconds) => {
  if (!seconds || seconds === 0) return '0 ثانية';
  
  const units = [
    { value: 31536000, label: 'سنة' },
    { value: 2592000, label: 'شهر' },
    { value: 86400, label: 'يوم' },
    { value: 3600, label: 'ساعة' },
    { value: 60, label: 'دقيقة' },
    { value: 1, label: 'ثانية' }
  ];
  
  for (const unit of units) {
    if (seconds >= unit.value) {
      const value = Math.floor(seconds / unit.value);
      return `${value} ${unit.label}`;
    }
  }
  
  return `${seconds} ثانية`;
};

/**
 * تنسيق الوقت النسبي
 */
export const formatRelativeTime = (date) => {
  if (!date) return '-';
  
  const now = new Date();
  const target = new Date(date);
  const diffInSeconds = Math.floor((now - target) / 1000);
  
  if (diffInSeconds < 60) {
    return 'الآن';
  }
  
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    return `منذ ${diffInMinutes} دقيقة`;
  }
  
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return `منذ ${diffInHours} ساعة`;
  }
  
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 7) {
    return `منذ ${diffInDays} يوم`;
  }
  
  return formatDate(date);
};

/**
 * تنسيق الهاتف
 */
export const formatPhoneNumber = (phone) => {
  if (!phone) return '-';
  
  // إزالة جميع الأحرف غير الرقمية
  const cleaned = phone.replace(/\D/g, '');
  
  // تنسيق الرقم الدولي
  if (cleaned.length === 10) {
    return cleaned.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
  }
  
  return phone;
};

/**
 * تنسيق البريد الإلكتروني
 */
export const formatEmail = (email) => {
  if (!email) return '-';
  return email.toLowerCase();
};

/**
 * إنشاء نص بديل للصورة
 */
export const generateInitials = (name) => {
  if (!name) return '?';
  
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2);
};

/**
 * تنسيق حالة العنصر
 */
export const formatStatus = (status) => {
  const statusMap = {
    active: 'نشط',
    inactive: 'غير نشط',
    pending: 'قيد الانتظار',
    completed: 'مكتمل',
    failed: 'فشل',
    sent: 'مرسل',
    read: 'مقروء'
  };
  
  return statusMap[status] || status;
};

/**
 * تنسيق اللون بناءً على الحالة
 */
export const getStatusColor = (status) => {
  const colorMap = {
    active: 'success',
    inactive: 'error',
    pending: 'warning',
    completed: 'success',
    failed: 'error',
    sent: 'info',
    read: 'success'
  };
  
  return colorMap[status] || 'info';
};

export default {
  formatDate,
  formatTime,
  formatDateTime,
  formatCurrency,
  formatNumber,
  formatPercentage,
  truncateText,
  formatFileSize,
  formatDuration,
  formatRelativeTime,
  formatPhoneNumber,
  formatEmail,
  generateInitials,
  formatStatus,
  getStatusColor
};
