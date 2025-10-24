"""
إدارة اتصالات قاعدة البيانات
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from amazon_core.utils.config import config

logger = logging.getLogger(__name__)

# قاعدة النماذج
Base = declarative_base()

# محرك قاعدة البيانات
engine = create_engine(
    config.DATABASE_URL,
    echo=config.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300
)

# جلسة قاعدة البيانات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    الحصول على جلسة قاعدة البيانات
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    تهيئة قاعدة البيانات وإنشاء الجداول
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ تم تهيئة قاعدة البيانات بنجاح")
    except Exception as e:
        logger.error(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
        raise

def test_connection():
    """
    اختبار اتصال قاعدة البيانات
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✅ اتصال قاعدة البيانات نشط")
        return True
    except Exception as e:
        logger.error(f"❌ فشل في الاتصال بقاعدة البيانات: {e}")
        return False
