/**
 * سياق الإشعارات
 * إدارة الإشعارات والتحديثات في الوقت الحقيقي
 */

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { notificationService } from '../services/websocket';

// أنواع الإشعارات
const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
};

// حالة أولية
const initialState = {
  notifications: [],
  unreadCount: 0,
  connected: false,
};

// أنواع الإجراءات
const ACTION_TYPES = {
  ADD_NOTIFICATION: 'ADD_NOTIFICATION',
  MARK_AS_READ: 'MARK_AS_READ',
  CLEAR_NOTIFICATIONS: 'CLEAR_NOTIFICATIONS',
  SET_CONNECTED: 'SET_CONNECTED',
  SET_UNREAD_COUNT: 'SET_UNREAD_COUNT',
};

// reducer لإدارة الحالة
const notificationReducer = (state, action) => {
  switch (action.type) {
    case ACTION_TYPES.ADD_NOTIFICATION:
      const newNotification = {
        id: Date.now(),
        timestamp: new Date(),
        ...action.payload,
      };
      
      return {
        ...state,
        notifications: [newNotification, ...state.notifications].slice(0, 50), // حفظ آخر 50 إشعار فقط
        unreadCount: state.unreadCount + 1,
      };
    
    case ACTION_TYPES.MARK_AS_READ:
      return {
        ...state,
        notifications: state.notifications.map(notification =>
          notification.id === action.payload
            ? { ...notification, read: true }
            : notification
        ),
        unreadCount: Math.max(0, state.unreadCount - 1),
      };
    
    case ACTION_TYPES.CLEAR_NOTIFICATIONS:
      return {
        ...state,
        notifications: [],
        unreadCount: 0,
      };
    
    case ACTION_TYPES.SET_CONNECTED:
      return {
        ...state,
        connected: action.payload,
      };
    
    case ACTION_TYPES.SET_UNREAD_COUNT:
      return {
        ...state,
        unreadCount: action.payload,
      };
    
    default:
      return state;
  }
};

// إنشاء السياق
const NotificationContext = createContext();

// مقدم السياق
export const NotificationProvider = ({ children }) => {
  const [state, dispatch] = useReducer(notificationReducer, initialState);

  // إضافة إشعار
  const addNotification = (notification) => {
    dispatch({
      type: ACTION_TYPES.ADD_NOTIFICATION,
      payload: notification,
    });
  };

  // تعليم إشعار كمقروء
  const markAsRead = (notificationId) => {
    dispatch({
      type: ACTION_TYPES.MARK_AS_READ,
      payload: notificationId,
    });
  };

  // مسح جميع الإشعارات
  const clearNotifications = () => {
    dispatch({ type: ACTION_TYPES.CLEAR_NOTIFICATIONS });
  };

  // إشعار نجاح
  const showSuccess = (message, title = 'نجاح') => {
    addNotification({
      type: NOTIFICATION_TYPES.SUCCESS,
      title,
      message,
    });
  };

  // إشعار خطأ
  const showError = (message, title = 'خطأ') => {
    addNotification({
      type: NOTIFICATION_TYPES.ERROR,
      title,
      message,
    });
  };

  // إشعار تحذير
  const showWarning = (message, title = 'تحذير') => {
    addNotification({
      type: NOTIFICATION_TYPES.WARNING,
      title,
      message,
    });
  };

  // إشعار معلومات
  const showInfo = (message, title = 'معلومات') => {
    addNotification({
      type: NOTIFICATION_TYPES.INFO,
      title,
      message,
    });
  };

  // الاتصال بخدمة WebSocket
  useEffect(() => {
    const connectWebSocket = async () => {
      try {
        await notificationService.connect({
          onMessage: (data) => {
            // معالجة الرسائل الواردة من WebSocket
            switch (data.type) {
              case 'NEW_USER':
                showInfo(`مستخدم جديد: ${data.data.username}`, 'مستخدم جديد');
                break;
              case 'PRICE_DROP':
                showSuccess(
                  `انخفاض سعر المنتج: ${data.data.product_name}`,
                  'انخفاض سعر'
                );
                break;
              case 'SYSTEM_ALERT':
                showWarning(data.data.message, 'تنبيه النظام');
                break;
              default:
                showInfo(data.data.message, 'تحديث');
            }
          },
          onConnect: () => {
            dispatch({ type: ACTION_TYPES.SET_CONNECTED, payload: true });
          },
          onDisconnect: () => {
            dispatch({ type: ACTION_TYPES.SET_CONNECTED, payload: false });
          },
        });
      } catch (error) {
        console.error('Failed to connect to WebSocket:', error);
        showError('فشل في الاتصال بخدمة التحديثات المباشرة');
      }
    };

    connectWebSocket();

    return () => {
      notificationService.disconnect();
    };
  }, []);

  const value = {
    // الحالة
    notifications: state.notifications,
    unreadCount: state.unreadCount,
    connected: state.connected,
    
    // الإجراءات
    addNotification,
    markAsRead,
    clearNotifications,
    showSuccess,
    showError,
    showWarning,
    showInfo,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
};

// hook لاستخدام السياق
export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};

export default NotificationContext;
