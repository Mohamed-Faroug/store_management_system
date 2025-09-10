# API Documentation - نظام إدارة المخزون

## نظرة عامة

هذا المستند يوضح واجهة البرمجة التطبيقية (API) لنظام إدارة المخزون والمبيعات. جميع الطلبات تستخدم JSON وتستجيب بـ JSON.

## Base URL
```
http://localhost:5000
```

## Authentication

جميع الطلبات تتطلب مصادقة باستخدام session cookies.

### Login
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

### Logout
```http
GET /logout
```

## Endpoints

### 1. إدارة الأصناف (Items)

#### الحصول على قائمة الأصناف
```http
GET /items
```

**Response:**
```json
{
  "success": true,
  "items": [
    {
      "id": 1,
      "name": "صنف 1",
      "price": 100.0,
      "quantity": 50,
      "category_id": 1,
      "barcode": "123456789"
    }
  ]
}
```

#### إضافة صنف جديد
```http
POST /items/new
Content-Type: application/x-www-form-urlencoded

name=صنف جديد&price=150.0&quantity=25&category_id=1&barcode=987654321
```

#### تحديث صنف
```http
POST /items/{item_id}/edit
Content-Type: application/x-www-form-urlencoded

name=صنف محدث&price=200.0&quantity=30
```

#### حذف صنف
```http
POST /items/{item_id}/delete
```

### 2. إدارة الفواتير (Invoices)

#### الحصول على قائمة الفواتير
```http
GET /invoices
```

**Query Parameters:**
- `date`: تاريخ محدد (YYYY-MM-DD)
- `customer`: اسم العميل
- `invoice`: رقم الفاتورة

**Response:**
```json
{
  "success": true,
  "invoices": [
    {
      "id": 1,
      "invoice_number": "INV-001",
      "customer_name": "عميل 1",
      "total_amount": 500.0,
      "payment_method": "cash",
      "created_at": "2025-01-01 10:00:00"
    }
  ]
}
```

#### إنشاء فاتورة جديدة
```http
POST /invoices/new
Content-Type: application/x-www-form-urlencoded

customer_name=عميل جديد&customer_phone=123456789&payment_method=cash&items_data=[{"item_id":1,"quantity":2,"price":100}]
```

#### عرض فاتورة
```http
GET /invoices/{invoice_id}
```

#### طباعة فاتورة A4
```http
GET /invoices/{invoice_id}/print
```

#### طباعة فاتورة 58mm
```http
GET /invoices/{invoice_id}/print-58mm
```

### 3. إدارة المبيعات (Sales/POS)

#### إنشاء عملية بيع
```http
POST /sales/new
Content-Type: application/x-www-form-urlencoded

items_data=[{"item_id":1,"quantity":1,"price":100}]&total_amount=100.0&payment_method=cash
```

### 4. إدارة المشتريات (Purchases)

#### الحصول على قائمة المشتريات
```http
GET /purchases
```

#### إنشاء عملية شراء
```http
POST /purchases/new
Content-Type: application/x-www-form-urlencoded

supplier_name=مورد 1&supplier_phone=123456789&payment_method=cash&items_data=[{"item_id":1,"quantity":10,"price":50}]
```

### 5. إدارة الفئات (Categories)

#### الحصول على قائمة الفئات
```http
GET /categories
```

#### إضافة فئة جديدة
```http
POST /categories/new
Content-Type: application/x-www-form-urlencoded

name=فئة جديدة&description=وصف الفئة
```

### 6. إدارة المستخدمين (Users)

#### الحصول على قائمة المستخدمين
```http
GET /users
```

#### إضافة مستخدم جديد
```http
POST /users/new
Content-Type: application/x-www-form-urlencoded

username=مستخدم جديد&password=كلمة المرور&role=clerk
```

#### تحديث مستخدم
```http
POST /users/{user_id}/edit
Content-Type: application/x-www-form-urlencoded

username=مستخدم محدث&password=كلمة مرور جديدة&role=manager
```

### 7. الإعدادات (Settings)

#### إعدادات المتجر
```http
GET /settings/store
POST /settings/api/store
```

#### إعدادات طرق الدفع
```http
GET /settings/payment-methods
POST /settings/api/payment-methods
PUT /settings/api/payment-methods/{method_id}
DELETE /settings/api/payment-methods/{method_id}
```

#### إعدادات الضرائب
```http
GET /settings/tax
POST /settings/api/tax
```

#### إعدادات العملات
```http
GET /settings/currency
POST /settings/api/currency
```

