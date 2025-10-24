/**
 * خدمة WebSocket
 * إدارة الاتصالات في الوقت الحقيقي
 */

class WebSocketService {
  constructor() {
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 3000;
    this.listeners = new Map();
    this.isConnected = false;
  }

  /**
   * الاتصال بخادم WebSocket
   */
  async connect(options = {}) {
    return new Promise((resolve, reject) => {
      try {
        const token = localStorage.getItem('admin_token');
        if (!token) {
          throw new Error('No authentication token found');
        }

        const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
        this.socket = new WebSocket(`${wsUrl}?token=${token}`);

        this.socket.onopen = () => {
          console.log('WebSocket connected');
          this.isConnected = true;
          this.reconnectAttempts = 0;
          
          if (options.onConnect) {
            options.onConnect();
          }
          
          resolve();
        };

        this.socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this._handleMessage(data);
            
            if (options.onMessage) {
              options.onMessage(data);
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        this.socket.onclose = (event) => {
          console.log('WebSocket disconnected:', event.code, event.reason);
          this.isConnected = false;
          
          if (options.onDisconnect) {
            options.onDisconnect();
          }
          
          this._attemptReconnect(options);
        };

        this.socket.onerror = (error) => {
          console.error('WebSocket error:', error);
          
          if (options.onError) {
            options.onError(error);
          }
          
          reject(error);
        };

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * محاولة إعادة الاتصال
   */
  _attemptReconnect(options) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect(options).catch(error => {
          console.error('Reconnection failed:', error);
        });
      }, this.reconnectInterval);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  /**
   * معالجة الرسائل الواردة
   */
  _handleMessage(data) {
    const { type, payload } = data;
    
    // إشعار المستمعين العامين
    if (this.listeners.has('*')) {
      this.listeners.get('*').forEach(callback => {
        callback(data);
      });
    }
    
    // إشعار المستمعين لنوع محدد
    if (this.listeners.has(type)) {
      this.listeners.get(type).forEach(callback => {
        callback(payload);
      });
    }
  }

  /**
   * إرسال رسالة عبر WebSocket
   */
  send(message) {
    if (this.socket && this.isConnected) {
      this.socket.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  /**
   * إضافة مستمع للرسائل
   */
  on(eventType, callback) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, new Set());
    }
    this.listeners.get(eventType).add(callback);
  }

  /**
   * إزالة مستمع للرسائل
   */
  off(eventType, callback) {
    if (this.listeners.has(eventType)) {
      this.listeners.get(eventType).delete(callback);
    }
  }

  /**
   * قطع الاتصال
   */
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.isConnected = false;
      this.listeners.clear();
    }
  }

  /**
   * الحصول على حالة الاتصال
   */
  getConnectionStatus() {
    return this.isConnected;
  }
}

// إنشاء نسخة وحيدة من الخدمة
export const notificationService = new WebSocketService();
export default notificationService;
