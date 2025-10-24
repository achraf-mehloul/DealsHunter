/**
 * صفحة قائمة المنتجات
 */

import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import DataTable from '../../components/common/DataTable';
import ProductModal from '../../components/modals/ProductModal';

const ProductsList = () => {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const { get, post, put, del, loading } = useApi();

  // أعمدة الجدول
  const columns = [
    {
      key: 'image_url',
      title: 'الصورة',
      render: (value, product) => (
        <div className="h-12 w-12 bg-gray-200 rounded-lg flex items-center justify-center">
          {value ? (
            <img 
              src={value} 
              alt={product.name}
              className="h-12 w-12 object-cover rounded-lg"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }}
            />
          ) : null}
          <div className="h-12 w-12 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400 text-lg" style={{ display: value ? 'none' : 'flex' }}>
            📦
          </div>
        </div>
      )
    },
    {
      key: 'name',
      title: 'المنتج',
      render: (value, product) => (
        <div>
          <div className="font-medium text-gray-900 line-clamp-2">{value}</div>
          <div className="text-sm text-gray-500">ASIN: {product.asin}</div>
        </div>
      )
    },
    {
      key: 'price',
      title: 'السعر',
      render: (value, product) => (
        <div>
          <div className="font-bold text-green-600">${value}</div>
          {product.original_price > value && (
            <div className="text-sm text-gray-500 line-through">${product.original_price}</div>
          )}
        </div>
      )
    },
    {
      key: 'rating',
      title: 'التقييم',
      render: (value) => (
        <div className="flex items-center space-x-1 rtl:space-x-reverse">
          <span className="text-yellow-400">⭐</span>
          <span className="font-medium">{value || 'N/A'}</span>
        </div>
      )
    },
    {
      key: 'category',
      title: 'الفئة',
      render: (value) => (
        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
          {value || 'غير محدد'}
        </span>
      )
    },
    {
      key: 'prime_eligible',
      title: 'Prime',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value 
            ? 'bg-orange-100 text-orange-800'
            : 'bg-gray-100 text-gray-800'
        }`}>
          {value ? '✓' : '✗'}
        </span>
      )
    }
  ];

  // جلب المنتجات
  const fetchProducts = async () => {
    try {
      const response = await get('/products');
      setProducts(response.products || []);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  // إضافة/تعديل منتج
  const handleSaveProduct = async (productData, productId) => {
    try {
      if (productId) {
        await put(`/products/${productId}`, productData);
      } else {
        await post('/products', productData);
      }
      
      setIsModalOpen(false);
      setSelectedProduct(null);
      fetchProducts();
    } catch (error) {
      console.error('Error saving product:', error);
    }
  };

  // حذف منتج
  const handleDeleteProduct = async (product) => {
    if (window.confirm(`هل أنت متأكد من حذف المنتج "${product.name}"؟`)) {
      try {
        await del(`/products/${product.id}`);
        fetchProducts();
      } catch (error) {
        console.error('Error deleting product:', error);
      }
    }
  };

  // تصفية المنتجات
  const filteredProducts = products.filter(product =>
    product.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.asin?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.category?.toLowerCase().includes(searchTerm.toLowerCase())
  ).filter(product => 
    !categoryFilter || product.category === categoryFilter
  );

  // الفئات المتاحة
  const categories = [...new Set(products.map(p => p.category).filter(Boolean))];

  return (
    <div className="space-y-6">
      {/* الرأس */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">📦 إدارة المنتجات</h1>
          <p className="text-gray-600 mt-1">عرض وإدارة منتجات أمازون في النظام</p>
        </div>
        <button
          onClick={() => {
            setSelectedProduct(null);
            setIsModalOpen(true);
          }}
          className="btn btn-primary"
        >
          ➕ إضافة منتج
        </button>
      </div>

      {/* الإحصائيات */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="stat-card">
          <div className="stat-value text-blue-600">{products.length}</div>
          <div className="stat-label">إجمالي المنتجات</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-green-600">
            {products.filter(p => p.prime_eligible).length}
          </div>
          <div className="stat-label">منتجات Prime</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-purple-600">
            {products.reduce((sum, p) => sum + (p.search_count || 0), 0)}
          </div>
          <div className="stat-label">عمليات البحث</div>
        </div>
        <div className="stat-card">
          <div className="stat-value text-orange-600">
            {products.reduce((sum, p) => sum + (p.favorite_count || 0), 0)}
          </div>
          <div className="stat-label">إضافات للمفضلة</div>
        </div>
      </div>

      {/* البحث والتصفية */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex-1 max-w-md">
            <input
              type="text"
              placeholder="ابحث باسم المنتج، ASIN، أو الفئة..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="form-input"
            />
          </div>
          <div className="flex space-x-3 rtl:space-x-reverse">
            <select 
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="form-select w-40"
            >
              <option value="">جميع الفئات</option>
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
            <select className="form-select w-32">
              <option value="">الكل</option>
              <option value="prime">Prime فقط</option>
              <option value="discount">بخصم</option>
            </select>
          </div>
        </div>
      </div>

      {/* جدول المنتجات */}
      <div className="bg-white rounded-lg shadow-md">
        <DataTable
          columns={columns}
          data={filteredProducts}
          loading={loading}
          onEdit={(product) => {
            setSelectedProduct(product);
            setIsModalOpen(true);
          }}
          onDelete={handleDeleteProduct}
          selectable={true}
          pagination={true}
          pageSize={10}
        />
      </div>

      {/* نافذة إضافة/تعديل المنتج */}
      <ProductModal
        product={selectedProduct}
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedProduct(null);
        }}
        onSave={handleSaveProduct}
        loading={loading}
      />
    </div>
  );
};

export default ProductsList;
