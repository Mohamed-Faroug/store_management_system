# المرجع السريع - Quick Reference

## 🚀 التشغيل السريع

### الطريقة الأسهل
```bash
# 1. تحميل المشروع
git clone https://github.com/Mohamed-Faroug/store_management_system.git
cd store_management_system

# 2. تشغيل ملف التثبيت
INSTALL_AND_RUN.bat

# 3. الوصول للتطبيق
# http://localhost:5000
# admin/admin123
```

### الطريقة المباشرة
```bash
# 1. تثبيت المكتبات
pip install -r requirements.txt

# 2. تشغيل التطبيق
python run.py

# 3. الوصول للتطبيق
# http://localhost:5000
```

## 🔐 بيانات الدخول

| المستخدم | كلمة المرور | الصلاحيات |
|----------|-------------|-----------|
| admin | admin123 | جميع الصلاحيات |
| clerk | clerk123 | مبيعات ومخزون |

## 📱 الروابط المهمة

| الوظيفة | الرابط |
|---------|--------|
| الصفحة الرئيسية | http://localhost:5000 |
| تسجيل الدخول | http://localhost:5000/login |
| لوحة التحكم | http://localhost:5000/dashboard |
| نقطة البيع | http://localhost:5000/sales/new |
| إدارة الأصناف | http://localhost:5000/items |
| إدارة المبيعات | http://localhost:5000/sales |
| إدارة المشتريات | http://localhost:5000/purchases |
| التقارير | http://localhost:5000/reports |
| الإعدادات | http://localhost:5000/settings |

## 🛠️ الأوامر المفيدة

### Python
```bash
# تشغيل التطبيق
python run.py

# تثبيت المكتبات
pip install -r requirements.txt

# إنشاء قاعدة البيانات
python -c "from app.models.database import init_db; init_db()"
```

### Git
```bash
# تحميل المشروع
git clone https://github.com/Mohamed-Faroug/store_management_system.git

# تحديث المشروع
git pull origin main

# إرسال التغييرات
git add .
git commit -m "Update"
git push origin main
```

### Windows
```bash
# تشغيل سريع
START.bat

# تثبيت وتشغيل
INSTALL_AND_RUN.bat

# تشغيل تلقائي
AUTO_START.bat
```

## 📊 الوظائف الرئيسية

### 🏪 إدارة المخزون
- **إضافة صنف**: `/items/new`
- **تعديل صنف**: `/items/edit/{id}`
- **حذف صنف**: `/items/delete/{id}`
- **عرض الأصناف**: `/items`

### 💰 إدارة المبيعات
- **بيع سريع**: `/sales/new`
- **عرض المبيعات**: `/sales`
- **طباعة فاتورة**: `/invoices/print/{id}`

### 📦 إدارة المشتريات
- **شراء جديد**: `/purchases/new`
- **عرض المشتريات**: `/purchases`
- **عرض فاتورة**: `/purchases/view/{id}`

### 📊 التقارير
- **تقرير يومي**: `/reports/daily`
- **تقرير شهري**: `/reports/monthly`
- **تقرير سنوي**: `/reports/yearly`

### ⚙️ الإعدادات
- **إعدادات المتجر**: `/settings/store`
- **طرق الدفع**: `/settings/payment-methods`
- **الضرائب**: `/settings/tax`
- **العملات**: `/settings/currency`

## 🎯 اختصارات لوحة المفاتيح

| الاختصار | الوظيفة |
|----------|---------|
| Ctrl + S | حفظ |
| Ctrl + N | جديد |
| Ctrl + E | تعديل |
| Ctrl + D | حذف |
| Ctrl + P | طباعة |
| F5 | تحديث |
| Esc | إلغاء |

## 🔍 البحث السريع

### في الأصناف
- **البحث بالاسم**: اكتب اسم الصنف
- **البحث بالباركود**: اكتب الباركود
- **البحث بالفئة**: اختر الفئة

### في المبيعات
- **البحث بالعميل**: اكتب اسم العميل
- **البحث بالتاريخ**: اختر التاريخ
- **البحث بالمبلغ**: اكتب المبلغ

### في المشتريات
- **البحث بالمورد**: اكتب اسم المورد
- **البحث بالتاريخ**: اختر التاريخ
- **البحث بالمبلغ**: اكتب المبلغ

