/**
 * Hook للاتصال بالـ API
 * إدارة طلبات API مع معالجة الأخطاء
 */

import { useState, useCallback } from 'react';
import { apiService } from '../services/api';
import { useNotification } from './useNotification';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { showError } = useNotification();

  // دالة لتنفيذ طلبات API
  const callApi = useCallback(async (apiCall, successMessage = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiCall();
      
      if (successMessage) {
        // showSuccess(successMessage); // يمكن تفعيله لاحقاً
      }
      
      return response;
    } catch (err) {
      const errorMessage = err.response?.data?.message || err.message || 'حدث خطأ غير متوقع';
      setError(errorMessage);
      showError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [showError]);

  // طلبات CRUD الأساسية
  const get = useCallback((url, config = {}) => 
    callApi(() => apiService.get(url, config)), [callApi]);

  const post = useCallback((url, data = {}, config = {}) => 
    callApi(() => apiService.post(url, data, config)), [callApi]);

  const put = useCallback((url, data = {}, config = {}) => 
    callApi(() => apiService.put(url, data, config)), [callApi]);

  const patch = useCallback((url, data = {}, config = {}) => 
    callApi(() => apiService.patch(url, data, config)), [callApi]);

  const del = useCallback((url, config = {}) => 
    callApi(() => apiService.delete(url, config)), [callApi]);

  // مسح الخطأ
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    // الحالة
    loading,
    error,
    
    // الإجراءات
    callApi,
    get,
    post,
    put,
    patch,
    delete: del,
    clearError,
  };
};

export default useApi;
