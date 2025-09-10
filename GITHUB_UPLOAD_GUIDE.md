# دليل رفع المشروع على GitHub

## 📋 نظرة عامة

هذا الدليل يوضح كيفية رفع نظام إدارة المخزون على GitHub بطريقة احترافية.

## 🔗 رابط المستودع

**المستودع الرئيسي**: https://github.com/Mohamed-Faroug/store_management_system.git

## 🚀 الخطوات السريعة

### 1. إعداد Git
```bash
git config --global user.name "Mohamed Faroug"
git config --global user.email "mfh1134@gmail.com"
```

### 2. إنشاء مستودع على GitHub
1. اذهب إلى https://github.com
2. اضغط "New repository"
3. اكتب اسم: `store_management_system`
4. اختر "Public"
5. لا تضع علامة على "Initialize with README"
6. اضغط "Create repository"

### 3. رفع المشروع
```bash
cd store_management_system
git init
git add .
git commit -m "Initial commit - Store Management System v1.0.0"
git remote add origin https://github.com/Mohamed-Faroug/store_management_system.git
git push -u origin main
```

## 📁 الملفات المطلوبة للرفع

### ملفات أساسية
- ✅ `app/` - مجلد التطبيق الرئيسي
- ✅ `run.py` - ملف التشغيل الرئيسي
- ✅ `config.py` - إعدادات التطبيق
- ✅ `requirements.txt` - المكتبات المطلوبة
- ✅ `README.md` - دليل المستخدم
- ✅ `.gitignore` - ملف حماية Git

### ملفات التشغيل
- ✅ `START.bat` - التشغيل السريع
- ✅ `INSTALL_AND_RUN.bat` - التثبيت والتشغيل
- ✅ `AUTO_START.bat` - التشغيل التلقائي
- ✅ `START_HIDDEN.vbs` - التشغيل في الخلفية

### ملفات التوثيق
- ✅ `LICENSE` - رخصة المشروع
- ✅ `CONTRIBUTING.md` - دليل المساهمة
- ✅ `CHANGELOG.md` - سجل التغييرات
- ✅ `SECURITY.md` - سياسة الأمان
- ✅ `API_DOCUMENTATION.md` - وثائق API
- ✅ `DEPLOYMENT_GUIDE.md` - دليل النشر
- ✅ `QUICK_REFERENCE.md` - المرجع السريع
- ✅ `CURSOR_AI_GUIDE.md` - دليل Cursor AI
- ✅ `GITHUB_UPLOAD_GUIDE.md` - دليل رفع GitHub
- ✅ `PROJECT_SUMMARY.md` - ملخص المشروع
- ✅ `AUTO_START_GUIDE.txt` - دليل التشغيل التلقائي

### ملفات محمية (لا تُرفع)
- ❌ `inventory.db` - قاعدة البيانات
- ❌ `*_settings.json` - ملفات الإعدادات
- ❌ `uploads/` - مجلد الملفات المرفوعة
- ❌ `__pycache__/` - ملفات Python المؤقتة
- ❌ `venv/` - البيئة الافتراضية

## 🔧 إعدادات Git

### ملف .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite
*.sqlite3
inventory.db

# Configuration files
config_local.py
.env
.env.local
.env.production

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Uploads
uploads/
temp/

# Backup files
*.bak
*.backup
backup_*

# Settings files
*_settings.json
store_settings.json
payment_methods.json
tax_settings.json
currency_settings.json
pos_settings.json

# Test files
test_*.py
tests/
.pytest_cache/

# Coverage
htmlcov/
.coverage
.coverage.*
coverage.xml

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon
._*
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent

# Linux
*~
.fuse_hidden*
.directory
.Trash-*
.nfs*

# Temporary files
*.tmp
*.temp
*.swp
*.swo
*~

# Cache files
.cache/
*.cache

# Runtime files
*.pid
*.seed
*.pid.lock

# Application specific
*.db-journal
*.db-wal
*.db-shm

# Local development
local_settings.py
dev_settings.py
```

## 📝 رسائل Commit

### تنسيق الرسائل
```
نوع: وصف مختصر

وصف مفصل للتغيير (اختياري)

- نقطة 1
- نقطة 2
- نقطة 3
```

### أنواع التغييرات
- `Add:` - إضافة ميزة جديدة
- `Fix:` - إصلاح خطأ
- `Update:` - تحديث ميزة موجودة
- `Remove:` - حذف ميزة
- `Refactor:` - إعادة هيكلة الكود
- `Docs:` - تحديث الوثائق
- `Style:` - تحسين التنسيق
- `Test:` - إضافة اختبارات

### أمثلة
```
Add: user authentication system

- Added login/logout functionality
- Added password hashing
- Added session management
- Added user roles

Fix: database connection error

- Fixed connection timeout issue
- Added error handling
- Improved connection pooling

Update: invoice generation

