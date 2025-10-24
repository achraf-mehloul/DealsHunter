/**
 * الشريط الجانبي
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    {
      name: 'اللوحة الرئيسية',
      path: '/dashboard',
      icon: '📊',
      permission: 'read'
    },
    {
      name: 'المستخدمين',
      path: '/users',
      icon: '👥',
      permission: 'manage_users'
    },
    {
      name: 'المنتجات',
      path: '/products',
      icon: '📦',
      permission: 'manage_products'
    },
    {
      name: 'الإشعارات',
      path: '/notifications',
      icon: '🔔',
      permission: 'manage_notifications'
    },
    {
      name: 'الإعدادات',
      path: '/settings',
      icon: '⚙️',
      permission: 'manage_settings',
      children: [
        {
          name: 'إعدادات API',
          path: '/settings/api',
          icon: '🔑'
        },
        {
          name: 'إعدادات البوت',
          path: '/settings/bot',
          icon: '🤖'
        }
      ]
    }
  ];

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <div className="bg-gray-800 text-white w-64 min-h-screen flex flex-col">
      {/* الشعار */}
      <div className="p-6 border-b border-gray-700">
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <div className="h-10 w-10 bg-primary-500 rounded-lg flex items-center justify-center">
            <span className="text-xl">🤖</span>
          </div>
          <div>
            <h2 className="text-lg font-bold">Amazon Bot</h2>
            <p className="text-gray-400 text-sm">لوحة التحكم</p>
          </div>
        </div>
      </div>

      {/* القائمة */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {menuItems.map((item) => (
          <div key={item.path}>
            <Link
              to={item.path}
              className={`flex items-center space-x-3 rtl:space-x-reverse px-4 py-3 rounded-lg transition-colors ${
                isActive(item.path)
                  ? 'bg-primary-500 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="font-medium">{item.name}</span>
            </Link>

            {/* العناصر الفرعية */}
            {item.children && isActive(item.path) && (
              <div className="mt-2 mr-8 space-y-1">
                {item.children.map((child) => (
                  <Link
                    key={child.path}
                    to={child.path}
                    className={`flex items-center space-x-2 rtl:space-x-reverse px-4 py-2 rounded-lg text-sm transition-colors ${
                      isActive(child.path)
                        ? 'bg-gray-700 text-white'
                        : 'text-gray-400 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    <span>{child.icon}</span>
                    <span>{child.name}</span>
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>

      {/* التذييل */}
      <div className="p-4 border-t border-gray-700">
        <div className="bg-gray-700 rounded-lg p-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-300">حالة النظام</span>
            <span className="h-2 w-2 bg-green-500 rounded-full"></span>
          </div>
          <div className="text-xs text-gray-400">
            <div>المستخدمون: <span className="text-green-400">✓ نشط</span></div>
            <div>البوت: <span className="text-green-400">✓ يعمل</span></div>
            <div>API: <span className="text-green-400">✓ متصل</span></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