### 8. التقارير (Reports)

#### تقرير يومي
```http
GET /reports/daily?date=2025-01-01
```

#### تقرير شهري
```http
GET /reports/monthly?month=2025-01
```

#### تقرير سنوي
```http
GET /reports/yearly?year=2025
```

## Response Codes

| Code | Description |
|------|-------------|
| 200 | OK - الطلب نجح |
| 201 | Created - تم إنشاء المورد بنجاح |
| 400 | Bad Request - خطأ في البيانات المرسلة |
| 401 | Unauthorized - غير مصرح بالوصول |
| 403 | Forbidden - ممنوع الوصول |
| 404 | Not Found - المورد غير موجود |
| 500 | Internal Server Error - خطأ في الخادم |

## Error Response Format

```json
{
  "success": false,
  "message": "رسالة الخطأ",
  "error_code": "ERROR_CODE"
}
```

## Success Response Format

```json
{
  "success": true,
  "message": "تمت العملية بنجاح",
  "data": {
    // البيانات المطلوبة
  }
}
```

## Authentication Headers

```http
Cookie: session=your_session_cookie
```

## Rate Limiting

- **الحد الأقصى:** 100 طلب في الدقيقة
- **الحد الأقصى للفرد:** 10 طلبات في الثانية

## Pagination

للقوائم الطويلة، استخدم معاملات الصفحات:

```http
GET /items?page=1&per_page=20
```

**Response:**
```json
{
  "success": true,
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

## Filtering and Sorting

### Filtering
```http
GET /items?category_id=1&price_min=100&price_max=500
```

### Sorting
```http
GET /items?sort_by=name&sort_order=asc
```

## Data Validation

### Item Validation
- `name`: مطلوب، نص، 1-100 حرف
- `price`: مطلوب، رقم، أكبر من 0
- `quantity`: مطلوب، رقم صحيح، أكبر من أو يساوي 0
- `barcode`: اختياري، نص، فريد

### Invoice Validation
- `customer_name`: مطلوب، نص، 1-100 حرف
- `customer_phone`: اختياري، نص، 10-15 رقم
- `payment_method`: مطلوب، نص، من القائمة المحددة
- `items`: مطلوب، مصفوفة، غير فارغة

## Webhooks

### Invoice Created
```json
{
  "event": "invoice.created",
  "data": {
    "invoice_id": 123,
    "invoice_number": "INV-001",
    "total_amount": 500.0,
    "created_at": "2025-01-01T10:00:00Z"
  }
}
```

### Low Stock Alert
```json
{
  "event": "stock.low",
  "data": {
    "item_id": 456,
    "item_name": "صنف 1",
    "current_quantity": 5,
    "minimum_quantity": 10
  }
}
```

## SDK Examples

### Python
```python
import requests

# Login
session = requests.Session()
login_data = {
    'username': 'admin',
    'password': 'admin123'
}
session.post('http://localhost:5000/login', data=login_data)

# Get items
response = session.get('http://localhost:5000/items')
items = response.json()['items']

# Create invoice
invoice_data = {
    'customer_name': 'عميل جديد',
    'payment_method': 'cash',
    'items_data': '[{"item_id":1,"quantity":2,"price":100}]'
}
response = session.post('http://localhost:5000/invoices/new', data=invoice_data)
```

### JavaScript
```javascript
// Login
const loginData = new FormData();
loginData.append('username', 'admin');
loginData.append('password', 'admin123');

fetch('/login', {
    method: 'POST',
    body: loginData
}).then(() => {
    // Get items
    return fetch('/items');
}).then(response => response.json())
.then(data => {
    console.log(data.items);
});
```

## Testing

### Unit Tests
```bash
pytest tests/
```

### API Tests
```bash
pytest tests/api/
```

### Load Testing
```bash
# Install artillery
npm install -g artillery

# Run load test
artillery run load-test.yml
```

## Changelog

### v1.0.0
- إطلاق النسخة الأولى
- جميع الـ endpoints الأساسية
- نظام المصادقة
- إدارة الأصناف والفواتير

### v1.1.0
- إضافة تقارير متقدمة
- تحسين الأداء
- إضافة webhooks

## Support

للحصول على الدعم:
- **GitHub Issues:** [رابط GitHub]
- **Email:** support@example.com
- **Documentation:** [رابط الوثائق]

---

**تم إنشاء هذا المستند بواسطة:** محمد فاروق  
**آخر تحديث:** 2025-01-01
