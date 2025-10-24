/**
 * صفحة تفاصيل المستخدم
 */

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useApi } from '../../hooks/useApi';

const UserDetail = () => {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [userStats, setUserStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const { get } = useApi();

  useEffect(() => {
    fetchUserDetails();
  }, [userId]);

  const fetchUserDetails = async () => {
    try {
      setLoading(true);
      const [userResponse, statsResponse] = await Promise.all([
        get(`/users/${userId}`),
        get('/users/stats')
      ]);
      
      setUser(userResponse);
      setUserStats(statsResponse);
    } catch (error) {
      console.error('Error fetching user details:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">😕</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">المستخدم غير موجود</h2>
        <p className="text-gray-600 mb-4">لم يتم العثور على المستخدم المطلوب</p>
        <Link to="/users" className="btn btn-primary">
          العودة لقائمة المستخدمين
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* رأس الصفحة */}
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center space-x-3 rtl:space-x-reverse mb-2">
            <Link to="/users" className="text-primary-600 hover:text-primary-700">
              ← العودة للمستخدمين
            </Link>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">👤 تفاصيل المستخدم</h1>
        </div>
        <button className="btn btn-outline">
          ✏️ تعديل
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* المعلومات الأساسية */}
        <div className="lg:col-span-2 space-y-6">
          {/* البطاقة الرئيسية */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex items-center space-x-4 rtl:space-x-reverse mb-6">
              <div className="h-16 w-16 bg-primary-500 rounded-full flex items-center justify-center">
                <span className="text-white text-2xl font-bold">
                  {user.first_name?.charAt(0) || 'U'}
                </span>
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">
                  {user.first_name} {user.last_name || ''}
                </h2>
                <p className="text-gray-600">
                  {user.username ? `@${user.username}` : 'بدون اسم مستخدم'}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-500">معرف التليجرام</label>
                <p className="mt-1 text-sm text-gray-900 font-mono">{user.telegram_id}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-500">الدور</label>
                <span className={`mt-1 inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                  user.role === 'admin' 
                    ? 'bg-red-100 text-red-800'
                    : user.role === 'moderator'
                    ? 'bg-blue-100 text-blue-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {user.role === 'admin' ? 'مدير' : user.role === 'moderator' ? 'مشرف' : 'مستخدم'}
                </span>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-500">الحالة</label>
                <span className={`mt-1 inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                  user.is_active 
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {user.is_active ? 'نشط' : 'غير نشط'}
                </span>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-500">الإشعارات</label>
                <span className={`mt-1 inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                  user.notifications_enabled 
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {user.notifications_enabled ? 'مفعّلة' : 'معطّلة'}
                </span>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-500">اللغة</label>
                <p className="mt-1 text-sm text-gray-900">
                  {user.language_code === 'ar' ? 'العربية' : 'English'}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-500">تاريخ التسجيل</label>
                <p className="mt-1 text-sm text-gray-900">
                  {new Date(user.created_at).toLocaleDateString('ar-SA')}
                </p>
              </div>
            </div>
          </div>

          {/* الإحصائيات */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📊 إحصائيات المستخدم</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">0</div>
                <div className="text-sm text-gray-600">عمليات البحث</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">0</div>
                <div className="text-sm text-gray-600">منتجات مفضلة</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">0</div>
                <div className="text-sm text-gray-600">إشعارات مستلمة</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">0</div>
                <div className="text-sm text-gray-600">آخر نشاط</div>
              </div>
            </div>
          </div>
        </div>

        {/* الجانب الأيمن */}
        <div className="space-y-6">
          {/* الإجراءات السريعة */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">⚡ إجراءات سريعة</h3>
            <div className="space-y-3">
              <button className="w-full btn btn-outline justify-start">
                🔔 إرسال إشعار
              </button>
              <button className="w-full btn btn-outline justify-start">
                📧 إرسال بريد
              </button>
              <button className="w-full btn btn-outline justify-start">
                🔄 تفعيل/تعطيل
              </button>
              <button className="w-full btn btn-outline justify-start text-red-600 border-red-200 hover:bg-red-50">
                🗑️ حذف المستخدم
              </button>
            </div>
          </div>

          {/* معلومات النظام */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">ℹ️ معلومات النظام</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">معرف المستخدم:</span>
                <span className="font-medium">{user.id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">تاريخ التسجيل:</span>
                <span className="font-medium">
                  {new Date(user.created_at).toLocaleDateString('ar-SA')}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">آخر تحديث:</span>
                <span className="font-medium">
                  {new Date(user.updated_at).toLocaleDateString('ar-SA')}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">آخر نشاط:</span>
                <span className="font-medium text-gray-400">غير معروف</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDetail;