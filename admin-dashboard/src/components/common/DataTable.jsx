/**
 * جدول بيانات عام
 */

import React, { useState } from 'react';

const DataTable = ({
  columns,
  data,
  loading = false,
  onEdit,
  onDelete,
  onView,
  actions = true,
  selectable = false,
  onSelect,
  pagination = true,
  pageSize = 10
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedRows, setSelectedRows] = useState([]);

  // التقسيم الصفحي
  const totalPages = Math.ceil(data.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const paginatedData = data.slice(startIndex, startIndex + pageSize);

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      const allIds = paginatedData.map(item => item.id);
      setSelectedRows(allIds);
      onSelect?.(allIds);
    } else {
      setSelectedRows([]);
      onSelect?.([]);
    }
  };

  const handleSelectRow = (id, checked) => {
    const newSelected = checked
      ? [...selectedRows, id]
      : selectedRows.filter(rowId => rowId !== id);
    
    setSelectedRows(newSelected);
    onSelect?.(newSelected);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  if (loading) {
    return (
      <div className="table-container">
        <table className="table">
          <thead className="table-header">
            <tr>
              {selectable && (
                <th className="table-header-cell w-12">
                  <input type="checkbox" disabled />
                </th>
              )}
              {columns.map(column => (
                <th key={column.key} className="table-header-cell">
                  {column.title}
                </th>
              ))}
              {actions && <th className="table-header-cell w-32">الإجراءات</th>}
            </tr>
          </thead>
          <tbody className="table-body">
            {[...Array(5)].map((_, index) => (
              <tr key={index}>
                {selectable && (
                  <td className="table-cell">
                    <div className="skeleton h-4 w-4"></div>
                  </td>
                )}
                {columns.map(column => (
                  <td key={column.key} className="table-cell">
                    <div className="skeleton h-4 w-3/4"></div>
                  </td>
                ))}
                {actions && (
                  <td className="table-cell">
                    <div className="skeleton h-8 w-24"></div>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className="table">
        <thead className="table-header">
          <tr>
            {selectable && (
              <th className="table-header-cell w-12">
                <input
                  type="checkbox"
                  checked={selectedRows.length === paginatedData.length && paginatedData.length > 0}
                  onChange={handleSelectAll}
                />
              </th>
            )}
            {columns.map(column => (
              <th key={column.key} className="table-header-cell">
                {column.title}
              </th>
            ))}
            {actions && <th className="table-header-cell w-32">الإجراءات</th>}
          </tr>
        </thead>
        <tbody className="table-body">
          {paginatedData.map((row, index) => (
            <tr key={row.id || index} className="hover:bg-gray-50">
              {selectable && (
                <td className="table-cell">
                  <input
                    type="checkbox"
                    checked={selectedRows.includes(row.id)}
                    onChange={(e) => handleSelectRow(row.id, e.target.checked)}
                  />
                </td>
              )}
              {columns.map(column => (
                <td key={column.key} className="table-cell">
                  {column.render ? column.render(row[column.key], row) : row[column.key]}
                </td>
              ))}
              {actions && (
                <td className="table-cell">
                  <div className="flex space-x-2 rtl:space-x-reverse">
                    {onView && (
                      <button
                        onClick={() => onView(row)}
                        className="text-blue-600 hover:text-blue-800 transition-colors"
                        title="عرض"
                      >
                        👁️
                      </button>
                    )}
                    {onEdit && (
                      <button
                        onClick={() => onEdit(row)}
                        className="text-green-600 hover:text-green-800 transition-colors"
                        title="تعديل"
                      >
                        ✏️
                      </button>
                    )}
                    {onDelete && (
                      <button
                        onClick={() => onDelete(row)}
                        className="text-red-600 hover:text-red-800 transition-colors"
                        title="حذف"
                      >
                        🗑️
                      </button>
                    )}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>

      {/* التقسيم الصفحي */}
      {pagination && totalPages > 1 && (
        <div className="bg-white px-6 py-3 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-700">
              عرض {startIndex + 1} إلى {Math.min(startIndex + pageSize, data.length)} من {data.length} عنصر
            </div>
            <div className="flex space-x-2 rtl:space-x-reverse">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="px-3 py-1 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                السابق
              </button>
              
              {[...Array(totalPages)].map((_, index) => (
                <button
                  key={index + 1}
                  onClick={() => handlePageChange(index + 1)}
                  className={`px-3 py-1 border rounded-lg ${
                    currentPage === index + 1
                      ? 'bg-primary-500 text-white border-primary-500'
                      : 'border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {index + 1}
                </button>
              ))}
              
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="px-3 py-1 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                التالي
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataTable;
