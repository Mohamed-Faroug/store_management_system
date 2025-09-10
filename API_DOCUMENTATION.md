# وثائق API - API Documentation

## 📋 نظرة عامة

نظام إدارة المخزون يوفر واجهة برمجية (API) شاملة للتفاعل مع جميع وظائف النظام.

## 🔗 Base URL

```
http://localhost:5000/api
```

## 🔐 المصادقة

### تسجيل الدخول
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

**الاستجابة:**
```json
{
    "success": true,
    "message": "تم تسجيل الدخول بنجاح",
    "user": {
        "id": 1,
        "username": "admin",
        "role": "manager"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### تسجيل الخروج
```http
POST /api/auth/logout
Authorization: Bearer <token>
```

**الاستجابة:**
```json
{
    "success": true,
    "message": "تم تسجيل الخروج بنجاح"
}
```

## 📦 الأصناف (Items)

### الحصول على جميع الأصناف
```http
GET /api/items
Authorization: Bearer <token>
```

**الاستجابة:**
```json
{
    "success": true,
    "items": [
        {
            "id": 1,
            "name": "منتج 1",
            "description": "وصف المنتج",
            "category_id": 1,
            "price": 100.0,
            "cost": 80.0,
            "stock_quantity": 50,
            "min_stock_level": 10,
            "barcode": "123456789",
            "created_at": "2025-09-10T10:00:00Z"
        }
    ]
}
```

### الحصول على صنف محدد
```http
GET /api/items/{id}
Authorization: Bearer <token>
```

### إضافة صنف جديد
```http
POST /api/items
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "منتج جديد",
    "description": "وصف المنتج",
    "category_id": 1,
    "price": 100.0,
    "cost": 80.0,
    "stock_quantity": 50,
    "min_stock_level": 10,
    "barcode": "123456789"
}
```

### تحديث صنف
```http
PUT /api/items/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "منتج محدث",
    "price": 120.0
}
```

### حذف صنف
```http
DELETE /api/items/{id}
Authorization: Bearer <token>
```

## 🏷️ الفئات (Categories)

### الحصول على جميع الفئات
```http
GET /api/categories
Authorization: Bearer <token>
```

### إضافة فئة جديدة
```http
POST /api/categories
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "فئة جديدة",
    "description": "وصف الفئة"
}
```

### تحديث فئة
```http
PUT /api/categories/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "فئة محدثة"
}
```

### حذف فئة
```http
DELETE /api/categories/{id}
Authorization: Bearer <token>
```

## 💰 المبيعات (Sales)

### الحصول على جميع المبيعات
```http
GET /api/sales
Authorization: Bearer <token>
```

### إضافة مبيعة جديدة
```http
POST /api/sales
Authorization: Bearer <token>
Content-Type: application/json

{
    "customer_name": "عميل 1",
    "items": [
        {
            "item_id": 1,
            "quantity": 2,
            "price": 100.0
        }
    ],
    "payment_method": "cash",
    "total_amount": 200.0
}
```

### الحصول على مبيعة محددة
```http
GET /api/sales/{id}
Authorization: Bearer <token>
```

## 📦 المشتريات (Purchases)

### الحصول على جميع المشتريات
```http
GET /api/purchases
Authorization: Bearer <token>
```

### إضافة مشتريات جديدة
```http
POST /api/purchases
Authorization: Bearer <token>
Content-Type: application/json

{
    "supplier_name": "مورد 1",
    "items": [
        {
            "item_id": 1,
            "quantity": 10,
            "cost": 80.0
        }
    ],
    "payment_method": "cash",
    "total_amount": 800.0
}
```

## 📊 التقارير (Reports)

### تقرير المبيعات اليومية
```http
GET /api/reports/sales/daily?date=2025-09-10
Authorization: Bearer <token>
```

### تقرير المبيعات الشهرية
```http
GET /api/reports/sales/monthly?year=2025&month=9
Authorization: Bearer <token>
```

### تقرير المبيعات السنوية
```http
GET /api/reports/sales/yearly?year=2025
Authorization: Bearer <token>
```

### تقرير المخزون
```http
GET /api/reports/inventory
Authorization: Bearer <token>
```

## 👥 المستخدمين (Users)

### الحصول على جميع المستخدمين
```http
GET /api/users
Authorization: Bearer <token>
```

### إضافة مستخدم جديد
```http
POST /api/users
Authorization: Bearer <token>
Content-Type: application/json

{
    "username": "user1",
    "password": "password123",
    "role": "clerk"
}
```

### تحديث مستخدم
```http
PUT /api/users/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "username": "user1_updated",
    "role": "manager"
}
```

### حذف مستخدم
```http
DELETE /api/users/{id}
Authorization: Bearer <token>
```

## ⚙️ الإعدادات (Settings)

### الحصول على إعدادات المتجر
```http
GET /api/settings/store
Authorization: Bearer <token>
```

### تحديث إعدادات المتجر
```http
PUT /api/settings/store
Authorization: Bearer <token>
Content-Type: application/json

