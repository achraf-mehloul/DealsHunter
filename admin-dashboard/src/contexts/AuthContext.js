/**
 * سياق المصادقة
 * إدارة حالة المستخدم والمصادقة
 */

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authService } from '../services/auth';

// حالة أولية
const initialState = {
  user: null,
  loading: true,
  error: null,
};

// أنواع الإجراءات
const ACTION_TYPES = {
  SET_LOADING: 'SET_LOADING',
  SET_USER: 'SET_USER',
  SET_ERROR: 'SET_ERROR',
  LOGOUT: 'LOGOUT',
};

// reducer لإدارة الحالة
const authReducer = (state, action) => {
  switch (action.type) {
    case ACTION_TYPES.SET_LOADING:
      return {
        ...state,
        loading: action.payload,
      };
    case ACTION_TYPES.SET_USER:
      return {
        ...state,
        user: action.payload,
        loading: false,
        error: null,
      };
    case ACTION_TYPES.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        loading: false,
        user: null,
      };
    case ACTION_TYPES.LOGOUT:
      return {
        ...initialState,
        loading: false,
      };
    default:
      return state;
  }
};

// إنشاء السياق
const AuthContext = createContext();

// مقدم السياق
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // تحميل بيانات المستخدم عند التحميل
  useEffect(() => {
    const loadUser = async () => {
      try {
        dispatch({ type: ACTION_TYPES.SET_LOADING, payload: true });
        
        const token = localStorage.getItem('admin_token');
        if (!token) {
          dispatch({ type: ACTION_TYPES.SET_LOADING, payload: false });
          return;
        }

        const userData = await authService.getCurrentUser();
        dispatch({ type: ACTION_TYPES.SET_USER, payload: userData });
      } catch (error) {
        console.error('Failed to load user:', error);
        localStorage.removeItem('admin_token');
        dispatch({ type: ACTION_TYPES.SET_ERROR, payload: 'فشل في تحميل بيانات المستخدم' });
      }
    };

    loadUser();
  }, []);

  // تسجيل الدخول
  const login = async (email, password) => {
    try {
      dispatch({ type: ACTION_TYPES.SET_LOADING, payload: true });
      
      const { user, token } = await authService.login(email, password);
      
      localStorage.setItem('admin_token', token);
      dispatch({ type: ACTION_TYPES.SET_USER, payload: user });
      
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'فشل تسجيل الدخول';
      dispatch({ type: ACTION_TYPES.SET_ERROR, payload: errorMessage });
      return { success: false, error: errorMessage };
    }
  };

  // تسجيل الخروج
  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('admin_token');
      dispatch({ type: ACTION_TYPES.LOGOUT });
    }
  };

  // تحديث بيانات المستخدم
  const updateUser = (userData) => {
    dispatch({ type: ACTION_TYPES.SET_USER, payload: userData });
  };

  const value = {
    // الحالة
    user: state.user,
    loading: state.loading,
    error: state.error,
    
    // الإجراءات
    login,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// hook لاستخدام السياق
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
