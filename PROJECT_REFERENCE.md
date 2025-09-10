# مرجع المشروع النهائي - Project Reference

## 📁 هيكل المشروع النهائي

```
inventory-management-system/
├── 📁 app/                          # التطبيق الرئيسي
│   ├── 📁 models/                   # نماذج قاعدة البيانات
│   │   ├── __init__.py             # ملف التهيئة
│   │   ├── database.py             # إعدادات قاعدة البيانات
│   │   ├── settings_models.py      # نماذج الإعدادات
│   │   └── store_settings.py       # إعدادات المتجر
│   ├── 📁 static/                   # الملفات الثابتة
│   │   ├── 📁 css/                  # ملفات CSS
│   │   │   └── style.css           # التصميم الرئيسي
│   │   ├── 📁 icons/                # الأيقونات
│   │   ├── 📁 js/                   # ملفات JavaScript
│   │   │   └── main.js             # JavaScript الرئيسي
│   │   └── sw.js                   # Service Worker
│   ├── 📁 templates/                # قوالب HTML
│   │   ├── base.html               # القالب الأساسي
│   │   ├── dashboard.html          # لوحة التحكم
│   │   ├── login.html              # صفحة تسجيل الدخول
│   │   ├── 📁 categories/          # قوالب الفئات
│   │   ├── 📁 data_management/     # قوالب إدارة البيانات
│   │   ├── 📁 invoices/            # قوالب الفواتير
│   │   ├── 📁 items/               # قوالب الأصناف
│   │   ├── 📁 mobile/              # قوالب الهواتف
│   │   ├── 📁 purchases/           # قوالب المشتريات
│   │   ├── 📁 reports/             # قوالب التقارير
│   │   ├── 📁 sales/               # قوالب المبيعات
│   │   ├── 📁 settings/            # قوالب الإعدادات
│   │   ├── 📁 stock/               # قوالب المخزون
│   │   ├── 📁 tablet_pwa/          # قوالب الأجهزة اللوحية
│   │   └── 📁 users/               # قوالب المستخدمين
│   ├── 📁 utils/                    # أدوات مساعدة
│   │   ├── __init__.py             # ملف التهيئة
│   │   ├── auth.py                 # نظام المصادقة
│   │   ├── context_processors.py   # معالجات السياق
│   │   └── payment_utils.py        # أدوات طرق الدفع
│   ├── 📁 views/                    # معالجات الطلبات
│   │   ├── __init__.py             # ملف التهيئة
│   │   ├── advanced_settings.py    # الإعدادات المتقدمة
│   │   ├── api.py                  # واجهة برمجية
│   │   ├── auth.py                 # المصادقة
│   │   ├── categories.py           # إدارة الفئات
│   │   ├── data_management.py      # إدارة البيانات
│   │   ├── invoices.py             # إدارة الفواتير
│   │   ├── items.py                # إدارة الأصناف
│   │   ├── main.py                 # الصفحة الرئيسية
│   │   ├── purchases.py            # إدارة المشتريات
│   │   ├── reports.py              # التقارير
│   │   ├── sales.py                # المبيعات
│   │   ├── settings.py             # الإعدادات
│   │   ├── stock.py                # المخزون
│   │   └── users.py                # إدارة المستخدمين
│   └── __init__.py                 # ملف التهيئة الرئيسي
├── 📁 .github/                      # إعدادات GitHub
│   ├── 📁 workflows/               # CI/CD
│   │   ├── ci.yml                  # اختبارات مستمرة
│   │   └── release.yml             # نشر الإصدارات
│   ├── 📁 ISSUE_TEMPLATE/          # قوالب Issues
│   │   ├── bug_report.md           # تقرير الأخطاء
│   │   └── feature_request.md      # اقتراح الميزات
│   ├── CODEOWNERS                  # مالكي الكود
│   ├── CODE_OF_CONDUCT.md          # مدونة السلوك (عربي)
│   ├── CODE_OF_CONDUCT_EN.md       # مدونة السلوك (إنجليزي)
│   ├── dependabot.yml              # تحديث التبعيات
│   ├── FUNDING.yml                 # التمويل
│   ├── PULL_REQUEST_TEMPLATE.md    # قالب Pull Requests
│   └── SUPPORT.md                  # دليل الدعم
├── 📁 tests/                        # الاختبارات
│   ├── __init__.py                 # ملف التهيئة
│   ├── conftest.py                 # إعدادات الاختبار
│   ├── test_basic.py               # اختبارات أساسية
│   └── test_payment_utils.py       # اختبارات طرق الدفع
├── 📁 uploads/                      # الملفات المرفوعة
├── 📁 __pycache__/                  # ملفات Python المؤقتة
├── 📄 .editorconfig                 # إعدادات المحرر
├── 📄 .gitignore                    # ملفات Git المهملة
├── 📄 .pre-commit-config.yaml       # فحص ما قبل الـ commit
├── 📄 CHANGELOG.md                  # سجل التغييرات
├── 📄 CODE_OF_CONDUCT.md            # مدونة السلوك
├── 📄 CONTRIBUTING.md               # دليل المساهمة
├── 📄 DEPLOYMENT_GUIDE.md           # دليل النشر
├── 📄 Dockerfile                    # صورة Docker
├── 📄 LICENSE                       # الترخيص
├── 📄 Makefile                      # أوامر مساعدة
├── 📄 MANIFEST.in                   # ملفات الحزمة
├── 📄 PROJECT_REFERENCE.md          # هذا الملف
├── 📄 README.md                     # دليل المشروع
├── 📄 SECURITY.md                   # سياسة الأمان
├── 📄 api_documentation.md          # وثائق API
├── 📄 config.py                     # إعدادات التطبيق
├── 📄 currency_settings.json        # إعدادات العملات
├── 📄 docker-compose.yml            # إعداد Docker
├── 📄 env.example                   # مثال متغيرات البيئة
├── 📄 inventory.db                  # قاعدة البيانات
├── 📄 nginx.conf                    # إعداد Nginx
├── 📄 payment_methods.json          # طرق الدفع
├── 📄 pos_settings.json             # إعدادات نقطة البيع
├── 📄 pyproject.toml                # إعدادات المشروع
├── 📄 requirements.txt              # متطلبات Python
├── 📄 requirements-dev.txt          # متطلبات التطوير
├── 📄 run.py                        # ملف التشغيل الرئيسي
├── 📄 setup.py                      # إعداد الحزمة
└── 📄 store_settings.json           # إعدادات المتجر
```

