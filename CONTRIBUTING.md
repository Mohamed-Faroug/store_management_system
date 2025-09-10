# دليل المساهمة - Contributing Guide

نرحب بمساهماتكم في تطوير نظام إدارة المخزون! هذا الدليل يوضح كيفية المساهمة في المشروع.

## كيفية المساهمة

### 1. الإبلاغ عن الأخطاء (Bug Reports)

#### قبل الإبلاغ
- تأكد من أن المشكلة لم يتم الإبلاغ عنها مسبقاً
- تحقق من أنك تستخدم أحدث إصدار
- جرب إعادة تشغيل التطبيق

#### عند الإبلاغ
استخدم قالب GitHub Issue التالي:

```markdown
**وصف المشكلة**
وصف واضح ومفصل للمشكلة.

**خطوات إعادة إنتاج المشكلة**
1. اذهب إلى '...'
2. اضغط على '...'
3. مرر لأسفل إلى '...'
4. شاهد الخطأ

**النتيجة المتوقعة**
ما كنت تتوقع أن يحدث.

**النتيجة الفعلية**
ما حدث فعلاً.

**لقطات الشاشة**
إذا كان ذلك مناسباً، أضف لقطات شاشة.

**معلومات إضافية**
- نظام التشغيل: [مثل Windows 10, Ubuntu 20.04]
- إصدار Python: [مثل 3.8.5]
- إصدار المتصفح: [مثل Chrome 90]
- إصدار التطبيق: [مثل 1.0.0]

**سجلات الأخطاء**
```
ضع هنا أي رسائل خطأ من console أو logs
```
```

### 2. اقتراح ميزات جديدة (Feature Requests)

#### قبل الاقتراح
- تحقق من أن الميزة لم يتم اقتراحها مسبقاً
- تأكد من أن الميزة تتناسب مع أهداف المشروع
- فكر في كيفية تنفيذ الميزة

#### عند الاقتراح
```markdown
**وصف الميزة**
وصف واضح ومفصل للميزة المقترحة.

**المشكلة التي تحلها**
ما المشكلة التي تحلها هذه الميزة؟

**الحل المقترح**
كيف تقترح تنفيذ هذه الميزة؟

**البدائل المطروحة**
هل فكرت في بدائل أخرى؟

**معلومات إضافية**
أي معلومات أخرى قد تكون مفيدة.
```

### 3. المساهمة بالكود (Code Contributions)

#### إعداد بيئة التطوير

1. **Fork المشروع**
   - اضغط على زر "Fork" في أعلى الصفحة
   - استنسخ fork إلى جهازك المحلي

2. **إعداد البيئة المحلية**
   ```bash
   # استنساخ fork
   git clone https://github.com/yourusername/inventory-management-system.git
   cd inventory-management-system
   
   # إضافة remote الأصلي
   git remote add upstream https://github.com/original-owner/inventory-management-system.git
   
   # إنشاء بيئة افتراضية
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # أو
   venv\Scripts\activate  # Windows
   
   # تثبيت المتطلبات
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # إذا كان موجود
   ```

3. **إنشاء branch جديد**
   ```bash
   git checkout -b feature/your-feature-name
   # أو
   git checkout -b fix/your-bug-fix
   ```

#### معايير الكود

1. **Python Style Guide**
   - استخدم PEP 8
   - استخدم type hints
   - اكتب docstrings شاملة

2. **JavaScript Style Guide**
   - استخدم ESLint
   - استخدم camelCase للمتغيرات
   - استخدم const/let بدلاً من var

3. **HTML/CSS Style Guide**
   - استخدم indentation متسق (2 spaces)
   - استخدم semantic HTML
   - استخدم Bootstrap classes

#### أمثلة على الكود الجيد

**Python:**
```python
def calculate_total_price(items: List[Dict[str, Any]]) -> float:
    """
    حساب السعر الإجمالي للأصناف
    
    Args:
        items: قائمة الأصناف مع الكميات والأسعار
        
    Returns:
        float: السعر الإجمالي
        
    Raises:
        ValueError: إذا كانت الكمية أو السعر سالب
    """
    if not items:
        return 0.0
    
    total = 0.0
    for item in items:
        quantity = item.get('quantity', 0)
        price = item.get('price', 0.0)
        
        if quantity < 0 or price < 0:
            raise ValueError("الكمية والسعر يجب أن يكونا موجبين")
        
        total += quantity * price
    
    return round(total, 2)
```

**JavaScript:**
```javascript
/**
 * تحديث إجمالي السلة
 * @param {Array} items - عناصر السلة
 * @returns {number} - الإجمالي
 */
function updateCartTotal(items) {
    if (!Array.isArray(items)) {
        console.error('items يجب أن يكون مصفوفة');
        return 0;
    }
    
    const total = items.reduce((sum, item) => {
        const quantity = parseInt(item.quantity) || 0;
        const price = parseFloat(item.price) || 0;
        return sum + (quantity * price);
    }, 0);
    
    return Math.round(total * 100) / 100; // تقريب لرقمين عشريين
}
```

