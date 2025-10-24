/**
 * نموذج إنشاء وتعديل قواعد الفلترة
 */

import React, { useState } from 'react';

const FilterRuleForm = ({ 
  initialData = {}, 
  onSubmit, 
  onCancel, 
  loading = false 
}) => {
  const [formData, setFormData] = useState({
    name: initialData.name || '',
    condition: initialData.condition || { type: 'price_drop', threshold: 10 },
    action: initialData.action || { type: 'send_notification', template: 'default' },
    is_active: initialData.is_active ?? true,
    ...initialData
  });

  const [errors, setErrors] = useState({});

  const conditionTypes = [
    { 
      value: 'price_drop', 
      label: 'انخفاض السعر', 
      icon: '💰',
      fields: [
        { name: 'threshold', type: 'number', label: 'نسبة الانخفاض (%)', min: 1, max: 100 }
      ]
    },
    { 
      value: 'new_product', 
      label: 'منتج جديد', 
      icon: '🆕',
      fields: [
        { name: 'category', type: 'select', label: 'الفئة', options: ['electronics', 'books', 'home'] }
      ]
    },
    { 
      value: 'stock_change', 
      label: 'تغير المخزون', 
      icon: '📦',
      fields: [
        { name: 'threshold', type: 'number', label: 'الحد الأدنى للمخزون', min: 0 }
      ]
    },
    { 
      value: 'rating_threshold', 
      label: 'حد التقييم', 
      icon: '⭐',
      fields: [
        { name: 'threshold', type: 'number', label: 'الحد الأدنى للتقييم', min: 1, max: 5, step: 0.1 }
      ]
    }
  ];

  const actionTypes = [
    { value: 'send_notification', label: 'إرسال إشعار', icon: '🔔' },
    { value: 'send_email', label: 'إرسال بريد إلكتروني', icon: '📧' },
    { value: 'webhook', label: 'استدعاء Webhook', icon: '🔗' }
  ];

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

  const handleConditionChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      condition: {
        ...prev.condition,
        [field]: value
      }
    }));
  };

  const handleActionChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      action: {
        ...prev.action,
        [field]: value
      }
    }));
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'اسم القاعدة مطلوب';
    } else if (formData.name.length < 3) {
      newErrors.name = 'الاسم يجب أن يكون 3 أحرف على الأقل';
    }

    if (!formData.condition.type) {
      newErrors.condition = 'نوع الشرط مطلوب';
    }

    if (!formData.action.type) {
      newErrors.action = 'نوع الإجراء مطلوب';
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

  const selectedCondition = conditionTypes.find(c => c.value === formData.condition.type);
  const selectedAction = actionTypes.find(a => a.value === formData.action.type);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-gray-800 mb-6">
        {initialData.id ? '✏️ تعديل قاعدة الفلترة' : '🆕 إنشاء قاعدة فلترة جديدة'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* المعلومات الأساسية */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* اسم القاعدة */}
          <div className="form-group">
            <label className="form-label">اسم القاعدة</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="أدخل اسم القاعدة..."
              className={`form-input ${errors.name ? 'border-red-500' : ''}`}
            />
            {errors.name && (
              <p className="form-error">{errors.name}</p>
            )}
          </div>

          {/* حالة القاعدة */}
          <div className="form-group">
            <label className="form-label">الحالة</label>
            <div className="mt-2">
              <label className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer">
                <input
                  type="checkbox"
                  name="is_active"
                  checked={formData.is_active}
                  onChange={handleChange}
                  className="rounded text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  {formData.is_active ? '✅ مفعلة' : '❌ معطلة'}
                </span>
              </label>
            </div>
          </div>
        </div>

        {/* الشرط */}
        <div className="form-group">
          <label className="form-label">⚡ الشرط</label>
          
          {/* نوع الشرط */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">نوع الشرط</label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {conditionTypes.map(condition => (
                <label key={condition.value} className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer border border-gray-200 rounded-lg p-3 hover:bg-gray-50">
                  <input
                    type="radio"
                    name="condition_type"
                    value={condition.value}
                    checked={formData.condition.type === condition.value}
                    onChange={(e) => handleConditionChange('type', e.target.value)}
                    className="text-primary-600 focus:ring-primary-500"
                  />
                  <span className="text-sm">
                    {condition.icon} {condition.label}
                  </span>
                </label>
              ))}
            </div>
            {errors.condition && (
              <p className="form-error">{errors.condition}</p>
            )}
          </div>

          {/* حقول الشرط */}
          {selectedCondition && selectedCondition.fields && (
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <label className="block text-sm font-medium text-gray-700 mb-3">إعدادات الشرط</label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {selectedCondition.fields.map(field => (
                  <div key={field.name}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {field.label}
                    </label>
                    {field.type === 'select' ? (
                      <select
                        value={formData.condition[field.name] || ''}
                        onChange={(e) => handleConditionChange(field.name, e.target.value)}
                        className="form-select"
                      >
                        <option value="">اختر {field.label}</option>
                        {field.options?.map(option => (
                          <option key={option} value={option}>
                            {option}
                          </option>
                        ))}
                      </select>
                    ) : (
                      <input
                        type={field.type}
                        value={formData.condition[field.name] || ''}
                        onChange={(e) => handleConditionChange(field.name, e.target.value)}
                        min={field.min}
                        max={field.max}
                        step={field.step}
                        placeholder={`أدخل ${field.label}`}
                        className="form-input"
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* الإجراء */}
        <div className="form-group">
          <label className="form-label">🎯 الإجراء</label>
          
          {/* نوع الإجراء */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">نوع الإجراء</label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {actionTypes.map(action => (
                <label key={action.value} className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer border border-gray-200 rounded-lg p-3 hover:bg-gray-50">
                  <input
                    type="radio"
                    name="action_type"
                    value={action.value}
                    checked={formData.action.type === action.value}
                    onChange={(e) => handleActionChange('type', e.target.value)}
                    className="text-primary-600 focus:ring-primary-500"
                  />
                  <span className="text-sm">
                    {action.icon} {action.label}
                  </span>
                </label>
              ))}
            </div>
            {errors.action && (
              <p className="form-error">{errors.action}</p>
            )}
          </div>

          {/* إعدادات الإجراء */}
          {selectedAction && (
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
              <label className="block text-sm font-medium text-gray-700 mb-3">إعدادات الإجراء</label>
              <div className="space-y-4">
                {selectedAction.value === 'send_notification' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      قالب الإشعار
                    </label>
                    <select
                      value={formData.action.template || 'default'}
                      onChange={(e) => handleActionChange('template', e.target.value)}
                      className="form-select"
                    >
                      <option value="default">القالب الافتراضي</option>
                      <option value="price_drop">انخفاض السعر</option>
                      <option value="new_product">منتج جديد</option>
                      <option value="stock_alert">تنبيه المخزون</option>
                    </select>
                  </div>
                )}
                
                {selectedAction.value === 'webhook' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      رابط Webhook
                    </label>
                    <input
                      type="url"
                      value={formData.action.url || ''}
                      onChange={(e) => handleActionChange('url', e.target.value)}
                      placeholder="https://example.com/webhook"
                      className="form-input"
                    />
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* معاينة القاعدة */}
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <h4 className="font-medium text-blue-800 mb-2">👁️ معاينة القاعدة:</h4>
          <div className="text-sm text-blue-700 space-y-1">
            <p><strong>الاسم:</strong> {formData.name || 'غير محدد'}</p>
            <p><strong>الشرط:</strong> {selectedCondition?.label || 'غير محدد'}</p>
            <p><strong>الإجراء:</strong> {selectedAction?.label || 'غير محدد'}</p>
            <p><strong>الحالة:</strong> {formData.is_active ? '✅ مفعلة' : '❌ معطلة'}</p>
          </div>
        </div>

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
              initialData.id ? 'تحديث القاعدة' : 'إنشاء القاعدة'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FilterRuleForm;
