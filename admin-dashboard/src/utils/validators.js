/**
 * دوال التحقق من الصحة
 * التحقق من صحة البيانات المدخلة
 */

/**
 * التحقق من البريد الإلكتروني
 */
export const validateEmail = (email) => {
  if (!email) {
    return 'البريد الإلكتروني مطلوب';
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return 'البريد الإلكتروني غير صالح';
  }
  
  return null;
};

/**
 * التحقق من كلمة المرور
 */
export const validatePassword = (password) => {
  if (!password) {
    return 'كلمة المرور مطلوبة';
  }
  
  if (password.length < 8) {
    return 'كلمة المرور يجب أن تكون 8 أحرف على الأقل';
  }
  
  if (!/(?=.*[a-z])/.test(password)) {
    return 'كلمة المرور يجب أن تحتوي على حرف صغير على الأقل';
  }
  
  if (!/(?=.*[A-Z])/.test(password)) {
    return 'كلمة المرور يجب أن تحتوي على حرف كبير على الأقل';
  }
  
  if (!/(?=.*\d)/.test(password)) {
    return 'كلمة المرور يجب أن تحتوي على رقم على الأقل';
  }
  
  return null;
};

/**
 * التحقق من التأكيد كلمة المرور
 */
export const validatePasswordConfirmation = (password, confirmation) => {
  if (!confirmation) {
    return 'تأكيد كلمة المرور مطلوب';
  }
  
  if (password !== confirmation) {
    return 'كلمات المرور غير متطابقة';
  }
  
  return null;
};

/**
 * التحقق من الاسم
 */
export const validateName = (name, fieldName = 'الاسم') => {
  if (!name) {
    return `${fieldName} مطلوب`;
  }
  
  if (name.length < 2) {
    return `${fieldName} يجب أن يكون حرفين على الأقل`;
  }
  
  if (name.length > 50) {
    return `${fieldName} يجب أن لا يتجاوز 50 حرف`;
  }
  
  return null;
};

/**
 * التحقق من الرقم
 */
export const validateNumber = (number, options = {}) => {
  const {
    required = true,
    min,
    max,
    fieldName = 'القيمة'
  } = options;
  
  if (!number && required) {
    return `${fieldName} مطلوبة`;
  }
  
  if (number === '' || number === null || number === undefined) {
    return null;
  }
  
  const num = Number(number);
  if (isNaN(num)) {
    return `${fieldName} يجب أن تكون رقمية`;
  }
  
  if (min !== undefined && num < min) {
    return `${fieldName} يجب أن تكون ${min} على الأقل`;
  }
  
  if (max !== undefined && num > max) {
    return `${fieldName} يجب أن لا تتجاوز ${max}`;
  }
  
  return null;
};

/**
 * التحقق من النص
 */
export const validateText = (text, options = {}) => {
  const {
    required = true,
    minLength,
    maxLength,
    fieldName = 'النص'
  } = options;
  
  if (!text && required) {
    return `${fieldName} مطلوب`;
  }
  
  if (!text) {
    return null;
  }
  
  if (minLength && text.length < minLength) {
    return `${fieldName} يجب أن يكون ${minLength} أحرف على الأقل`;
  }
  
  if (maxLength && text.length > maxLength) {
    return `${fieldName} يجب أن لا يتجاوز ${maxLength} حرف`;
  }
  
  return null;
};

/**
 * التحقق من الهاتف
 */
export const validatePhone = (phone) => {
  if (!phone) {
    return 'رقم الهاتف مطلوب';
  }
  
  // إزالة جميع الأحرف غير الرقمية
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length < 10) {
    return 'رقم الهاتف يجب أن يكون 10 أرقام على الأقل';
  }
  
  return null;
};

/**
 * التحقق من الرابط
 */
export const validateUrl = (url) => {
  if (!url) {
    return 'الرابط مطلوب';
  }
  
  try {
    new URL(url);
    return null;
  } catch (error) {
    return 'الرابط غير صالح';
  }
};

/**
 * التحقق من التاريخ
 */
export const validateDate = (date, options = {}) => {
  const {
    required = true,
    minDate,
    maxDate,
    fieldName = 'التاريخ'
  } = options;
  
  if (!date && required) {
    return `${fieldName} مطلوب`;
  }
  
  if (!date) {
    return null;
  }
  
  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) {
    return `${fieldName} غير صالح`;
  }
  
  if (minDate && dateObj < new Date(minDate)) {
    return `${fieldName} يجب أن يكون بعد ${formatDate(minDate)}`;
  }
  
  if (maxDate && dateObj > new Date(maxDate)) {
    return `${fieldName} يجب أن يكون قبل ${formatDate(maxDate)}`;
  }
  
  return null;
};

