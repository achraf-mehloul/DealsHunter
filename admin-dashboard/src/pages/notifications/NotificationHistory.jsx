/**
 * صفحة سجل الإشعارات
 */

import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import DataTable from '../../components/common/DataTable';

const NotificationHistory = () => {
  const [notifications, setNotifications] = useState([]);
  const [filterType, setFilterType] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const { get, loading } = useApi();

  // أعمدة الجدول
  const columns = [
    {
      key: 'title',
      title: 'الإشعار',
      render: (value, notification) => (
        <div>
          <div className="font-medium text-gray-900">{value}</div>
          <div className="text-sm text-gray-500 line-clamp-2">{notification.message}</div>
        </div>
      )
    },
    {
      key: 'notification_type',
      title: 'النوع',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value === 'price_drop' ? 'bg-green-100 text-green-800' :
          value === 'new_product' ? 'bg-blue-100 text-blue-800' :
          value === 'system_alert' ? 'bg-orange-100 text-orange-800' :
          value === 'promotion' ? 'bg-purple-100 text-purple-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {value === 'price_drop' && '💰 انخفاض سعر'}
          {value === 'new_product' && '🆕 منتج جديد'}
          {value === 'system_alert' && '⚠️ تنبيه نظام'}
          {value === 'promotion' && '🎉 عرض ترويجي'}
          {value === 'stock_alert' && '📦 تنبيه مخزون'}
        </span>
      )
    },
    {
      key: 'status',
      title: 'الحالة',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value === 'sent' ? 'bg-green-100 text-green-800' :
          value === 'pending' ? 'bg-yellow-100 text-yellow-800' :
          value === 'failed' ? 'bg-red-100 text-red-800' :
          'bg-blue-100 text-blue-800'
        }`}>
          {value === 'sent' && '✅ مرسل'}
          {value === 'pending' && '⏳ قيد الانتظار'}
          {value === 'failed' && '❌ فشل'}
          {value === 'read' && '👁️ مقروء'}
        </span>
      )
    },
    {
      key: 'broadcast',
      title: 'النطاق',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
        }`}>
          {value ? '📢 جماعي' : '👤 فردي'}
        </span>
      )
    },
    {
      key: 'sent_at',
      title: 'وقت الإرسال',
      render: (value) => value ? new Date(value).toLocaleString('ar-SA') : 'لم يتم الإرسال'
    }
  ];

  // جلب الإشعارات
  const fetchNotifications = async () => {
    try {
      const response = await get('/notifications');
      setNotifications(response.notifications || []);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  // تصفية الإشعارات
  const filteredNotifications = notifications.filter(notification => {
    const typeMatch = !filterType || notification.notification_type === filterType;
    const statusMatch = !filterStatus || notification.status === filterStatus;
    return typeMatch && statusMatch;
  });

  return (
    <div className="space-y-6">
      {/* الرأس */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">📋 سجل الإشعارات</h1>
          <p className="text-gray-600 mt-1">عرض سجل جميع الإشعارات المرسلة في النظام</p>
        </div>
      </div>

      {/* الإحصائيات */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="stat-card">
          <div className="stat-value text-blue-600">{notifications.length}</div>
          <div className="stat-label">إجمالي الإشعارات</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-green-600">
            {notifications.filter(n => n.status === 'sent').length}
          </div>
          <div className="stat-label">مرسلة</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-orange-600">
            {notifications.filter(n => n.status === 'pending').length}
          </div>
          <div className="stat-label">قيد الانتظار</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-red-600">
            {notifications.filter(n => n.status === 'failed').length}
          </div>
          <div className="stat-label">فاشلة</div>
        </div>
      </div>

      {/* الفلاتر */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4 rtl:md:space-x-reverse">
          <div className="flex-1">
            <h3 className="text-sm font-medium text-gray-700 mb-2">تصفية النتائج:</h3>
          </div>
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="form-select w-40"
          >
            <option value="">جميع الأنواع</option>
            <option value="price_drop">انخفاض سعر</option>
            <option value="new_product">منتج جديد</option>
            <option value="system_alert">تنبيه نظام</option>
            <option value="promotion">عرض ترويجي</option>
          </select>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="form-select w-40"
          >
            <option value="">جميع الحالات</option>
            <option value="sent">مرسلة</option>
            <option value="pending">قيد الانتظار</option>
            <option value="failed">فاشلة</option>
            <option value="read">مقروءة</option>
          </select>
        </div>
      </div>

      {/* جدول الإشعارات */}
      <div className="bg-white rounded-lg shadow-md">
        <DataTable
          columns={columns}
          data={filteredNotifications}
          loading={loading}
          pagination={true}
          pageSize={10}
        />
      </div>
    </div>
  );
};

export default NotificationHistory;