## 📋 مرجع الملفات الرئيسية

### 🏗️ ملفات البنية الأساسية

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `run.py` | ملف التشغيل الرئيسي | ⭐⭐⭐⭐⭐ |
| `config.py` | إعدادات التطبيق | ⭐⭐⭐⭐⭐ |
| `app/__init__.py` | تهيئة التطبيق | ⭐⭐⭐⭐⭐ |
| `app/views/main.py` | الصفحة الرئيسية | ⭐⭐⭐⭐⭐ |

### 🗄️ ملفات قاعدة البيانات

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `inventory.db` | قاعدة البيانات SQLite | ⭐⭐⭐⭐⭐ |
| `app/models/database.py` | إعدادات قاعدة البيانات | ⭐⭐⭐⭐⭐ |
| `app/models/settings_models.py` | نماذج الإعدادات | ⭐⭐⭐⭐ |
| `app/models/store_settings.py` | إعدادات المتجر | ⭐⭐⭐⭐ |

### 🎨 ملفات الواجهة

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `app/templates/base.html` | القالب الأساسي | ⭐⭐⭐⭐⭐ |
| `app/templates/dashboard.html` | لوحة التحكم | ⭐⭐⭐⭐⭐ |
| `app/templates/login.html` | صفحة تسجيل الدخول | ⭐⭐⭐⭐⭐ |
| `app/static/css/style.css` | التصميم الرئيسي | ⭐⭐⭐⭐ |
| `app/static/js/main.js` | JavaScript الرئيسي | ⭐⭐⭐⭐ |

