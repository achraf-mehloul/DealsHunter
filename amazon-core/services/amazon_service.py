"""
خدمة أمازون
التكامل مع Amazon Product Advertising API
"""

import logging
import aiohttp
import hmac
import hashlib
import urllib.parse
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from amazon_core.utils.config import config
from amazon_core.schemas.product_schemas import ProductSearch, ProductResponse

class AmazonService:
    """خدمة للتعامل مع Amazon Product Advertising API"""
    
    def __init__(self):
        self.access_key = config.AWS_ACCESS_KEY_ID
        self.secret_key = config.AWS_SECRET_ACCESS_KEY
        self.associate_tag = config.AWS_ASSOCIATE_TAG
        self.region = config.AWS_REGION
        self.endpoint = f"https://webservices.amazon.{self.region.split('-')[0]}.com/onca/xml"
        
    async def search_products(self, search_request: ProductSearch) -> List[ProductResponse]:
        """
        البحث عن منتجات في أمازون
        
        Args:
            search_request: طلب البحث
            
        Returns:
            List[ProductResponse]: قائمة المنتجات
        """
        try:
            # بناء معاملات البحث
            params = {
                'Service': 'AWSECommerceService',
                'Operation': 'ItemSearch',
                'AWSAccessKeyId': self.access_key,
                'AssociateTag': self.associate_tag,
                'SearchIndex': 'All',
                'Keywords': search_request.query,
                'ResponseGroup': 'Images,ItemAttributes,Offers,Reviews',
                'ItemPage': search_request.page,
                'Sort': 'relevancerank'
            }
            
            # تطبيق الفلاتر
            if search_request.filters:
                filters = search_request.filters
                
                if filters.min_price:
                    params['MinimumPrice'] = int(filters.min_price * 100)  # تحويل للسنتات
                
                if filters.max_price:
                    params['MaximumPrice'] = int(filters.max_price * 100)
                
                if filters.min_rating:
                    params['MinRating'] = filters.min_rating
                
                if filters.prime_only:
                    params['DeliveryFlag'] = 'Amazon'
                
                if filters.category:
                    params['SearchIndex'] = filters.category
            
            # توقيع الطلب
            signed_params = self._sign_request(params)
            
            # إرسال الطلب
            async with aiohttp.ClientSession() as session:
                async with session.get(self.endpoint, params=signed_params) as response:
                    if response.status == 200:
                        data = await response.text()
                        return self._parse_products(data)
                    else:
                        logging.error(f"Amazon API Error: {response.status}")
                        return []
                        
        except Exception as e:
            logging.error(f"Error in Amazon API search: {e}")
            return []
    
    def _sign_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        توقيع طلب Amazon API
        
        Args:
            params: معاملات الطلب
            
        Returns:
            Dict[str, Any]: المعاملات الموقعة
        """
        # إضافة الطابع الزمني
        params['Timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # فرز المعاملات
        sorted_params = sorted(params.items())
        
        # بناء سلسلة الاستعلام
        query_string = '&'.join([f"{k}={self._percent_encode(str(v))}" for k, v in sorted_params])
        
        # بناء سلسلة التوقيع
        string_to_sign = f"GET\nwebservices.amazon.{self.region.split('-')[0]}.com\n/onca/xml\n{query_string}"
        
        # إنشاء التوقيع
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # ترميز التوقيع
        signature_b64 = self._percent_encode(signature)
        
        # إضافة التوقيع للمعاملات
        params['Signature'] = signature_b64
        
        return params
    
    def _percent_encode(self, s: str) -> str:
        """
        ترميز النسبة المئوية للنص
        
        Args:
            s: النص المراد ترميزه
            
        Returns:
            str: النص المرمز
        """
        return urllib.parse.quote(s, safe='~')
    
    def _parse_products(self, xml_data: str) -> List[ProductResponse]:
        """
        تحليل استجابة XML من أمازون
        
        Args:
            xml_data: بيانات XML
            
        Returns:
            List[ProductResponse]: قائمة المنتجات المحللة
        """
        # TODO: تنفيذ تحليل XML الفعلي
        # هذا تنفيذ مؤقت لإرجاع بيانات تجريبية
        
        products = []
        
        # بيانات تجريبية للاختبار
        sample_products = [
            {
                'id': 1,
                'asin': 'B08N5WRWNW',
                'name': 'Amazon Echo Dot (4th Gen)',
                'price': 49.99,
                'original_price': 59.99,
                'currency': 'USD',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/714Rq4k05UL._SL1000_.jpg',
                'product_url': 'https://amazon.com/dp/B08N5WRWNW',
                'rating': 4.7,
                'review_count': 25000,
                'category': 'Electronics',
                'availability': 'In Stock',
                'prime_eligible': True,
                'search_count': 0,
                'favorite_count': 0,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'id': 2,
                'asin': 'B08F7PTF53',
                'name': 'Apple AirPods Pro',
                'price': 249.99,
                'original_price': 249.99,
                'currency': 'USD', 
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/71bhWgQK-cL._SL1500_.jpg',
                'product_url': 'https://amazon.com/dp/B08F7PTF53',
                'rating': 4.6,
                'review_count': 18000,
                'category': 'Electronics',
                'availability': 'In Stock',
                'prime_eligible': True,
                'search_count': 0,
                'favorite_count': 0,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
        ]
        
        for product_data in sample_products:
            products.append(ProductResponse(**product_data))
        
        return products
    
    async def get_product_details(self, asin: str) -> Optional[ProductResponse]:
        """
        الحصول على تفاصيل منتج معين
        
        Args:
            asin: ASIN المنتج
            
        Returns:
            Optional[ProductResponse]: تفاصيل المنتج
        """
        try:
            params = {
                'Service': 'AWSECommerceService',
                'Operation': 'ItemLookup',
                'AWSAccessKeyId': self.access_key,
                'AssociateTag': self.associate_tag,
                'ItemId': asin,
                'ResponseGroup': 'Images,ItemAttributes,Offers,Reviews',
                'IdType': 'ASIN'
            }
            
            signed_params = self._sign_request(params)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.endpoint, params=signed_params) as response:
                    if response.status == 200:
                        data = await response.text()
                        return self._parse_product_detail(data, asin)
                    else:
                        logging.error(f"Amazon API Error for ASIN {asin}: {response.status}")
                        return None
                        
        except Exception as e:
            logging.error(f"Error getting product details for {asin}: {e}")
            return None
    
    def _parse_product_detail(self, xml_data: str, asin: str) -> Optional[ProductResponse]:
        """
        تحليل تفاصيل المنتج من XML
        
        Args:
            xml_data: بيانات XML
            asin: ASIN المنتج
            
        Returns:
            Optional[ProductResponse]: تفاصيل المنتج
        """
        # TODO: تنفيذ تحليل XML الفعلي
        # هذا تنفيذ مؤقت
        return None