/**
 * مخطط نمو المستخدمين
 */

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const UserGrowth = ({ data = [], period = '7d' }) => {
  // بيانات تجريبية إذا لم توجد بيانات
  const chartData = data.length > 0 ? data : [
    { date: '2024-01-01', users: 100, newUsers: 10 },
    { date: '2024-01-02', users: 120, newUsers: 8 },
    { date: '2024-01-03', users: 135, newUsers: 15 },
    { date: '2024-01-04', users: 150, newUsers: 12 },
    { date: '2024-01-05', users: 170, newUsers: 20 },
    { date: '2024-01-06', users: 185, newUsers: 15 },
    { date: '2024-01-07', users: 200, newUsers: 18 }
  ];

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
          <p className="font-medium text-gray-900">{formatDate(label)}</p>
          <p className="text-sm text-blue-600">
            إجمالي المستخدمين: <span className="font-medium">{payload[0].value}</span>
          </p>
          <p className="text-sm text-green-600">
            مستخدمين جدد: <span className="font-medium">{payload[1].value}</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-semibold text-gray-800">📈 نمو المستخدمين</h3>
        <div className="flex space-x-2 rtl:space-x-reverse">
          <select className="text-sm border border-gray-300 rounded-lg px-3 py-1 focus:outline-none focus:ring-2 focus:ring-primary-500">
            <option value="7d">آخر 7 أيام</option>
            <option value="30d">آخر 30 يوم</option>
            <option value="90d">آخر 90 يوم</option>
          </select>
        </div>
      </div>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
            <Legend />
            <Line 
              type="monotone" 
              dataKey="users" 
              stroke="#3b82f6" 
              strokeWidth={3}
              dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, fill: '#1d4ed8' }}
              name="إجمالي المستخدمين"
            />
            <Line 
              type="monotone" 
              dataKey="newUsers" 
              stroke="#10b981" 
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ fill: '#10b981', strokeWidth: 2, r: 3 }}
              name="مستخدمين جدد"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">
            {chartData[chartData.length - 1]?.users || 0}
          </div>
          <div className="text-sm text-gray-600">إجمالي المستخدمين</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">
            {chartData.reduce((sum, day) => sum + (day.newUsers || 0), 0)}
          </div>
          <div className="text-sm text-gray-600">مستخدمين جدد</div>
        </div>
      </div>
    </div>
  );
};

export default UserGrowth;