### 🔧 ملفات الإعدادات

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `requirements.txt` | متطلبات Python | ⭐⭐⭐⭐⭐ |
| `requirements-dev.txt` | متطلبات التطوير | ⭐⭐⭐⭐ |
| `pyproject.toml` | إعدادات المشروع الحديثة | ⭐⭐⭐⭐ |
| `setup.py` | إعداد الحزمة | ⭐⭐⭐ |
| `env.example` | مثال متغيرات البيئة | ⭐⭐⭐⭐ |

### 🐳 ملفات Docker

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `Dockerfile` | صورة Docker | ⭐⭐⭐⭐ |
| `docker-compose.yml` | إعداد Docker كامل | ⭐⭐⭐⭐ |
| `nginx.conf` | إعداد Nginx | ⭐⭐⭐ |

### 📚 ملفات الوثائق

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `README.md` | دليل المشروع الرئيسي | ⭐⭐⭐⭐⭐ |
| `API_DOCUMENTATION.md` | وثائق API | ⭐⭐⭐⭐⭐ |
| `DEPLOYMENT_GUIDE.md` | دليل النشر | ⭐⭐⭐⭐⭐ |
| `CONTRIBUTING.md` | دليل المساهمة | ⭐⭐⭐⭐ |
| `CHANGELOG.md` | سجل التغييرات | ⭐⭐⭐⭐ |
| `SECURITY.md` | سياسة الأمان | ⭐⭐⭐⭐ |

### 🧪 ملفات الاختبارات

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `tests/conftest.py` | إعدادات الاختبار | ⭐⭐⭐⭐ |
| `tests/test_basic.py` | اختبارات أساسية | ⭐⭐⭐ |
| `tests/test_payment_utils.py` | اختبارات طرق الدفع | ⭐⭐⭐ |

### 🔄 ملفات CI/CD

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `.github/workflows/ci.yml` | اختبارات مستمرة | ⭐⭐⭐⭐ |
| `.github/workflows/release.yml` | نشر الإصدارات | ⭐⭐⭐ |
| `.pre-commit-config.yaml` | فحص ما قبل الـ commit | ⭐⭐⭐ |

### 🛠️ ملفات التطوير

| الملف | الوصف | الأهمية |
|-------|-------|---------|
| `Makefile` | أوامر مساعدة | ⭐⭐⭐⭐ |
| `.editorconfig` | إعدادات المحرر | ⭐⭐⭐ |
| `.gitignore` | ملفات Git المهملة | ⭐⭐⭐⭐ |
| `MANIFEST.in` | ملفات الحزمة | ⭐⭐⭐ |

## 🎯 ملفات حسب الوظيفة

### 📊 إدارة البيانات
- `app/views/invoices.py` - إدارة الفواتير
- `app/views/items.py` - إدارة الأصناف
- `app/views/sales.py` - نقطة البيع
- `app/views/purchases.py` - إدارة المشتريات
- `app/views/stock.py` - إدارة المخزون
- `app/views/reports.py` - التقارير

### ⚙️ الإعدادات
- `app/views/settings.py` - الإعدادات الأساسية
- `app/views/advanced_settings.py` - الإعدادات المتقدمة
- `app/views/users.py` - إدارة المستخدمين
- `app/views/categories.py` - إدارة الفئات

### 🔐 الأمان والمصادقة
- `app/utils/auth.py` - نظام المصادقة
- `app/views/auth.py` - معالجات المصادقة
- `SECURITY.md` - سياسة الأمان

### 🎨 الواجهة
- `app/templates/` - جميع قوالب HTML
- `app/static/` - الملفات الثابتة
- `app/utils/context_processors.py` - معالجات السياق

### 🛠️ الأدوات المساعدة
- `app/utils/payment_utils.py` - أدوات طرق الدفع
- `Makefile` - أوامر مساعدة
- `tests/` - الاختبارات

## 📈 ترتيب الأهمية

