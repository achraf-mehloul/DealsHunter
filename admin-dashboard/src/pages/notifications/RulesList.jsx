/**
 * صفحة قواعد الإشعارات
 */

import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import DataTable from '../../components/common/DataTable';
import FilterRuleForm from '../../components/forms/FilterRuleForm';

const RulesList = () => {
  const [rules, setRules] = useState([]);
  const [selectedRule, setSelectedRule] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { get, post, put, del, loading } = useApi();

  // أعمدة الجدول
  const columns = [
    {
      key: 'name',
      title: 'اسم القاعدة',
      render: (value, rule) => (
        <div>
          <div className="font-medium text-gray-900">{value}</div>
          <div className="text-sm text-gray-500">
            {rule.condition.type === 'price_drop' && '💰 انخفاض السعر'}
            {rule.condition.type === 'new_product' && '🆕 منتج جديد'}
            {rule.condition.type === 'stock_change' && '📦 تغير المخزون'}
            {rule.condition.type === 'rating_threshold' && '⭐ حد التقييم'}
          </div>
        </div>
      )
    },
    {
      key: 'condition',
      title: 'الشرط',
      render: (value) => (
        <div className="text-sm">
          {value.type === 'price_drop' && `انخفاض ${value.threshold}%`}
          {value.type === 'new_product' && `فئة: ${value.category}`}
          {value.type === 'stock_change' && `مخزون < ${value.threshold}`}
          {value.type === 'rating_threshold' && `تقييم > ${value.threshold}`}
        </div>
      )
    },
    {
      key: 'action',
      title: 'الإجراء',
      render: (value) => (
        <div className="text-sm">
          {value.type === 'send_notification' && '🔔 إرسال إشعار'}
          {value.type === 'send_email' && '📧 إرسال بريد'}
          {value.type === 'webhook' && '🔗 استدعاء Webhook'}
        </div>
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
          {value ? 'مفعلة' : 'معطلة'}
        </span>
      )
    },
    {
      key: 'created_at',
      title: 'تاريخ الإنشاء',
      render: (value) => new Date(value).toLocaleDateString('ar-SA')
    }
  ];

  // جلب القواعد
  const fetchRules = async () => {
    try {
      const response = await get('/notifications/rules');
      setRules(response || []);
    } catch (error) {
      console.error('Error fetching rules:', error);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  // حفظ القاعدة
  const handleSaveRule = async (ruleData, ruleId) => {
    try {
      if (ruleId) {
        await put(`/notifications/rules/${ruleId}`, ruleData);
      } else {
        await post('/notifications/rules', ruleData);
      }
      
      setIsModalOpen(false);
      setSelectedRule(null);
      fetchRules();
    } catch (error) {
      console.error('Error saving rule:', error);
    }
  };

  // حذف القاعدة
  const handleDeleteRule = async (rule) => {
    if (window.confirm(`هل أنت متأكد من حذف القاعدة "${rule.name}"؟`)) {
      try {
        await del(`/notifications/rules/${rule.id}`);
        fetchRules();
      } catch (error) {
        console.error('Error deleting rule:', error);
      }
    }
  };

  // تبديل حالة القاعدة
  const handleToggleRule = async (rule) => {
    try {
      await put(`/notifications/rules/${rule.id}`, {
        ...rule,
        is_active: !rule.is_active
      });
      fetchRules();
    } catch (error) {
      console.error('Error toggling rule:', error);
    }
  };

  return (
    <div className="space-y-6">
      {/* الرأس */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">⚡ قواعد الإشعارات</h1>
          <p className="text-gray-600 mt-1">إدارة القواعد الآلية للإشعارات والتنبيهات</p>
        </div>
        <button
          onClick={() => {
            setSelectedRule(null);
            setIsModalOpen(true);
          }}
          className="btn btn-primary"
        >
          ➕ إضافة قاعدة
        </button>
      </div>

      {/* الإحصائيات */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="stat-card">
          <div className="stat-value text-blue-600">{rules.length}</div>
          <div className="stat-label">إجمالي القواعد</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-green-600">
            {rules.filter(r => r.is_active).length}
          </div>
          <div className="stat-label">قواعد مفعلة</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-purple-600">
            {rules.filter(r => r.condition.type === 'price_drop').length}
          </div>
          <div className="stat-label">قواعد أسعار</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-orange-600">
            {rules.filter(r => r.action.type === 'send_notification').length}
          </div>
          <div className="stat-label">إشعارات</div>
        </div>
      </div>

      {/* جدول القواعد */}
      <div className="bg-white rounded-lg shadow-md">
        <DataTable
          columns={columns}
          data={rules}
          loading={loading}
          onEdit={(rule) => {
            setSelectedRule(rule);
            setIsModalOpen(true);
          }}
          onDelete={handleDeleteRule}
          actions={true}
        />
      </div>

      {/* نافذة إضافة/تعديل القاعدة */}
      <FilterRuleForm
        initialData={selectedRule}
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedRule(null);
        }}
        onSave={handleSaveRule}
        loading={loading}
      />
    </div>
  );
};

export default RulesList;