## 📱 الواجهات المدعومة

### 🖥️ سطح المكتب
- **المتصفحات**: Chrome, Firefox, Edge, Safari
- **الدقة**: 1024x768 أو أعلى
- **الوظائف**: جميع الوظائف متاحة

### 📱 الهاتف المحمول
- **المتصفحات**: Chrome Mobile, Safari Mobile
- **الدقة**: 320x568 أو أعلى
- **الوظائف**: مبيعات، مخزون، تقارير

### 📟 التابلت
- **المتصفحات**: Chrome, Safari
- **الدقة**: 768x1024 أو أعلى
- **الوظائف**: نقطة بيع، مبيعات، مخزون

## 🚨 استكشاف الأخطاء السريع

### مشاكل شائعة

#### التطبيق لا يعمل
```bash
# تحقق من Python
python --version

# تحقق من المكتبات
pip list

# تحقق من المنفذ
netstat -an | findstr :5000
```

#### خطأ في قاعدة البيانات
```bash
# إعادة إنشاء قاعدة البيانات
python -c "from app.models.database import init_db; init_db()"

# تحقق من الملف
dir inventory.db
```

#### خطأ في المكتبات
```bash
# إعادة تثبيت المكتبات
pip install -r requirements.txt --force-reinstall

# تحديث pip
python -m pip install --upgrade pip
```

### رسائل الخطأ الشائعة

| الخطأ | الحل |
|-------|------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `Address already in use` | `taskkill /f /im python.exe` |
| `Database is locked` | إعادة تشغيل التطبيق |
| `Permission denied` | تشغيل كمدير |

## 📞 الدعم السريع

### معلومات التواصل
- **البريد الإلكتروني**: mfh1134@gmail.com
- **GitHub**: @Mohamed-Faroug
- **المستودع**: store_management_system

### طلب المساعدة
1. **تحقق من هذا المرجع**
2. **راجع README.md**
3. **ابحث في Issues**
4. **تواصل مع المطور**

## 🎯 نصائح مفيدة

### للأداء الأمثل
- **استخدم Chrome** للحصول على أفضل أداء
- **أغلق التطبيقات الأخرى** لتوفير الذاكرة
- **حدث المتصفح** بانتظام
- **احذف ملفات التخزين المؤقت**

### للأمان
- **غيّر كلمات المرور الافتراضية**
- **استخدم كلمات مرور قوية**
- **سجل الخروج عند الانتهاء**
- **احتفظ بنسخ احتياطية**

### للاستخدام
- **احفظ عملك بانتظام**
- **استخدم الاختصارات**
- **تعلم الوظائف الأساسية**
- **اقرأ الوثائق**

## 📚 الملفات المهمة

| الملف | الوصف |
|-------|--------|
| `run.py` | ملف التشغيل الرئيسي |
| `config.py` | إعدادات التطبيق |
| `requirements.txt` | المكتبات المطلوبة |
| `README.md` | دليل المستخدم |
| `START.bat` | التشغيل السريع |
| `INSTALL_AND_RUN.bat` | التثبيت والتشغيل |

## 🔄 التحديثات

### تحديث المشروع
```bash
git pull origin main
pip install -r requirements.txt
```

### تحديث المكتبات
```bash
pip install --upgrade -r requirements.txt
```

### تحديث Python
```bash
# تحميل من python.org
# تثبيت الإصدار الجديد
# تحديث PATH
```

## 🎉 نصائح للمبتدئين

### البداية
1. **اقرأ README.md** أولاً
2. **شغل INSTALL_AND_RUN.bat**
3. **سجل دخول كـ admin**
4. **استكشف الواجهة**

### التعلم
1. **ابدأ بالأصناف**
2. **جرب المبيعات**
3. **استكشف التقارير**
4. **عدّل الإعدادات**

### التطوير
1. **اقرأ الكود**
2. **جرب التعديلات**
3. **اختبر التغييرات**
4. **شارك التحسينات**

---

**آخر تحديث**: 10 سبتمبر 2025
**الإصدار**: 1.0.0
**المطور**: محمد فاروق

*هذا المرجع السريع يغطي أهم المعلومات التي تحتاجها لاستخدام النظام بفعالية.*