### 🔥 حرجة (Critical)
1. `run.py` - ملف التشغيل
2. `app/__init__.py` - تهيئة التطبيق
3. `config.py` - الإعدادات
4. `inventory.db` - قاعدة البيانات
5. `README.md` - دليل المشروع

### ⚡ مهمة جداً (Very Important)
1. `app/views/main.py` - الصفحة الرئيسية
2. `app/models/database.py` - قاعدة البيانات
3. `app/templates/base.html` - القالب الأساسي
4. `requirements.txt` - المتطلبات
5. `API_DOCUMENTATION.md` - وثائق API

### 📋 مهمة (Important)
1. `app/views/invoices.py` - الفواتير
2. `app/views/sales.py` - المبيعات
3. `app/views/items.py` - الأصناف
4. `app/static/css/style.css` - التصميم
5. `DEPLOYMENT_GUIDE.md` - دليل النشر

### 🔧 مفيدة (Useful)
1. `Makefile` - الأوامر المساعدة
2. `tests/` - الاختبارات
3. `Dockerfile` - Docker
4. `.github/workflows/` - CI/CD
5. `CONTRIBUTING.md` - دليل المساهمة

## 🗑️ الملفات المحذوفة

تم حذف الملفات التالية لعدم الحاجة إليها:

- `BAT_FILES_GUIDE_EN.txt` - دليل ملفات BAT (إنجليزي)
- `BAT_FILES_GUIDE.txt` - دليل ملفات BAT (عربي)
- `PROJECT_STRUCTURE_EN.txt` - هيكل المشروع (إنجليزي)
- `PROJECT_STRUCTURE.txt` - هيكل المشروع (عربي)
- `test_english_files.bat` - اختبار الملفات الإنجليزية
- `backup.bat` - نسخ احتياطي
- `check_system.bat` - فحص النظام
- `cleanup.bat` - تنظيف
- `export_data.bat` - تصدير البيانات
- `import_data.bat` - استيراد البيانات
- `install.bat` - التثبيت
- `main_menu.bat` - القائمة الرئيسية
- `quick_start.bat` - البدء السريع
- `restore.bat` - الاستعادة
- `start.bat` - التشغيل
- `start_production.bat` - تشغيل الإنتاج
- `start_production.py` - تشغيل الإنتاج (Python)

## 📊 إحصائيات المشروع النهائية

### 📁 المجلدات
- **المجلدات الرئيسية:** 8
- **المجلدات الفرعية:** 25+
- **إجمالي المجلدات:** 33+

### 📄 الملفات
- **ملفات Python:** 25+
- **ملفات HTML:** 30+
- **ملفات CSS/JS:** 5+
- **ملفات JSON:** 4
- **ملفات Markdown:** 8
- **ملفات YAML:** 6
- **ملفات أخرى:** 10+
- **إجمالي الملفات:** 88+

### 📏 أحجام الملفات
- **أكبر ملف:** `README.md` (~15KB)
- **أصغر ملف:** `__init__.py` (~50B)
- **متوسط الحجم:** ~2KB
- **إجمالي الحجم:** ~200KB

### 🎯 التوزيع
- **الكود:** 60%
- **الوثائق:** 25%
- **الإعدادات:** 10%
- **الاختبارات:** 5%

## 🚀 التوصيات

### للمطورين الجدد
1. ابدأ بـ `README.md`
2. اقرأ `CONTRIBUTING.md`
3. راجع `API_DOCUMENTATION.md`
4. اختبر مع `tests/`

### للمطورين المتقدمين
1. راجع `DEPLOYMENT_GUIDE.md`
2. ادرس `SECURITY.md`
3. استخدم `Makefile` للأوامر
4. راجع `.github/workflows/`

### للمستخدمين
1. اقرأ `README.md`
2. اتبع دليل التثبيت
3. راجع `SUPPORT.md` للدعم
4. استخدم `env.example` للإعداد

---

**تم إنشاء هذا المرجع بواسطة:** محمد فاروق  
**تاريخ الإنشاء:** 2025-01-01  
**الإصدار:** 1.0.0  
**اللغة:** العربية
