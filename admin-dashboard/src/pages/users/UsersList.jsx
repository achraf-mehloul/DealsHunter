/**
 * صفحة قائمة المستخدمين
 */

import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import DataTable from '../../components/common/DataTable';
import UserModal from '../../components/modals/UserModal';

const UsersList = () => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const { get, post, put, del, loading } = useApi();

  // أعمدة الجدول
  const columns = [
    {
      key: 'telegram_id',
      title: 'معرف التليجرام',
      render: (value) => <span className="font-mono">{value}</span>
    },
    {
      key: 'username',
      title: 'اسم المستخدم',
      render: (value, user) => (
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <div className="h-8 w-8 bg-primary-500 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-medium">
              {user.first_name?.charAt(0) || 'U'}
            </span>
          </div>
      <div>
            <div className="font-medium text-gray-900">
              {user.first_name} {user.last_name || ''}
            </div>
            <div className="text-sm text-gray-500">{value || 'بدون اسم مستخدم'}</div>
          </div>
        </div>
      )
    },
    {
      key: 'role',
      title: 'الدور',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value === 'admin' 
            ? 'bg-red-100 text-red-800'
            : value === 'moderator'
            ? 'bg-blue-100 text-blue-800'
            : 'bg-gray-100 text-gray-800'
        }`}>
          {value === 'admin' ? 'مدير' : value === 'moderator' ? 'مشرف' : 'مستخدم'}
        </span>
      )
    },
    {
      key: 'is_active',
      title: 'الحالة',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value 
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        }`}>
          {value ? 'نشط' : 'غير نشط'}
        </span>
      )
    },
    {
      key: 'created_at',
      title: 'تاريخ التسجيل',
      render: (value) => new Date(value).toLocaleDateString('ar-SA')
    }
  ];

  // جلب المستخدمين
  const fetchUsers = async () => {
    try {
      const response = await get('/users');
      setUsers(response.users || []);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // إضافة/تعديل مستخدم
  const handleSaveUser = async (userData, userId) => {
    try {
      if (userId) {
        // تعديل مستخدم موجود
        await put(`/users/${userId}`, userData);
      } else {
        // إضافة مستخدم جديد
        await post('/users', userData);
      }
      
      setIsModalOpen(false);
      setSelectedUser(null);
      fetchUsers(); // إعادة تحميل البيانات
    } catch (error) {
      console.error('Error saving user:', error);
    }
  };

  // حذف مستخدم
  const handleDeleteUser = async (user) => {
    if (window.confirm(`هل أنت متأكد من حذف المستخدم "${user.first_name}"؟`)) {
      try {
        await del(`/users/${user.id}`);
        fetchUsers(); // إعادة تحميل البيانات
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  };

  // عرض مستخدم
  const handleViewUser = (user) => {
    // الانتقال لصفحة تفاصيل المستخدم
    window.location.href = `/users/${user.id}`;
  };

  // فتح نافذة الإضافة
  const handleAddUser = () => {
    setSelectedUser(null);
    setIsModalOpen(true);
  };

  // تصفية المستخدمين حسب البحث
  const filteredUsers = users.filter(user =>
    user.first_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.telegram_id?.toString().includes(searchTerm)
  );

  return (
    <div className="space-y-6">
      {/* الرأس */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">👥 إدارة المستخدمين</h1>
          <p className="text-gray-600 mt-1">إدارة مستخدمي بوت أمازون وعرض الإحصائيات</p>
        </div>
        <button
          onClick={handleAddUser}
          className="btn btn-primary"
        >
          ➕ إضافة مستخدم
        </button>
      </div>

      {/* الإحصائيات */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="stat-card">
          <div className="stat-value text-blue-600">{users.length}</div>
          <div className="stat-label">إجمالي المستخدمين</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-green-600">
            {users.filter(u => u.is_active).length}
          </div>
          <div className="stat-label">مستخدمين نشطين</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-purple-600">
            {users.filter(u => u.role === 'admin').length}
          </div>
          <div className="stat-label">مديرين</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-orange-600">
            {users.filter(u => u.notifications_enabled).length}
          </div>
          <div className="stat-label">مفعلين الإشعارات</div>
        </div>
      </div>

      {/* البحث والتصفية */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex-1 max-w-md">
            <input
              type="text"
              placeholder="ابحث بالاسم أو اسم المستخدم أو المعرف..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="form-input"
            />
          </div>
          <div className="flex space-x-3 rtl:space-x-reverse">
            <select className="form-select w-32">
              <option value="">جميع الأدوار</option>
              <option value="user">مستخدم</option>
              <option value="moderator">مشرف</option>
              <option value="admin">مدير</option>
            </select>
            <select className="form-select w-32">
              <option value="">جميع الحالات</option>
              <option value="active">نشط</option>
              <option value="inactive">غير نشط</option>
            </select>
          </div>
        </div>
      </div>

      {/* جدول المستخدمين */}
      <div className="bg-white rounded-lg shadow-md">
        <DataTable
          columns={columns}
          data={filteredUsers}
          loading={loading}
          onView={handleViewUser}
          onEdit={(user) => {
            setSelectedUser(user);
            setIsModalOpen(true);
          }}
          onDelete={handleDeleteUser}
          selectable={true}
          pagination={true}
          pageSize={10}
        />
      </div>

      {/* نافذة إضافة/تعديل المستخدم */}
      <UserModal
        user={selectedUser}
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedUser(null);
        }}
        onSave={handleSaveUser}
        loading={loading}
      />
    </div>
  );
};

export default UsersList;