#### كتابة الاختبارات

1. **Unit Tests**
   ```python
   # tests/test_utils.py
   import unittest
   from app.utils.payment_utils import get_payment_method_name
   
   class TestPaymentUtils(unittest.TestCase):
       def test_get_payment_method_name_cash(self):
           """اختبار الحصول على اسم طريقة الدفع النقدي"""
           result = get_payment_method_name('cash')
           self.assertEqual(result, 'نقدي')
       
       def test_get_payment_method_name_invalid(self):
           """اختبار طريقة دفع غير صحيحة"""
           result = get_payment_method_name('invalid')
           self.assertEqual(result, 'غير محدد')
   ```

2. **Integration Tests**
   ```python
   # tests/test_api.py
   import json
   from app import create_app
   
   class TestInvoiceAPI(unittest.TestCase):
       def setUp(self):
           self.app = create_app('testing')
           self.client = self.app.test_client()
       
       def test_create_invoice(self):
           """اختبار إنشاء فاتورة جديدة"""
           data = {
               'customer_name': 'عميل تجريبي',
               'payment_method': 'cash',
               'items_data': '[{"item_id":1,"quantity":2,"price":100}]'
           }
           
           response = self.client.post('/invoices/new', data=data)
           self.assertEqual(response.status_code, 302)  # redirect
   ```

#### تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
python -m pytest

# تشغيل اختبارات محددة
python -m pytest tests/test_utils.py

# تشغيل مع coverage
python -m pytest --cov=app tests/

# تشغيل مع verbose
python -m pytest -v
```

#### مراجعة الكود

1. **قبل إرسال Pull Request**
   ```bash
   # تشغيل الاختبارات
   python -m pytest
   
   # فحص الكود
   flake8 app/
   black --check app/
   isort --check-only app/
   
   # تحديث branch
   git fetch upstream
   git rebase upstream/main
   ```

2. **إرسال Pull Request**
   - تأكد من أن جميع الاختبارات تمر
   - أضف وصف واضح للتغييرات
   - أرفق لقطات شاشة إذا لزم الأمر
   - اربط Issues ذات الصلة

#### قالب Pull Request

```markdown
## وصف التغييرات
وصف مختصر للتغييرات المضافة.

## نوع التغيير
- [ ] إصلاح خطأ
- [ ] ميزة جديدة
- [ ] تحسين أداء
- [ ] تحديث وثائق
- [ ] إعادة هيكلة الكود

## الاختبارات
- [ ] تم تشغيل الاختبارات المحلية
- [ ] تم إضافة اختبارات جديدة
- [ ] جميع الاختبارات تمر

## لقطات الشاشة
إذا كان ذلك مناسباً، أضف لقطات شاشة.

## معلومات إضافية
أي معلومات أخرى قد تكون مفيدة للمراجعين.
```

## إرشادات المساهمة

### 1. رسائل Commit

استخدم تنسيق واضح لرسائل commit:

```
type(scope): description

[optional body]

[optional footer]
```

**الأ types:**
- `feat`: ميزة جديدة
- `fix`: إصلاح خطأ
- `docs`: تحديث الوثائق
- `style`: تغييرات في التنسيق
- `refactor`: إعادة هيكلة الكود
- `test`: إضافة أو تعديل الاختبارات
- `chore`: مهام الصيانة

**أمثلة:**
```
feat(invoices): add payment method display
fix(sales): resolve payment method not showing in invoices
docs(api): update authentication documentation
style(ui): improve button styling in POS
refactor(utils): extract payment utilities to separate module
```

### 2. تسمية Branches

```
feature/description
fix/description
hotfix/description
docs/description
refactor/description
```

**أمثلة:**
```
feature/payment-methods-management
fix/invoice-printing-issue
hotfix/security-vulnerability
docs/api-documentation
refactor/database-models
```

### 3. تسمية Issues

```
[Type] Brief description

