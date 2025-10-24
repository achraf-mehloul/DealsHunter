/**
 * خدمة API
 * إدارة جميع طلبات HTTP للخلفية
 */

import axios from 'axios';

// عنوان API الأساسي
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// إنشاء instance من axios
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// interceptor لإضافة token للمصادقة
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// interceptor لمعالجة الاستجابات
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // معالجة أخطاء المصادقة
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

// خدمة API الرئيسية
export const apiService = {
  // طلبات HTTP الأساسية
  get: (url, config = {}) => apiClient.get(url, config),
  
  post: (url, data = {}, config = {}) => apiClient.post(url, data, config),
  
  put: (url, data = {}, config = {}) => apiClient.put(url, data, config),
  
  patch: (url, data = {}, config = {}) => apiClient.patch(url, data, config),
  
  delete: (url, config = {}) => apiClient.delete(url, config),
  
  // طلبات محددة للتطبيق
  auth: {
    login: (credentials) => apiClient.post('/auth/login', credentials),
    logout: () => apiClient.post('/auth/logout'),
    getCurrentUser: () => apiClient.get('/auth/me'),
    refreshToken: () => apiClient.post('/auth/refresh'),
  },
  
  users: {
    list: (params = {}) => apiClient.get('/users', { params }),
    get: (userId) => apiClient.get(`/users/${userId}`),
    create: (userData) => apiClient.post('/users', userData),
    update: (userId, userData) => apiClient.put(`/users/${userId}`, userData),
    delete: (userId) => apiClient.delete(`/users/${userId}`),
    stats: () => apiClient.get('/users/stats'),
  },
  
  products: {
    list: (params = {}) => apiClient.get('/products', { params }),
    get: (productId) => apiClient.get(`/products/${productId}`),
    search: (query, filters = {}) => apiClient.post('/products/search', { query, filters }),
    analytics: () => apiClient.get('/products/analytics'),
    popular: () => apiClient.get('/products/popular'),
  },
  
  notifications: {
    list: (params = {}) => apiClient.get('/notifications', { params }),
    create: (notificationData) => apiClient.post('/notifications', notificationData),
    send: (notificationId) => apiClient.post(`/notifications/${notificationId}/send`),
    broadcast: (message) => apiClient.post('/notifications/broadcast', { message }),
    rules: {
      list: () => apiClient.get('/notification-rules'),
      create: (ruleData) => apiClient.post('/notification-rules', ruleData),
      update: (ruleId, ruleData) => apiClient.put(`/notification-rules/${ruleId}`, ruleData),
      delete: (ruleId) => apiClient.delete(`/notification-rules/${ruleId}`),
    },
  },
  
  analytics: {
    dashboard: () => apiClient.get('/analytics/dashboard'),
    users: (period = '7d') => apiClient.get(`/analytics/users?period=${period}`),
    products: (period = '7d') => apiClient.get(`/analytics/products?period=${period}`),
    searches: (period = '7d') => apiClient.get(`/analytics/searches?period=${period}`),
  },
  
  settings: {
    get: () => apiClient.get('/settings'),
    update: (settingsData) => apiClient.put('/settings', settingsData),
    testAmazonApi: (credentials) => apiClient.post('/settings/test-amazon-api', credentials),
    testTelegramBot: (token) => apiClient.post('/settings/test-telegram-bot', { token }),
  },
};

export default apiService;
