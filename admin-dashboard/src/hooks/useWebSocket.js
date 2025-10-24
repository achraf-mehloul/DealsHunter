/**
 * Hook لـ WebSocket
 * إدارة الاتصالات في الوقت الحقيقي
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { notificationService } from '../services/websocket';

export const useWebSocket = (options = {}) => {
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);
  
  const optionsRef = useRef(options);

  // تحديث options
  useEffect(() => {
    optionsRef.current = options;
  }, [options]);

  // معالجة الرسائل الواردة
  const handleMessage = useCallback((data) => {
    setMessages(prev => [data, ...prev].slice(0, 100)); // حفظ آخر 100 رسالة
    
    if (optionsRef.current.onMessage) {
      optionsRef.current.onMessage(data);
    }
  }, []);

  // معالجة الاتصال
  const handleConnect = useCallback(() => {
    setConnected(true);
    setError(null);
    
    if (optionsRef.current.onConnect) {
      optionsRef.current.onConnect();
    }
  }, []);

  // معالجة قطع الاتصال
  const handleDisconnect = useCallback(() => {
    setConnected(false);
    
    if (optionsRef.current.onDisconnect) {
      optionsRef.current.onDisconnect();
    }
  }, []);

  // معالجة الأخطاء
  const handleError = useCallback((err) => {
    setError(err.message);
    
    if (optionsRef.current.onError) {
      optionsRef.current.onError(err);
    }
  }, []);

  // الاتصال بـ WebSocket
  const connect = useCallback(async () => {
    try {
      await notificationService.connect({
        onMessage: handleMessage,
        onConnect: handleConnect,
        onDisconnect: handleDisconnect,
        onError: handleError,
      });
    } catch (err) {
      setError(err.message);
    }
  }, [handleMessage, handleConnect, handleDisconnect, handleError]);

  // قطع الاتصال
  const disconnect = useCallback(() => {
    notificationService.disconnect();
  }, []);

  // إرسال رسالة
  const sendMessage = useCallback((type, data) => {
    if (connected) {
      notificationService.send({ type, data });
    } else {
      setError('غير متصل بخدمة WebSocket');
    }
  }, [connected]);

  // الاتصال التلقائي عند التحميل
  useEffect(() => {
    if (optionsRef.current.autoConnect !== false) {
      connect();
    }

    return () => {
      if (optionsRef.current.autoDisconnect !== false) {
        disconnect();
      }
    };
  }, [connect, disconnect]);

  // إعادة الاتصال
  const reconnect = useCallback(() => {
    disconnect();
    setTimeout(() => {
      connect();
    }, 1000);
  }, [connect, disconnect]);

  return {
    // الحالة
    connected,
    messages,
    error,
    
    // الإجراءات
    connect,
    disconnect,
    reconnect,
    sendMessage,
  };
};

export default useWebSocket;
