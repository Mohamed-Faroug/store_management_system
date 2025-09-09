# 📁 هيكل المشروع المنظم

## 🎯 نظرة عامة

تم تنظيم المشروع بالكامل ليكون جاهزاً للإنتاج ورفعه على GitHub مع ملف EXE واحد نظيف ومكتمل.

## 📂 هيكل الملفات

```
inventory-management/
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 ci.yml                    # GitHub Actions
├── 📁 app/                              # كود التطبيق
│   ├── 📁 static/                       # ملفات CSS و JS
│   ├── 📁 templates/                    # قوالب HTML
│   ├── 📁 views/                        # صفحات التطبيق
│   ├── 📁 models/                       # نماذج قاعدة البيانات
│   └── 📄 __init__.py                   # إعدادات Flask
├── 📁 dist/                             # ملفات EXE
│   └── 📄 inventory_system.exe          # التطبيق الرئيسي
├── 📁 inventory_system_release/         # حزمة التوزيع
│   ├── 📄 inventory_system.exe          # التطبيق الرئيسي
│   ├── 📄 start.bat                     # تشغيل سريع
│   ├── 📄 install.bat                   # ملف التثبيت
│   ├── 📄 README.txt                    # دليل الاستخدام
│   ├── 📁 app/                          # ملفات التطبيق
│   └── 📄 inventory.db                  # قاعدة البيانات
├── 📄 .gitignore                        # ملفات Git المهملة
├── 📄 README.md                         # دليل المشروع
├── 📄 main.py                           # ملف التشغيل الرئيسي
├── 📄 config.py                         # إعدادات التطبيق
├── 📄 requirements.txt                  # متطلبات Python
├── 📄 install.bat                       # ملف التثبيت
├── 📄 build_simple.bat                  # بناء EXE بسيط
├── 📄 build_production.bat              # بناء EXE للإنتاج
├── 📄 Dockerfile                        # إعدادات Docker
├── 📄 docker-compose.yml                # إعدادات Docker Compose
└── 📄 inventory.db                      # قاعدة البيانات
```

## 🚀 طرق التشغيل

### **1. التشغيل المباشر (Python):**
```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل التطبيق
python main.py
```

### **2. التشغيل من EXE:**
```bash
# تشغيل مباشر
dist\inventory_system.exe

# أو من حزمة التوزيع
inventory_system_release\inventory_system.exe
```

### **3. التثبيت الشامل:**
```bash
# تشغيل ملف التثبيت
install.bat
```

## 🏗️ طرق البناء

### **1. بناء بسيط:**
```bash
build_simple.bat
```

### **2. بناء للإنتاج:**
```bash
build_production.bat
```

### **3. بناء مع Docker:**
```bash
docker build -t inventory-system .
docker run -p 8080:8080 inventory-system
```

## 📦 حزمة التوزيع

### **المحتويات:**
- `inventory_system.exe` - التطبيق الرئيسي
- `start.bat` - تشغيل سريع
- `install.bat` - ملف التثبيت
- `README.txt` - دليل الاستخدام
- `app/` - ملفات التطبيق
- `inventory.db` - قاعدة البيانات

### **الاستخدام:**
1. نسخ مجلد `inventory_system_release/` إلى أي جهاز
2. تشغيل `install.bat` للتثبيت
3. أو تشغيل `start.bat` مباشرة

## 🔧 المميزات الجديدة

### **1. إعدادات الإنتاج:**
- ملف `config.py` للإعدادات
- دعم بيئات متعددة (تطوير، إنتاج، اختبار)
- إعدادات أمان محسنة

### **2. Docker Support:**
- `Dockerfile` للتشغيل في الحاويات
- `docker-compose.yml` للتشغيل المحلي
- دعم البيئات السحابية

### **3. CI/CD:**
- GitHub Actions للبناء التلقائي
- اختبارات تلقائية
- نشر تلقائي للإصدارات

### **4. التنظيم:**
- حذف الملفات غير الضرورية
- تنظيم الملفات بشكل منطقي
- ملفات README شاملة

## 🛠️ التطوير

### **إعداد بيئة التطوير:**
```bash
# 1. استنساخ المشروع
git clone https://github.com/username/inventory-management.git

# 2. الانتقال للمجلد
cd inventory-management

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. تشغيل التطبيق
python main.py
```

### **اختبار التطبيق:**
```bash
# تشغيل الاختبارات
python -m pytest tests/ -v

# بناء EXE
build_simple.bat
```

## 📋 المتطلبات

### **للتشغيل:**
- Python 3.8+ (للتشغيل من الكود)
- Windows 10/11 (للـ EXE)

### **للتطوير:**
- Python 3.8+
- Git
- Docker (اختياري)

## 🔒 الأمان

### **إعدادات الأمان:**
- كلمات مرور قوية
- تشفير البيانات
- حماية من SQL Injection
- CSRF Protection

### **توصيات:**
- غيّر كلمات المرور الافتراضية
- احتفظ بنسخ احتياطية
- راقب السجلات

## 📞 الدعم

### **للحصول على المساعدة:**
- 📧 البريد الإلكتروني: support@example.com
- 📱 الهاتف: +1234567890
- 🌐 الموقع: https://mfarouk.dev

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT. راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

**تم تطوير هذا النظام بواسطة: محمد فاروق**  
**تاريخ آخر تحديث: 9/9/2025**  
**جميع الحقوق محفوظة © 2025**
