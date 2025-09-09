# إصلاح مشكلة طباعة الفاتورة - PDF فارغ

## 🔧 المشكلة

عند طباعة الفاتورة يظهر PDF فارغ بدون بيانات الأصناف.

## 🔍 تشخيص المشكلة

### **السبب الرئيسي:**
- البيانات لا تظهر في قالب الفاتورة
- مشكلة في استعلام قاعدة البيانات
- عدم وجود معالجة للأخطاء

### **الأسباب المحتملة:**
1. **مشكلة في استعلام البيانات** - لا يتم جلب أصناف الفاتورة
2. **مشكلة في القالب** - لا يتم عرض البيانات بشكل صحيح
3. **مشكلة في طباعة PDF** - لا يتم تطبيق تنسيقات الطباعة

## 🚀 الحلول المطبقة

### 1. إضافة تصحيح مفصل
```python
# في app/views/invoices.py
print(f"Debug: Invoice ID: {invoice_id}")
print(f"Debug: Invoice data: {dict(invoice) if invoice else 'None'}")
print(f"Debug: Items count: {len(items)}")
for item in items:
    print(f"Debug: Item: {dict(item)}")
```

### 2. تحسين استعلام البيانات
```python
# Get invoice items from sales table
items = db.execute('''
    SELECT s.*, i.name as item_name
    FROM sales s
    JOIN items i ON i.id = s.item_id
    WHERE s.invoice_id = ?
    ORDER BY s.id
''', (invoice_id,)).fetchall()
```

### 3. تحسين قالب الفاتورة
```html
<!-- إضافة معالجة للأخطاء -->
{% if items %}
<table class="table table-sm">
  <!-- جدول الأصناف -->
</table>
{% else %}
<div class="alert alert-warning">
  <i class="bi bi-exclamation-triangle me-2"></i>
  لا توجد أصناف في هذه الفاتورة
</div>
{% endif %}
```

### 4. تحسين طباعة PDF
```javascript
function printInvoice() {
  // Add print-specific styles
  const printStyles = `
    <style>
      @media print {
        body * {
          visibility: hidden;
        }
        .printable, .printable * {
          visibility: visible;
        }
        .printable {
          position: absolute;
          left: 0;
          top: 0;
          width: 100%;
        }
        .no-print {
          display: none !important;
        }
        .card {
          border: 1px solid #000 !important;
          box-shadow: none !important;
        }
        .table {
          border-collapse: collapse !important;
        }
        .table th, .table td {
          border: 1px solid #000 !important;
        }
        .table-primary {
          background-color: #f8f9fa !important;
        }
      }
    </style>
  `;
  
  // Apply styles and print
  const styleElement = document.createElement('div');
  styleElement.innerHTML = printStyles;
  document.head.appendChild(styleElement);
  
  window.print();
  
  // Clean up
  setTimeout(() => {
    document.head.removeChild(styleElement);
  }, 1000);
}
```

## 📱 كيفية الاختبار

### 1. اختبار إنشاء فاتورة
```bash
# شغل التطبيق
python main.py

# افتح المتصفح
http://localhost:5000/sales/new
```

### 2. خطوات الاختبار
1. **أضف أصناف للسلة** من نظام POS
2. **أتم البيع** وانقر "إتمام البيع"
3. **تحقق من الفاتورة** - يجب أن تظهر الأصناف
4. **اطبع الفاتورة** - يجب أن تظهر البيانات في PDF

### 3. فحص سجلات التصحيح
```bash
# راقب سجلات التصحيح في Terminal
Debug: Invoice ID: 123
Debug: Invoice data: {'id': 123, 'invoice_number': 'POS-000123', ...}
Debug: Items count: 3
Debug: Item: {'id': 1, 'item_name': 'إطار ميشلان', 'quantity': 2, ...}
```

## 🔍 تشخيص المشاكل

### **إذا كانت الفاتورة فارغة:**
1. **تحقق من سجلات التصحيح** في Terminal
2. **تحقق من قاعدة البيانات** - هل تم حفظ البيانات؟
3. **تحقق من استعلام البيانات** - هل يتم جلب الأصناف؟

### **إذا كانت البيانات تظهر ولكن PDF فارغ:**
1. **تحقق من تنسيقات الطباعة** في CSS
2. **تحقق من JavaScript** - هل يتم تطبيق التنسيقات؟
3. **جرب طباعة من متصفحات مختلفة**

### **إذا كانت البيانات جزئية:**
1. **تحقق من استعلام JOIN** - هل يتم ربط الجداول بشكل صحيح؟
2. **تحقق من أسماء الأعمدة** - هل تتطابق مع قاعدة البيانات؟
3. **تحقق من معالجة الأخطاء** - هل يتم عرض القيم الافتراضية؟

## 🎯 النتائج المتوقعة

### ✅ يجب أن يعمل الآن:
- عرض بيانات الفاتورة بشكل صحيح
- عرض أصناف الفاتورة في الجدول
- طباعة PDF مع جميع البيانات
- رسائل خطأ واضحة في حالة المشاكل

### 📊 سجلات التصحيح:
```
Debug: Invoice ID: 123
Debug: Invoice data: {'id': 123, 'invoice_number': 'POS-000123', 'total_amount': 150.0, ...}
Debug: Items count: 3
Debug: Item: {'id': 1, 'item_name': 'إطار ميشلان', 'quantity': 2, 'unit_price': 75.0, 'total_price': 150.0}
Debug: Item: {'id': 2, 'item_name': 'مرايا جانبية', 'quantity': 1, 'unit_price': 50.0, 'total_price': 50.0}
Debug: Item: {'id': 3, 'item_name': 'غطاء مقعد', 'quantity': 1, 'unit_price': 100.0, 'total_price': 100.0}
```

## 🛠️ الملفات المحدثة

1. **`app/views/invoices.py`** - إضافة تصحيح وتحسين استعلام البيانات
2. **`app/views/sales.py`** - إضافة تصحيح لحفظ البيانات
3. **`app/templates/invoices/view.html`** - تحسين القالب وإضافة معالجة الأخطاء
4. **`INVOICE_PRINT_FIX.md`** - هذا الملف

---

**تم تطوير هذا النظام بواسطة: محمد فاروق**  
**تاريخ آخر تحديث: 9/9/2025**  
**جميع الحقوق محفوظة © 2025**