- Improved invoice layout
- Added new fields
- Enhanced printing options
```

## 🏷️ إنشاء Tags

### إنشاء tag للإصدار
```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"
git push origin v1.0.0
```

### إنشاء tag للنسخة التجريبية
```bash
git tag -a v1.0.0-beta -m "Version 1.0.0 Beta - Testing Release"
git push origin v1.0.0-beta
```

## 📊 إنشاء Release

### 1. إنشاء Release على GitHub
1. اذهب إلى "Releases"
2. اضغط "Create a new release"
3. اكتب رقم الإصدار: `v1.0.0`
4. اكتب عنوان الإصدار: `Store Management System v1.0.0`
5. اكتب وصف الإصدار:
   ```
   ## 🎉 الإصدار الأول - Store Management System v1.0.0
   
   ### ✨ الميزات الجديدة
   - نظام إدارة المخزون الكامل
   - نقطة بيع متقدمة
   - تقارير شاملة
   - واجهة عربية متطورة
   
   ### 🔧 التحسينات
   - أداء محسن
   - واجهة مستخدم محسنة
   - أمان متقدم
   - توثيق شامل
   
   ### 📱 التوافق
   - Windows 10/11
   - Python 3.7+
   - جميع المتصفحات الحديثة
   
   ### 🚀 التثبيت
   1. حمل الملفات
   2. شغل `INSTALL_AND_RUN.bat`
   3. اذهب إلى http://localhost:5000
   4. سجل دخول كـ admin/admin123
   ```
6. اضغط "Publish release"

### 2. إرفاق ملفات
- **Source code (zip)**: الملفات المضغوطة
- **Source code (tar.gz)**: الملفات المضغوطة
- **Binary files**: ملفات التشغيل

## 🔄 تحديث المشروع

### إضافة التغييرات
```bash
git add .
git commit -m "Update: Added new features and improvements"
git push origin main
```

### إنشاء إصدار جديد
```bash
git tag -a v1.1.0 -m "Version 1.1.0 - New Features"
git push origin v1.1.0
```

### إنشاء Release جديد
1. اذهب إلى "Releases"
2. اضغط "Create a new release"
3. اكتب رقم الإصدار الجديد
4. اكتب وصف التحديثات
5. اضغط "Publish release"

## 🐛 استكشاف الأخطاء

### إذا لم يعمل git push
```bash
git pull origin main
git push -u origin main
```

### إذا لم يعمل git add
```bash
git status
git add -A
```

### إذا لم يعمل git commit
```bash
git config --global user.name "Mohamed Faroug"
git config --global user.email "mfh1134@gmail.com"
```

### إذا لم يعمل git remote
```bash
git remote -v
git remote remove origin
git remote add origin https://github.com/Mohamed-Faroug/store_management_system.git
```

## 📚 إعدادات المستودع

### 1. إعدادات المستودع
- **اسم المستودع**: `store_management_system`
- **الوصف**: `نظام إدارة المخزون المتكامل للمتاجر - Store Management System`
- **الموقع**: `https://github.com/Mohamed-Faroug/store_management_system`
- **الموقع الإلكتروني**: `http://localhost:5000`

### 2. إعدادات الحماية
- **Branch protection**: تفعيل حماية main branch
- **Required status checks**: تفعيل فحص الحالة
- **Restrict pushes**: تقييد الدفع
- **Require pull request reviews**: طلب مراجعة PR

### 3. إعدادات Issues
- **Enable Issues**: تفعيل Issues
- **Enable Projects**: تفعيل Projects
- **Enable Wiki**: تفعيل Wiki
- **Enable Discussions**: تفعيل Discussions

## 🎯 نصائح مهمة

### قبل الرفع
- [ ] تحقق من جميع الملفات
- [ ] تأكد من عمل التطبيق
- [ ] اختبر في بيئة نظيفة
- [ ] راجع الوثائق

### بعد الرفع
- [ ] تحقق من المستودع
- [ ] اختبر التحميل
- [ ] راجع الإعدادات
- [ ] شارك الرابط

### للصيانة
- [ ] حدث الوثائق بانتظام
- [ ] راجع Issues
- [ ] أجب على الأسئلة
- [ ] شارك التحديثات

## 📞 الدعم

### معلومات التواصل
- **البريد الإلكتروني**: [mfh1134@gmail.com](mailto:mfh1134@gmail.com)
- **GitHub**: [@Mohamed-Faroug](https://github.com/Mohamed-Faroug)
- **المستودع**: [store_management_system](https://github.com/Mohamed-Faroug/store_management_system)

### طلب المساعدة
1. تحقق من هذا الدليل
2. راجع README.md
3. ابحث في Issues
4. تواصل مع المطور

## 🎉 النتيجة النهائية

بعد اتباع هذا الدليل، ستحصل على:
- ✅ مستودع GitHub احترافي
- ✅ وثائق شاملة
- ✅ إصدارات منظمة
- ✅ مجتمع نشط
- ✅ دعم مستمر

---

**آخر تحديث**: 10 سبتمبر 2025
**الإصدار**: 1.0.0
**المطور**: محمد فاروق

*هذا الدليل سيساعدك في رفع المشروع على GitHub بطريقة احترافية ومهنية.*