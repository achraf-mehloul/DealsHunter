/**
 * نافذة عرض وتعديل المنتج
 */

import React, { useState, useEffect } from 'react';

const ProductModal = ({ 
  product = null, 
  isOpen, 
  onClose, 
  onSave, 
  loading = false 
}) => {
  const [formData, setFormData] = useState({
    name: '',
    asin: '',
    price: '',
    original_price: '',
    currency: 'USD',
    category: '',
    image_url: '',
    product_url: '',
    rating: '',
    review_count: '',
    availability: 'In Stock',
    prime_eligible: false
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name || '',
        asin: product.asin || '',
        price: product.price || '',
        original_price: product.original_price || '',
        currency: product.currency || 'USD',
        category: product.category || '',
        image_url: product.image_url || '',
        product_url: product.product_url || '',
        rating: product.rating || '',
        review_count: product.review_count || '',
        availability: product.availability || 'In Stock',
        prime_eligible: product.prime_eligible || false
      });
    } else {
      setFormData({
        name: '',
        asin: '',
        price: '',
        original_price: '',
        currency: 'USD',
        category: '',
        image_url: '',
        product_url: '',
        rating: '',
        review_count: '',
        availability: 'In Stock',
        prime_eligible: false
      });
    }
    setErrors({});
  }, [product, isOpen]);

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

    if (!formData.name.trim()) {
      newErrors.name = 'اسم المنتج مطلوب';
    }

    if (!formData.asin.trim()) {
      newErrors.asin = 'ASIN مطلوب';
    } else if (formData.asin.length !== 10) {
      newErrors.asin = 'ASIN يجب أن يكون 10 أحرف';
    }

    if (!formData.price || isNaN(formData.price)) {
      newErrors.price = 'السعر مطلوب ويجب أن يكون رقماً';
    }

    if (!formData.product_url.trim()) {
      newErrors.product_url = 'رابط المنتج مطلوب';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSave(formData, product?.id);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* الرأس */}
        <div className="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-800">
            {product ? '✏️ تعديل المنتج' : '📦 إضافة منتج جديد'}
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* اسم المنتج */}
            <div className="form-group md:col-span-2">
              <label className="form-label">اسم المنتج *</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className={`form-input ${errors.name ? 'border-red-500' : ''}`}
                placeholder="أدخل اسم المنتج"
              />
              {errors.name && (
                <p className="form-error">{errors.name}</p>
              )}
            </div>

            {/* ASIN */}
            <div className="form-group">
              <label className="form-label">ASIN *</label>
              <input
                type="text"
                name="asin"
                value={formData.asin}
                onChange={handleChange}
                className={`form-input ${errors.asin ? 'border-red-500' : ''}`}
                placeholder="B08N5WRWNW"
                maxLength={10}
              />
              {errors.asin && (
                <p className="form-error">{errors.asin}</p>
              )}
            </div>

            {/* الفئة */}
            <div className="form-group">
              <label className="form-label">الفئة</label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="form-select"
              >
                <option value="">اختر الفئة</option>
                <option value="Electronics">إلكترونيات</option>
                <option value="Books">كتب</option>
                <option value="Home">منزل</option>
                <option value="Beauty">تجميل</option>
                <option value="Sports">رياضة</option>
                <option value="Other">أخرى</option>
              </select>
            </div>

            {/* السعر */}
            <div className="form-group">
              <label className="form-label">السعر الحالي *</label>
              <div className="relative">
                <input
                  type="number"
                  name="price"
                  value={formData.price}
                  onChange={handleChange}
                  step="0.01"
                  min="0"
                  className={`form-input pr-12 ${errors.price ? 'border-red-500' : ''}`}
                  placeholder="0.00"
                />
                <div className="absolute inset-y-0 left-0 flex items-center pl-3">
                  <span className="text-gray-500">$</span>
                </div>
              </div>
              {errors.price && (
                <p className="form-error">{errors.price}</p>
              )}
            </div>

            {/* السعر الأصلي */}
            <div className="form-group">
              <label className="form-label">السعر الأصلي</label>
              <div className="relative">
                <input
                  type="number"
                  name="original_price"
                  value={formData.original_price}
                  onChange={handleChange}
                  step="0.01"
                  min="0"
                  className="form-input pr-12"
                  placeholder="0.00"
                />
                <div className="absolute inset-y-0 left-0 flex items-center pl-3">
                  <span className="text-gray-500">$</span>
                </div>
              </div>
            </div>

            {/* التقييم */}
            <div className="form-group">
              <label className="form-label">التقييم</label>
              <input
                type="number"
                name="rating"
                value={formData.rating}
                onChange={handleChange}
                step="0.1"
                min="0"
                max="5"
                className="form-input"
                placeholder="4.5"
              />
            </div>

            {/* عدد التقييمات */}
            <div className="form-group">
              <label className="form-label">عدد التقييمات</label>
              <input
                type="number"
                name="review_count"
                value={formData.review_count}
                onChange={handleChange}
                min="0"
                className="form-input"
                placeholder="1000"
              />
            </div>

            {/* صورة المنتج */}
            <div className="form-group md:col-span-2">
              <label className="form-label">رابط الصورة</label>
              <input
                type="url"
                name="image_url"
                value={formData.image_url}
                onChange={handleChange}
                className="form-input"
                placeholder="https://example.com/image.jpg"
              />
            </div>

            {/* رابط المنتج */}
            <div className="form-group md:col-span-2">
              <label className="form-label">رابط المنتج *</label>
              <input
                type="url"
                name="product_url"
                value={formData.product_url}
                onChange={handleChange}
                className={`form-input ${errors.product_url ? 'border-red-500' : ''}`}
                placeholder="https://amazon.com/dp/B08N5WRWNW"
              />
              {errors.product_url && (
                <p className="form-error">{errors.product_url}</p>
              )}
            </div>
          </div>

          {/* الإعدادات الإضافية */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* التوفر */}
            <div className="form-group">
              <label className="form-label">الحالة</label>
              <select
                name="availability"
                value={formData.availability}
                onChange={handleChange}
                className="form-select"
              >
                <option value="In Stock">متوفر</option>
                <option value="Out of Stock">غير متوفر</option>
                <option value="Pre-order">طلب مسبق</option>
              </select>
            </div>

            {/* Prime */}
            <div className="form-group flex items-center justify-end">
              <label className="flex items-center space-x-2 rtl:space-x-reverse cursor-pointer">
                <input
                  type="checkbox"
                  name="prime_eligible"
                  checked={formData.prime_eligible}
                  onChange={handleChange}
                  className="rounded text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-gray-700">منتج Prime</span>
              </label>
            </div>
          </div>

          {/* معاينة الصورة */}
          {formData.image_url && (
            <div className="form-group">
              <label className="form-label">معاينة الصورة</label>
              <div className="mt-2">
                <img
                  src={formData.image_url}
                  alt="معاينة المنتج"
                  className="h-32 w-32 object-cover rounded-lg border border-gray-200"
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              </div>
            </div>
          )}

          {/* معلومات إضافية للمنتج الحالي */}
          {product && (
            <div className="bg-gray-50 p-3 rounded-lg border border-gray-200">
              <h4 className="font-medium text-gray-700 mb-2">إحصائيات المنتج:</h4>
              <div className="text-sm text-gray-600 grid grid-cols-2 gap-2">
                <p>عمليات البحث: <strong>{product.search_count || 0}</strong></p>
                <p>المفضلة: <strong>{product.favorite_count || 0}</strong></p>
                <p>تاريخ الإضافة: <strong>{new Date(product.created_at).toLocaleDateString('ar-SA')}</strong></p>
                <p>آخر تحديث: <strong>{new Date(product.updated_at).toLocaleDateString('ar-SA')}</strong></p>
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
                product ? 'تحديث' : 'إضافة'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProductModal;