{
    "store_name": "متجر جديد",
    "address": "العنوان الجديد",
    "phone": "0123456789",
    "email": "store@example.com"
}
```

### الحصول على طرق الدفع
```http
GET /api/settings/payment-methods
Authorization: Bearer <token>
```

### إضافة طريقة دفع جديدة
```http
POST /api/settings/payment-methods
Authorization: Bearer <token>
Content-Type: application/json

{
    "id": "new_method",
    "name": "طريقة دفع جديدة",
    "enabled": true
}
```

### تحديث طريقة دفع
```http
PUT /api/settings/payment-methods/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "طريقة دفع محدثة",
    "enabled": false
}
```

### حذف طريقة دفع
```http
DELETE /api/settings/payment-methods/{id}
Authorization: Bearer <token>
```

## 📈 الإحصائيات (Statistics)

### إحصائيات عامة
```http
GET /api/statistics
Authorization: Bearer <token>
```

**الاستجابة:**
```json
{
    "success": true,
    "statistics": {
        "total_items": 150,
        "total_sales": 2500.0,
        "total_purchases": 1800.0,
        "low_stock_items": 5,
        "total_customers": 100,
        "total_suppliers": 20
    }
}
```

### إحصائيات المبيعات
```http
GET /api/statistics/sales?period=daily
Authorization: Bearer <token>
```

### إحصائيات المخزون
```http
GET /api/statistics/inventory
Authorization: Bearer <token>
```

## 🔍 البحث (Search)

### البحث في الأصناف
```http
GET /api/search/items?q=منتج
Authorization: Bearer <token>
```

### البحث في المبيعات
```http
GET /api/search/sales?q=عميل
Authorization: Bearer <token>
```

### البحث في المشتريات
```http
GET /api/search/purchases?q=مورد
Authorization: Bearer <token>
```

## 📁 إدارة البيانات (Data Management)

### تصدير البيانات
```http
GET /api/data/export?type=all
Authorization: Bearer <token>
```

### استيراد البيانات
```http
POST /api/data/import
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <excel_file>
```

### إنشاء نسخة احتياطية
```http
POST /api/data/backup
Authorization: Bearer <token>
```

### استعادة نسخة احتياطية
```http
POST /api/data/restore
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <backup_file>
```

## 🚨 رموز الحالة (Status Codes)

| الكود | المعنى | الوصف |
|-------|--------|--------|
| 200 | OK | الطلب نجح |
| 201 | Created | تم إنشاء المورد |
| 400 | Bad Request | طلب غير صحيح |
| 401 | Unauthorized | غير مصرح |
| 403 | Forbidden | ممنوع |
| 404 | Not Found | غير موجود |
| 500 | Internal Server Error | خطأ في الخادم |

## 📝 أمثلة الاستخدام

### Python
```python
import requests

# تسجيل الدخول
response = requests.post('http://localhost:5000/api/auth/login', json={
    'username': 'admin',
    'password': 'admin123'
})
token = response.json()['token']

# الحصول على الأصناف
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/items', headers=headers)
items = response.json()['items']
```

### JavaScript
```javascript
// تسجيل الدخول
const loginResponse = await fetch('http://localhost:5000/api/auth/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'admin123'
    })
});
const { token } = await loginResponse.json();

// الحصول على الأصناف
const itemsResponse = await fetch('http://localhost:5000/api/items', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});
const { items } = await itemsResponse.json();
```

### cURL
```bash
# تسجيل الدخول
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# الحصول على الأصناف
curl -X GET http://localhost:5000/api/items \
  -H "Authorization: Bearer <token>"
```

## 🔒 الأمان

### المصادقة
- جميع الطلبات تتطلب مصادقة
- استخدام JWT tokens
- انتهاء صلاحية الرموز

### التفويض
- فحص الصلاحيات لكل طلب
- أدوار مختلفة للمستخدمين
- حماية من الوصول غير المصرح به

### حماية البيانات
- تشفير البيانات الحساسة
- حماية من SQL Injection
- التحقق من صحة البيانات

## 📊 الحدود (Rate Limits)

- **100 طلب/دقيقة** لكل مستخدم
- **1000 طلب/ساعة** لكل مستخدم
- **10000 طلب/يوم** لكل مستخدم

## 🐛 معالجة الأخطاء

### تنسيق الخطأ
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "البيانات المدخلة غير صحيحة",
        "details": {
            "field": "name",
            "message": "اسم المنتج مطلوب"
        }
    }
}
```

### أنواع الأخطاء
- **VALIDATION_ERROR**: خطأ في التحقق من البيانات
- **AUTHENTICATION_ERROR**: خطأ في المصادقة
- **AUTHORIZATION_ERROR**: خطأ في التفويض
- **NOT_FOUND**: المورد غير موجود
- **INTERNAL_ERROR**: خطأ داخلي

## 📚 موارد إضافية

### الروابط المفيدة
- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)

### الأدوات المقترحة
- [Postman](https://www.postman.com/) - اختبار API
- [Insomnia](https://insomnia.rest/) - عميل REST
- [curl](https://curl.se/) - أداة سطر الأوامر

---

**آخر تحديث**: 10 سبتمبر 2025
**الإصدار**: 1.0.0
**المطور**: محمد فاروق

*للمزيد من المعلومات، يرجى التواصل معنا على [mfh1134@gmail.com](mailto:mfh1134@gmail.com)*
