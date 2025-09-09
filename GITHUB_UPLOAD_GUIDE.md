# 🚀 دليل رفع المشروع على GitHub

## 📋 الخطوات المطلوبة

### **الخطوة 1: تهيئة Git في المشروع**

```bash
# 1. تهيئة Git
git init

# 2. إضافة الملفات
git add .

# 3. إنشاء أول commit
git commit -m "Initial commit: نظام إدارة المخزون - مخزن الزينة"
```

### **الخطوة 2: ربط المشروع بـ GitHub**

```bash
# 1. إضافة المستودع البعيد
git remote add origin https://github.com/Mohamed-Faroug/inventory_system.git

# 2. تعيين الفرع الرئيسي
git branch -M main

# 3. رفع المشروع
git push -u origin main
```

### **الخطوة 3: التحقق من الرفع**

```bash
# فحص حالة Git
git status

# فحص المستودعات البعيدة
git remote -v

# فحص الفروع
git branch -a
```

## 📁 الملفات التي سيتم رفعها

### **✅ ملفات مهمة:**
- `app/` - كود التطبيق
- `main.py` - ملف التشغيل الرئيسي
- `config.py` - إعدادات التطبيق
- `requirements.txt` - متطلبات Python
- `README.md` - دليل المشروع
- `install.bat` - ملف التثبيت
- `build_simple.bat` - بناء EXE
- `Dockerfile` - إعدادات Docker
- `docker-compose.yml` - إعدادات Docker Compose
- `.gitignore` - ملفات Git المهملة
- `.github/workflows/ci.yml` - GitHub Actions

### **❌ ملفات لن يتم رفعها (بسبب .gitignore):**
- `dist/` - ملفات EXE
- `build/` - ملفات البناء
- `*.db` - قواعد البيانات
- `__pycache__/` - ملفات Python المؤقتة
- `*.log` - ملفات السجلات

## 🔧 إعدادات إضافية

### **1. إنشاء ملف LICENSE:**
```bash
# إنشاء ملف ترخيص MIT
echo MIT License > LICENSE
```

### **2. إضافة وصف للمستودع:**
- اذهب إلى https://github.com/Mohamed-Faroug/inventory_system
- اضغط على "Settings"
- أضف وصف: "نظام إدارة المخزون - مخزن الزينة"
- أضف موقع: "https://mfarouk.dev"

### **3. إضافة Topics:**
- `inventory-management`
- `pos-system`
- `flask`
- `python`
- `arabic`

## 📝 أوامر Git كاملة

```bash
# تهيئة المشروع
git init
git add .
git commit -m "Initial commit: نظام إدارة المخزون - مخزن الزينة"

# ربط بـ GitHub
git remote add origin https://github.com/Mohamed-Faroug/inventory_system.git
git branch -M main
git push -u origin main
```

## 🔄 التحديثات المستقبلية

### **عند إجراء تغييرات:**
```bash
# إضافة التغييرات
git add .

# إنشاء commit
git commit -m "وصف التغييرات"

# رفع التغييرات
git push origin main
```

### **عند إضافة ملفات جديدة:**
```bash
# إضافة ملفات محددة
git add filename.py

# أو إضافة جميع الملفات
git add .

# commit و push
git commit -m "إضافة ملفات جديدة"
git push origin main
```

## 🎯 نصائح مهمة

### **1. قبل الرفع:**
- تأكد من أن جميع الملفات المهمة موجودة
- تحقق من ملف `.gitignore`
- اختبر التطبيق محلياً

### **2. بعد الرفع:**
- أضف وصف للمستودع
- أضف Topics
- أضف README.md
- فعّل GitHub Pages (اختياري)

### **3. الأمان:**
- لا ترفع ملفات حساسة
- استخدم `.gitignore` بشكل صحيح
- تحقق من الإعدادات الأمنية

## 📱 الوصول للمشروع

بعد الرفع، يمكن الوصول للمشروع من:
- **المستودع:** https://github.com/Mohamed-Faroug/inventory_system
- **التحميل:** يمكن تحميل المشروع كـ ZIP
- **الاستنساخ:** `git clone https://github.com/Mohamed-Faroug/inventory_system.git`

## 🔧 استكشاف الأخطاء

### **مشكلة: Permission denied**
```bash
# حل: إعادة إعداد Git
git config --global user.name "Mohamed-Faroug"
git config --global user.email "your-email@example.com"
```

### **مشكلة: Repository not found**
```bash
# حل: التحقق من الرابط
git remote -v
git remote set-url origin https://github.com/Mohamed-Faroug/inventory_system.git
```

### **مشكلة: Authentication failed**
```bash
# حل: استخدام Personal Access Token
git remote set-url origin https://username:token@github.com/Mohamed-Faroug/inventory_system.git
```

---

**تم تطوير هذا النظام بواسطة: محمد فاروق**  
**تاريخ آخر تحديث: 9/9/2025**  
**جميع الحقوق محفوظة © 2025**