/**
 * التحقق من القائمة
 */
export const validateArray = (array, options = {}) => {
  const {
    required = true,
    minLength,
    maxLength,
    fieldName = 'القائمة'
  } = options;
  
  if ((!array || array.length === 0) && required) {
    return `${fieldName} مطلوبة`;
  }
  
  if (!array) {
    return null;
  }
  
  if (minLength && array.length < minLength) {
    return `${fieldName} يجب أن تحتوي على ${minLength} عناصر على الأقل`;
  }
  
  if (maxLength && array.length > maxLength) {
    return `${fieldName} يجب أن لا تتجاوز ${maxLength} عنصر`;
  }
  
  return null;
};

/**
 * التحقق من الملف
 */
export const validateFile = (file, options = {}) => {
  const {
    required = true,
    maxSize, // بالبايت
    allowedTypes = [],
    fieldName = 'الملف'
  } = options;
  
  if (!file && required) {
    return `${fieldName} مطلوب`;
  }
  
  if (!file) {
    return null;
  }
  
  if (maxSize && file.size > maxSize) {
    const maxSizeMB = (maxSize / (1024 * 1024)).toFixed(1);
    return `حجم ${fieldName} يجب أن لا يتجاوز ${maxSizeMB} MB`;
  }
  
  if (allowedTypes.length > 0 && !allowedTypes.includes(file.type)) {
    const allowedExtensions = allowedTypes.map(type => type.split('/')[1]).join(', ');
    return `نوع ${fieldName} غير مسموح. المسموح: ${allowedExtensions}`;
  }
  
  return null;
};

/**
 * التحقق من سعر المنتج
 */
export const validateProductPrice = (price) => {
  if (!price && price !== 0) {
    return 'سعر المنتج مطلوب';
  }
  
  const num = Number(price);
  if (isNaN(num)) {
    return 'سعر المنتج يجب أن يكون رقماً';
  }
  
  if (num < 0) {
    return 'سعر المنتج يجب أن يكون موجباً';
  }
  
  if (num > 1000000) {
    return 'سعر المنتج كبير جداً';
  }
  
  return null;
};

/**
 * التحقق من تقييم المنتج
 */
export const validateProductRating = (rating) => {
  if (!rating && rating !== 0) {
    return null; // التقييم اختياري
  }
  
  const num = Number(rating);
  if (isNaN(num)) {
    return 'التقييم يجب أن يكون رقماً';
  }
  
  if (num < 0 || num > 5) {
    return 'التقييم يجب أن يكون بين 0 و 5';
  }
  
  return null;
};

/**
 * التحقق من بيانات تسجيل الدخول
 */
export const validateLoginForm = (data) => {
  const errors = {};
  
  const emailError = validateEmail(data.email);
  if (emailError) errors.email = emailError;
  
  const passwordError = validatePassword(data.password);
  if (passwordError) errors.password = passwordError;
  
  return errors;
};

/**
 * التحقق من بيانات المستخدم
 */
export const validateUserForm = (data) => {
  const errors = {};
  
  const nameError = validateName(data.name, 'الاسم');
  if (nameError) errors.name = nameError;
  
  const emailError = validateEmail(data.email);
  if (emailError) errors.email = emailError;
  
  if (data.phone) {
    const phoneError = validatePhone(data.phone);
    if (phoneError) errors.phone = phoneError;
  }
  
  return errors;
};

/**
 * التحقق من بيانات المنتج
 */
export const validateProductForm = (data) => {
  const errors = {};
  
  const nameError = validateText(data.name, { 
    fieldName: 'اسم المنتج',
    minLength: 2,
    maxLength: 200
  });
  if (nameError) errors.name = nameError;
  
  const priceError = validateProductPrice(data.price);
  if (priceError) errors.price = priceError;
  
  if (data.rating) {
    const ratingError = validateProductRating(data.rating);
    if (ratingError) errors.rating = ratingError;
  }
  
  return errors;
};

// استيراد دوال التنسيق للمساعدة
import { formatDate } from './formatters';

export default {
  validateEmail,
  validatePassword,
  validatePasswordConfirmation,
  validateName,
  validateNumber,
  validateText,
  validatePhone,
  validateUrl,
  validateDate,
  validateArray,
  validateFile,
  validateProductPrice,
  validateProductRating,
  validateLoginForm,
  validateUserForm,
  validateProductForm
};
