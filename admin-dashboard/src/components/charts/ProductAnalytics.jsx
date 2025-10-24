/**
 * مخطط تحليلات المنتجات
 */

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const ProductAnalytics = ({ data = {} }) => {
  const { popularCategories = [], searchTrends = [] } = data;

  // بيانات تجريبية
  const categoryData = popularCategories.length > 0 ? popularCategories : [
    { name: 'إلكترونيات', value: 1200 },
    { name: 'كتب', value: 800 },
    { name: 'منزل', value: 600 },
    { name: 'تجميل', value: 400 },
    { name: 'أخرى', value: 300 }
  ];

  const searchData = searchTrends.length > 0 ? searchTrends : [
    { date: '2024-01-01', searches: 450 },
    { date: '2024-01-02', searches: 520 },
    { date: '2024-01-03', searches: 480 },
    { date: '2024-01-04', searches: 610 },
    { date: '2024-01-05', searches: 550 },
    { date: '2024-01-06', searches: 490 },
    { date: '2024-01-07', searches: 530 }
  ];

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ar-SA', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{label}</p>
          <p className="text-sm text-blue-600">
            عدد عمليات البحث: <span className="font-medium">{payload[0].value}</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {/* الفئات الشائعة */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-gray-800 mb-6">📊 الفئات الشائعة</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* اتجاهات البحث */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-gray-800 mb-6">🔍 اتجاهات البحث</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={searchData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="date" 
                tickFormatter={formatDate}
                tick={{ fill: '#6b7280', fontSize: 12 }}
              />
              <YAxis 
                tick={{ fill: '#6b7280', fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar 
                dataKey="searches" 
                fill="#3b82f6" 
                radius={[4, 4, 0, 0]}
                name="عمليات البحث"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* الإحصائيات السريعة */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-md text-center">
          <div className="text-2xl font-bold text-blue-600">
            {categoryData.reduce((sum, cat) => sum + cat.value, 0).toLocaleString()}
          </div>
          <div className="text-sm text-gray-600">إجمالي عمليات البحث</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md text-center">
          <div className="text-2xl font-bold text-green-600">
            {categoryData.length}
          </div>
          <div className="text-sm text-gray-600">عدد الفئات</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md text-center">
          <div className="text-2xl font-bold text-orange-600">
            {Math.max(...categoryData.map(cat => cat.value)).toLocaleString()}
          </div>
          <div className="text-sm text-gray-600">أعلى فئة</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md text-center">
          <div className="text-2xl font-bold text-purple-600">
            {Math.round(searchData.reduce((sum, day) => sum + day.searches, 0) / searchData.length)}
          </div>
          <div className="text-sm text-gray-600">متوسط البحث/يوم</div>
        </div>
      </div>
    </div>
  );
};

export default ProductAnalytics;
