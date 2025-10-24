/**
 * نافذة عرض وتعديل المستخدم
 */

import React, { useState, useEffect } from 'react';

const UserModal = ({ 
  user = null, 
  isOpen, 
  onClose, 
  onSave, 
  loading = false 
}) => {
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    language_code: 'ar',
    role: 'user',
    is_active: true,
    notifications_enabled: true
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username || '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        language_code: user.language_code || 'ar',
        role: user.role || 'user',
        is_active: user.is_active ?? true,
        notifications_enabled: user.notifications_enabled ?? true
      });
    } else {
      setFormData({
        username: '',
        first_name: '',
        last_name: '',
        language_code: 'ar',
        role: 'user',
        is_active: true,
        notifications_enabled: true
      });
    }
    setErrors({});
  }, [user, isOpen]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.first_name.trim()) {
      newErrors.first_name = 'الاسم الأول مطلوب';
    }

    if (formData.username && formData.username.length < 3) {
      newErrors.username = 'اسم المستخدم يجب أن يكون 3 أحرف على الأقل';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSave(formData, user?.id);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* الرأس */}
        <div className="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-800">
            {user ? '✏️ تعديل المستخدم' : '👤 إضافة مستخدم جديد'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* المحتوى */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* الاسم الأول */}
          <div className="form-group">
            <label className="form-label">الاسم الأول *</label>
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              className={`form-input ${errors.first_name ? 'border-red-500' : ''}`}
              placeholder="أدخل الاسم الأول"
            />
            {errors.first_name && (
              <p className="form-error">{errors.first_name}</p>
            )}
          </div>

          {/* الاسم الأخير */}
          <div className="form-group">
            <label className="form-label">الاسم الأخير</label>
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              className="form-input"
              placeholder="أدخل الاسم الأخير"
            />
          </div>

          {/* اسم المستخدم */}
          <div className="form-group">
            <label className="form-label">اسم المستخدم</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className={`form-input ${errors.username ? 'border-red-500' : ''}`}
              placeholder="أدخل اسم المستخدم"
            />
            {errors.username && (
              <p className="form-error">{errors.username}</p>
            )}
          </div>

          {/* اللغة */}
          <div className="form-group">
            <label className="form-label">اللغة</label>
            <select
              name="language_code"
              value={formData.language_code}
              onChange={handleChange}
              className="form-select"
            >
              <option value="ar">العربية</option>
              <option value="en">English</option>
            </select>
          </div>

          {/* الدور */}
          <div className="form-group">
            <label className="form-label">الدور</label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="form-select"
            >
              <option value="user">مستخدم</option>
              <option value="admin">مدير</option>
              <option value="moderator">مشرف</option>
            </select>
          </div>

          {/* الإعدادات */}
          <div className="space-y-3">
            <label className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer">
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
                className="rounded text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm font-medium text-gray-700">الحساب نشط</span>
            </label>

            <label className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer">
              <input
                type="checkbox"
                name="notifications_enabled"
                checked={formData.notifications_enabled}
                onChange={handleChange}
                className="rounded text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm font-medium text-gray-700">تفعيل الإشعارات</span>
            </label>
          </div>

          {/* معلومات إضافية للمستخدم الحالي */}
          {user && (
            <div className="bg-gray-50 p-3 rounded-lg border border-gray-200">
              <h4 className="font-medium text-gray-700 mb-2">معلومات إضافية:</h4>
              <div className="text-sm text-gray-600 space-y-1">
                <p>معرف التليجرام: <strong>{user.telegram_id}</strong></p>
                <p>تاريخ التسجيل: <strong>{new Date(user.created_at).toLocaleDateString('ar-SA')}</strong></p>
                <p>آخر تحديث: <strong>{new Date(user.updated_at).toLocaleDateString('ar-SA')}</strong></p>
              </div>
            </div>
          )}

          {/* أزرار الإجراءات */}
          <div className="flex justify-end space-x-3 rtl:space-x-reverse pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-outline"
              disabled={loading}
            >
              إلغاء
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? (
                <span className="flex items-center space-x-2 rtl:space-x-reverse">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>جاري الحفظ...</span>
                </span>
              ) : (
                user ? 'تحديث' : 'إضافة'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserModal;
