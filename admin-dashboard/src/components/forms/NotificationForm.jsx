/**
 * نموذج إنشاء وتعديل الإشعارات
 */

import React, { useState } from 'react';

const NotificationForm = ({ 
  initialData = {}, 
  onSubmit, 
  onCancel, 
  loading = false 
}) => {
  const [formData, setFormData] = useState({
    title: initialData.title || '',
    message: initialData.message || '',
    notification_type: initialData.notification_type || 'system_alert',
    broadcast: initialData.broadcast || false,
    ...initialData
  });

  const [errors, setErrors] = useState({});

  const notificationTypes = [
    { value: 'system_alert', label: 'تنبيه النظام', icon: '⚠️' },
    { value: 'price_drop', label: 'انخفاض السعر', icon: '💰' },
    { value: 'new_product', label: 'منتج جديد', icon: '🆕' },
    { value: 'stock_alert', label: 'تنبيه المخزون', icon: '📦' },
    { value: 'promotion', label: 'عرض ترويجي', icon: '🎉' }
  ];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // مسح الخطأ عند التعديل
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'عنوان الإشعار مطلوب';
    } else if (formData.title.length < 5) {
      newErrors.title = 'العنوان يجب أن يكون 5 أحرف على الأقل';
    }

    if (!formData.message.trim()) {
      newErrors.message = 'نص الإشعار مطلوب';
    } else if (formData.message.length < 10) {
      newErrors.message = 'نص الإشعار يجب أن يكون 10 أحرف على الأقل';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-gray-800 mb-6">
        {initialData.id ? '✏️ تعديل الإشعار' : '🆕 إنشاء إشعار جديد'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* نوع الإشعار */}
        <div className="form-group">
          <label className="form-label">نوع الإشعار</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {notificationTypes.map(type => (
              <label key={type.value} className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer">
                <input
                  type="radio"
                  name="notification_type"
                  value={type.value}
                  checked={formData.notification_type === type.value}
                  onChange={handleChange}
                  className="text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm">
                  {type.icon} {type.label}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* بث لجميع المستخدمين */}
        <div className="form-group">
          <label className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer">
            <input
              type="checkbox"
              name="broadcast"
              checked={formData.broadcast}
              onChange={handleChange}
              className="rounded text-primary-600 focus:ring-primary-500"
            />
            <span className="form-label mb-0">📢 بث هذا الإشعار لجميع المستخدمين</span>
          </label>
          <p className="text-sm text-gray-500 mt-1">
            إذا تم تفعيل هذا الخيار، سيتم إرسال الإشعار لجميع المستخدمين المسجلين في النظام
          </p>
        </div>

        {/* عنوان الإشعار */}
        <div className="form-group">
          <label className="form-label">عنوان الإشعار</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="أدخل عنوان الإشعار..."
            className={`form-input ${errors.title ? 'border-red-500' : ''}`}
            maxLength={200}
          />
          {errors.title && (
            <p className="form-error">{errors.title}</p>
          )}
          <p className="text-xs text-gray-500 mt-1">
            {formData.title.length}/200 حرف
          </p>
        </div>

        {/* نص الإشعار */}
        <div className="form-group">
          <label className="form-label">نص الإشعار</label>
          <textarea
            name="message"
            value={formData.message}
            onChange={handleChange}
            placeholder="أدخل نص الإشعار..."
            rows={6}
            className={`form-textarea ${errors.message ? 'border-red-500' : ''}`}
            maxLength={1000}
          />
          {errors.message && (
            <p className="form-error">{errors.message}</p>
          )}
          <p className="text-xs text-gray-500 mt-1">
            {formData.message.length}/1000 حرف
          </p>
        </div>

        {/* معاينة الإشعار */}
        {formData.title && formData.message && (
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <h4 className="font-medium text-gray-700 mb-2">👁️ معاينة الإشعار:</h4>
            <div className="bg-white p-3 rounded border">
              <h5 className="font-bold text-lg mb-2">{formData.title}</h5>
              <p className="text-gray-700 whitespace-pre-wrap">{formData.message}</p>
              <div className="mt-2 text-xs text-gray-500">
                نوع: {notificationTypes.find(t => t.value === formData.notification_type)?.label}
                {formData.broadcast && ' • 📢 مرسل للجميع'}
              </div>
            </div>
          </div>
        )}

        {/* أزرار الإجراءات */}
        <div className="flex justify-end space-x-3 rtl:space-x-reverse pt-4 border-t border-gray-200">
          <button
            type="button"
            onClick={onCancel}
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
              initialData.id ? 'تحديث الإشعار' : 'إنشاء الإشعار'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default NotificationForm;
