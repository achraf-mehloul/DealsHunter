#!/bin/bash
# سكريبت تهيئة قاعدة البيانات

set -e

echo "🎯 بدء تهيئة قاعدة بيانات Amazon Bot..."

# الانتظار حتى يكون PostgreSQL جاهزاً
until pg_isready -U admin -d amazon_bot; do
  echo "⏳ في انتظار PostgreSQL..."
  sleep 2
done

echo "✅ PostgreSQL جاهز"

# إنشاء الجداول الأساسية
psql -v ON_ERROR_STOP=1 --username "admin" --dbname "amazon_bot" <<-EOSQL
    -- إنشاء امتداد UUID إذا لم يكن موجوداً
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- جدول المستخدمين
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE NOT NULL,
        username VARCHAR(100),
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100),
        language_code VARCHAR(10) DEFAULT 'ar',
        role VARCHAR(20) DEFAULT 'user',
        is_active BOOLEAN DEFAULT TRUE,
        notifications_enabled BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- جدول المنتجات
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        asin VARCHAR(10) UNIQUE NOT NULL,
        name VARCHAR(500) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        original_price DECIMAL(10,2),
        currency VARCHAR(10) DEFAULT 'USD',
        image_url TEXT,
        product_url TEXT NOT NULL,
        rating DECIMAL(3,2),
        review_count INTEGER DEFAULT 0,
        category VARCHAR(200),
        availability VARCHAR(100),
        prime_eligible BOOLEAN DEFAULT FALSE,
        search_count INTEGER DEFAULT 0,
        favorite_count INTEGER DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- جدول المفضلة
    CREATE TABLE IF NOT EXISTS favorites (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
        notes TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, product_id)
    );

    -- جدول الإشعارات
    CREATE TABLE IF NOT EXISTS notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        title VARCHAR(200) NOT NULL,
        message TEXT NOT NULL,
        notification_type VARCHAR(50) NOT NULL,
        status VARCHAR(20) DEFAULT 'pending',
        data JSONB,
        sent_at TIMESTAMP WITH TIME ZONE,
        read_at TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- جدول سجل البحث
    CREATE TABLE IF NOT EXISTS search_history (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        query VARCHAR(200) NOT NULL,
        filters JSONB,
        result_count INTEGER DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- جدول سجل الأسعار
    CREATE TABLE IF NOT EXISTS price_history (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
        price DECIMAL(10,2) NOT NULL,
        currency VARCHAR(10) DEFAULT 'USD',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- إنشاء الفهرس لتحسين الأداء
    CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
    CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
    CREATE INDEX IF NOT EXISTS idx_products_asin ON products(asin);
    CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
    CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
    CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);
    CREATE INDEX IF NOT EXISTS idx_favorites_product_id ON favorites(product_id);
    CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
    CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status);
    CREATE INDEX IF NOT EXISTS idx_search_history_user_id ON search_history(user_id);
    CREATE INDEX IF NOT EXISTS idx_search_history_created_at ON search_history(created_at);
    CREATE INDEX IF NOT EXISTS idx_price_history_product_id ON price_history(product_id);
    CREATE INDEX IF NOT EXISTS idx_price_history_created_at ON price_history(created_at);

    -- إدراج بيانات تجريبية
    INSERT INTO users (telegram_id, username, first_name, last_name, role) 
    VALUES 
        (123456789, 'admin_user', 'المشرف', 'النظام', 'admin')
    ON CONFLICT (telegram_id) DO NOTHING;

    INSERT INTO products (asin, name, price, original_price, currency, image_url, product_url, rating, review_count, category, prime_eligible) 
    VALUES 
        ('B08N5WRWNW', 'Amazon Echo Dot (4th Gen)', 49.99, 59.99, 'USD', 'https://images-na.ssl-images-amazon.com/images/I/714Rq4k05UL._SL1000_.jpg', 'https://amazon.com/dp/B08N5WRWNW', 4.7, 25000, 'Electronics', true),
        ('B08F7PTF53', 'Apple AirPods Pro', 249.99, 249.99, 'USD', 'https://images-na.ssl-images-amazon.com/images/I/71bhWgQK-cL._SL1500_.jpg', 'https://amazon.com/dp/B08F7PTF53', 4.6, 18000, 'Electronics', true)
    ON CONFLICT (asin) DO NOTHING;

    -- تحديث دالة updated_at
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS \$\$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    \$\$ language 'plpgsql';

    -- إنشاء triggers لتحديث updated_at
    DROP TRIGGER IF EXISTS update_users_updated_at ON users;
    CREATE TRIGGER update_users_updated_at
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();

    DROP TRIGGER IF EXISTS update_products_updated_at ON products;
    CREATE TRIGGER update_products_updated_at
        BEFORE UPDATE ON products
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();

    -- إنشاء أدوار المستخدمين
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'api_user') THEN
            CREATE ROLE api_user WITH LOGIN PASSWORD 'api_password';
        END IF;
    END
    \$\$;

    -- منح الصلاحيات
    GRANT CONNECT ON DATABASE amazon_bot TO api_user;
    GRANT USAGE ON SCHEMA public TO api_user;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO api_user;
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO api_user;

    -- إنشاء views للإحصائيات
    CREATE OR REPLACE VIEW user_stats AS
    SELECT 
        u.id,
        u.telegram_id,
        u.username,
        u.first_name,
        COUNT(DISTINCT sh.id) as total_searches,
        COUNT(DISTINCT f.id) as total_favorites,
        MAX(sh.created_at) as last_active
    FROM users u
    LEFT JOIN search_history sh ON u.id = sh.user_id
    LEFT JOIN favorites f ON u.id = f.user_id
    GROUP BY u.id, u.telegram_id, u.username, u.first_name;

    CREATE OR REPLACE VIEW product_stats AS
    SELECT 
        p.id,
        p.asin,
        p.name,
        p.price,
        COUNT(DISTINCT sh.id) as search_count,
        COUNT(DISTINCT f.id) as favorite_count,
        AVG(ph.price) as avg_price_history
    FROM products p
    LEFT JOIN search_history sh ON p.id = sh.id
    LEFT JOIN favorites f ON p.id = f.product_id
    LEFT JOIN price_history ph ON p.id = ph.product_id
    GROUP BY p.id, p.asin, p.name, p.price;

EOSQL

echo "🎉 تم تهيئة قاعدة البيانات بنجاح!"
echo "📊 الجداول المنشأة:"
echo "   - users (المستخدمين)"
echo "   - products (المنتجات)" 
echo "   - favorites (المفضلة)"
echo "   - notifications (الإشعارات)"
echo "   - search_history (سجل البحث)"
echo "   - price_history (سجل الأسعار)"
echo "   - والفهارس والـ views المساعدة"
