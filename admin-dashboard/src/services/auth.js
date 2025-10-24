/**
 * خدمة المصادقة
 * إدارة تسجيل الدخول والخروج والمصادقة
 */

import { apiService } from './api';

// خدمة المصادقة
export const authService = {
  /**
   * تسجيل الدخول
   */
  async login(email, password) {
    const response = await apiService.auth.login({ email, password });
    
    if (response.user && response.token) {
      // حفظ token في localStorage
      localStorage.setItem('admin_token', response.token);
      
      return {
        user: response.user,
        token: response.token,
      };
    }
    
    throw new Error('فشل تسجيل الدخول');
  },
  
  /**
   * تسجيل الخروج
   */
  async logout() {
    try {
      await apiService.auth.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // مسح token من localStorage
      localStorage.removeItem('admin_token');
    }
  },
  
  /**
   * الحصول على بيانات المستخدم الحالي
   */
  async getCurrentUser() {
    const response = await apiService.auth.getCurrentUser();
    return response.user;
  },
  
  /**
   * تحديث token
   */
  async refreshToken() {
    const response = await apiService.auth.refreshToken();
    
    if (response.token) {
      localStorage.setItem('admin_token', response.token);
      return response.token;
    }
    
    throw new Error('فشل في تحديث Token');
  },
  
  /**
   * التحقق من صلاحيات المستخدم
   */
  hasPermission(user, permission) {
    if (!user || !user.role) return false;
    
    const rolePermissions = {
      admin: ['read', 'write', 'delete', 'manage_users'],
      moderator: ['read', 'write'],
      viewer: ['read'],
    };
    
    return rolePermissions[user.role]?.includes(permission) || false;
  },
  
  /**
   * التحقق من صلاحية الدور
   */
  hasRole(user, role) {
    return user?.role === role;
  },
  
  /**
   * التحقق من تسجيل الدخول
   */
  isAuthenticated() {
    return !!localStorage.getItem('admin_token');
  },
  
  /**
   * الحصول على token
   */
  getToken() {
    return localStorage.getItem('admin_token');
  },
};

export default authService;
