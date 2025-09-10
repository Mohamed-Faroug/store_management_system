# المرجع السريع - Quick Reference

## 🚀 البدء السريع

```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل التطبيق
python run.py

# أو باستخدام Make
make run
```

## 📁 الملفات المهمة

### الأساسيات
- `run.py` - تشغيل التطبيق
- `config.py` - الإعدادات
- `app/__init__.py` - تهيئة التطبيق
- `inventory.db` - قاعدة البيانات

### الواجهة
- `app/templates/base.html` - القالب الأساسي
- `app/templates/dashboard.html` - لوحة التحكم
- `app/static/css/style.css` - التصميم

### البيانات
- `app/views/invoices.py` - الفواتير
- `app/views/sales.py` - المبيعات
- `app/views/items.py` - الأصناف
- `app/models/database.py` - قاعدة البيانات

## 🛠️ الأوامر المفيدة

```bash
# التطوير
make run          # تشغيل التطبيق
make test         # تشغيل الاختبارات
make lint         # فحص الكود
make format       # تنسيق الكود

# النشر
make build        # بناء الحزمة
make run-docker   # تشغيل في Docker
make deploy       # نشر التطبيق

# قاعدة البيانات
make init-db      # تهيئة قاعدة البيانات
make backup       # نسخ احتياطي
make restore      # استعادة
```

## 🔧 الإعدادات

### متغيرات البيئة
```bash
# انسخ ملف المثال
cp env.example .env

# عدّل الإعدادات
nano .env
```

### قاعدة البيانات
```python
# تهيئة قاعدة البيانات
from app.models.database import init_db
init_db()
```

## 📚 الوثائق

- [README.md](README.md) - دليل المشروع
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - وثائق API
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - دليل النشر
- [CONTRIBUTING.md](CONTRIBUTING.md) - دليل المساهمة

## 🐛 استكشاف الأخطاء

### مشاكل شائعة
```bash
# خطأ في التثبيت
pip install --upgrade pip
pip install -r requirements.txt

# خطأ في قاعدة البيانات
make init-db

# خطأ في الصلاحيات
chmod -R 755 app/
```

### السجلات
```bash
# سجلات التطبيق
tail -f logs/app.log

# سجلات النظام
sudo journalctl -u inventory -f
```

## 🧪 الاختبارات

```bash
# تشغيل جميع الاختبارات
make test

# تشغيل اختبارات محددة
pytest tests/test_basic.py

# تشغيل مع التغطية
make test-cov
```

## 🐳 Docker

```bash
# بناء الصورة
make build-docker

# تشغيل في Docker
make run-docker

# إيقاف Docker
make stop-docker
```

## 📊 التقارير

```bash
# تقرير يومي
curl http://localhost:5000/reports/daily

# تقرير شهري
curl http://localhost:5000/reports/monthly
```

## 🔐 الأمان

```bash
# فحص الأمان
make security

# فحص التبعيات
safety check

# فحص الكود
bandit -r app/
```

## 📞 الدعم

- **GitHub Issues:** [رابط GitHub]
- **البريد الإلكتروني:** support@example.com
- **الوثائق:** [SUPPORT.md](.github/SUPPORT.md)

---

**آخر تحديث:** 2025-01-01