Examples:
[Bug] Payment method not showing in invoices
[Feature] Add barcode scanning support
[Enhancement] Improve POS performance
[Docs] Update installation guide
```

### 4. كتابة الوثائق

1. **Docstrings للدوال**
   ```python
   def process_payment(amount: float, method: str) -> Dict[str, Any]:
       """
       معالجة عملية الدفع
       
       Args:
           amount: مبلغ الدفع
           method: طريقة الدفع
           
       Returns:
           Dict containing payment result and transaction ID
           
       Raises:
           ValueError: إذا كان المبلغ غير صحيح
           PaymentError: إذا فشلت عملية الدفع
           
       Example:
           >>> result = process_payment(100.0, 'cash')
           >>> print(result['success'])
           True
       """
   ```

2. **تعليقات الكود**
   ```python
   # تحويل معرف طريقة الدفع إلى الاسم المعروض
   # هذا ضروري للتوافق مع الفواتير القديمة
   if payment_method_id in ['نقدي', 'بنكك', 'شيك']:
       payment_method_id = normalize_payment_method_id(payment_method_id)
   ```

3. **README Updates**
   - حدث README.md عند إضافة ميزات جديدة
   - أضف أمثلة على الاستخدام
   - حدث قائمة المميزات

## عملية المراجعة

### للمراجعين

1. **فحص الكود**
   - هل الكود يتبع معايير المشروع؟
   - هل الاختبارات شاملة؟
   - هل الوثائق محدثة؟

2. **اختبار التغييرات**
   - جرب الميزة الجديدة
   - تأكد من عدم كسر الميزات الموجودة
   - تحقق من الأداء

3. **التعليقات**
   - كن محترفاً ومفيداً
   - اقترح تحسينات محددة
   - امدح الجوانب الجيدة

### للمساهمين

1. **الرد على المراجعات**
   - اقرأ التعليقات بعناية
   - اطرح أسئلة إذا لم تفهم
   - نفذ التغييرات المطلوبة

2. **التواصل**
   - كن محترفاً ومهذباً
   - اشرح قراراتك
   - اطلب المساعدة عند الحاجة

## المساهمة في الوثائق

### أنواع الوثائق

1. **User Documentation**
   - دليل المستخدم
   - أمثلة على الاستخدام
   - أسئلة شائعة

2. **Developer Documentation**
   - API documentation
   - Architecture guide
   - Development setup

3. **Admin Documentation**
   - Installation guide
   - Configuration guide
   - Troubleshooting guide

### إرشادات الكتابة

1. **استخدم لغة واضحة ومفهومة**
2. **أضف أمثلة عملية**
3. **استخدم لقطات الشاشة عند الحاجة**
4. **نظم المحتوى بشكل منطقي**
5. **راجع الأخطاء الإملائية والنحوية**

## المساهمة في التصميم

### UI/UX Guidelines

1. **التصميم المتجاوب**
   - دعم جميع أحجام الشاشات
   - تجربة مستخدم متسقة

2. **إمكانية الوصول**
   - دعم قارئات الشاشة
   - ألوان متباينة
   - تنقل بالكيبورد

3. **الأداء**
   - تحميل سريع
   - استجابة فورية
   - تحسين الصور

### إرشادات CSS

```css
/* استخدم متغيرات CSS */
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;
}

/* استخدم BEM methodology */
.invoice-card {
  /* Block styles */
}

.invoice-card__header {
  /* Element styles */
}

.invoice-card--featured {
  /* Modifier styles */
}
```

## المساهمة في الاختبارات

### أنواع الاختبارات

1. **Unit Tests**
   - اختبار الدوال الفردية
   - اختبار المنطق المعقد
   - اختبار معالجة الأخطاء

2. **Integration Tests**
   - اختبار APIs
   - اختبار قاعدة البيانات
   - اختبار التكامل بين المكونات

3. **End-to-End Tests**
   - اختبار سيناريوهات كاملة
   - اختبار واجهة المستخدم
   - اختبار التدفقات المعقدة

### إرشادات الاختبار

```python
# استخدم أسماء وصفية للاختبارات
def test_calculate_total_with_discount_should_apply_discount_correctly():
    """اختبار حساب الإجمالي مع الخصم"""
    pass

# اختبر الحالات الحدية
def test_calculate_total_with_zero_items_should_return_zero():
    """اختبار حساب الإجمالي مع صفر عناصر"""
    pass

# اختبر معالجة الأخطاء
def test_calculate_total_with_negative_price_should_raise_error():
    """اختبار حساب الإجمالي مع سعر سالب"""
    pass
```

## الاعتراف بالمساهمين

### أنواع المساهمات

1. **Code Contributions**
   - إضافة ميزات جديدة
   - إصلاح الأخطاء
   - تحسين الأداء

2. **Documentation**
   - كتابة الوثائق
   - ترجمة المحتوى
   - تحسين الأمثلة

3. **Testing**
   - كتابة الاختبارات
   - إصلاح الاختبارات المعطلة
   - تحسين تغطية الاختبارات

4. **Community**
   - الإجابة على الأسئلة
   - مساعدة المستخدمين
   - تحسين الوثائق

### الاعتراف

- إضافة أسماء المساهمين إلى README.md
- ذكر المساهمين في release notes
- إرسال شكر خاص للمساهمين المميزين

## الدعم والمساعدة

### الحصول على المساعدة

1. **GitHub Discussions**
   - مناقشة الأفكار
   - طلب المساعدة
   - مشاركة الخبرات

2. **GitHub Issues**
   - الإبلاغ عن الأخطاء
   - اقتراح الميزات
   - طلب المساعدة التقنية

3. **Email**
   - support@example.com
   - للمسائل الحساسة
   - للاستفسارات العامة

### موارد إضافية

- [Python Documentation](https://docs.python.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [Git Documentation](https://git-scm.com/doc)

---

**شكراً لمساهمتكم في تطوير المشروع!** 🎉

**تم إنشاء هذا الدليل بواسطة:** محمد فاروق  
**آخر تحديث:** 2025-01-01
