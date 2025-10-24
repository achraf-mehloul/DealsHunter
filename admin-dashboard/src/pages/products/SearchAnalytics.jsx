/**
 * صفحة تحليلات البحث
 */

import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import ProductAnalytics from '../../components/charts/ProductAnalytics';

const SearchAnalytics = () => {
  const [analytics, setAnalytics] = useState({});
  const [timePeriod, setTimePeriod] = useState('7d');
  const [loading, setLoading] = useState(true);
  const { get } = useApi();

  useEffect(() => {
    fetchAnalytics();
  }, [timePeriod]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await get(`/analytics/products?period=${timePeriod}`);
      setAnalytics(response);
    } catch (error) {
      console.error('Error fetching analytics:', error);
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

  return (
    <div className="space-y-6">
      {/* الرأس */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">📊 تحليلات البحث</h1>
          <p className="text-gray-600 mt-1">تحليلات وإحصائيات عمليات البحث عن المنتجات</p>
        </div>
        <select
          value={timePeriod}
          onChange={(e) => setTimePeriod(e.target.value)}
          className="form-select w-40"
        >
          <option value="today">اليوم</option>
          <option value="yesterday">أمس</option>
          <option value="7d">آخر 7 أيام</option>
          <option value="30d">آخر 30 يوم</option>
          <option value="90d">آخر 90 يوم</option>
        </select>
      </div>

      {/* الإحصائيات السريعة */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="stat-card">
          <div className="stat-value text-blue-600">{analytics.total_products || 0}</div>
          <div className="stat-label">إجمالي المنتجات</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-green-600">{analytics.products_added || 0}</div>
          <div className="stat-label">منتجات مضافة</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-purple-600">{analytics.total_searches || 0}</div>
          <div className="stat-label">عمليات البحث</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-orange-600">
            {analytics.popular_categories?.[0]?.count || 0}
          </div>
          <div className="stat-label">أعلى فئة</div>
        </div>
      </div>

      {/* المخططات */}
      <ProductAnalytics data={analytics} />

      {/* الفئات الشائعة */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">🏷️ الفئات الشائعة</h3>
        <div className="space-y-3">
          {analytics.popular_categories?.map((category, index) => (
            <div key={category.category} className="flex items-center justify-between">
              <div className="flex items-center space-x-3 rtl:space-x-reverse">
                <span className="text-lg">{index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '📌'}</span>
                <span className="font-medium">{category.category}</span>
              </div>
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <span className="font-bold text-blue-600">{category.count}</span>
                <span className="text-sm text-gray-500">بحث</span>
              </div>
            </div>
          )) || (
            <p className="text-gray-500 text-center py-4">لا توجد بيانات للعرض</p>
          )}
        </div>
      </div>

      {/* عمليات البحث الشائعة */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">🔍 عمليات البحث الشائعة</h3>
        <div className="space-y-3">
          {analytics.popular_queries?.map((query, index) => (
            <div key={query.query} className="flex items-center justify-between">
              <div className="flex items-center space-x-3 rtl:space-x-reverse">
                <span className="text-lg">{index === 0 ? '🔥' : index === 1 ? '⚡' : index === 2 ? '🎯' : '🔍'}</span>
                <span className="font-medium">{query.query}</span>
              </div>
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <span className="font-bold text-green-600">{query.count}</span>
                <span className="text-sm text-gray-500">مرة</span>
              </div>
            </div>
          )) || (
            <p className="text-gray-500 text-center py-4">لا توجد بيانات للعرض</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchAnalytics;
