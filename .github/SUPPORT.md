# الدعم والمساعدة

نحن هنا لمساعدتك! إذا كنت تواجه مشاكل أو لديك أسئلة حول نظام إدارة المخزون، فإليك الطرق المختلفة للحصول على المساعدة.

## 🆘 طرق الحصول على الدعم

### 1. GitHub Issues
- **للأخطاء:** استخدم [Bug Report](https://github.com/mfarouk/inventory-management-system/issues/new?template=bug_report.md)
- **للميزات:** استخدم [Feature Request](https://github.com/mfarouk/inventory-management-system/issues/new?template=feature_request.md)
- **للأسئلة:** استخدم [GitHub Discussions](https://github.com/mfarouk/inventory-management-system/discussions)

### 2. البريد الإلكتروني
- **الدعم العام:** support@example.com
- **الدعم التقني:** tech@example.com
- **الدعم التجاري:** sales@example.com

### 3. الوثائق
- **دليل المستخدم:** [README.md](README.md)
- **وثائق API:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **دليل النشر:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **دليل المساهمة:** [CONTRIBUTING.md](CONTRIBUTING.md)

## 📋 قبل طلب المساعدة

### 1. تحقق من الوثائق
- اقرأ [README.md](README.md) أولاً
- راجع [FAQ](#faq) أدناه
- ابحث في [Issues](https://github.com/mfarouk/inventory-management-system/issues) المفتوحة

### 2. اجمع المعلومات
- إصدار التطبيق
- نظام التشغيل
- إصدار Python
- رسائل الخطأ
- خطوات إعادة إنتاج المشكلة

### 3. ابحث عن الحلول
- استخدم البحث في GitHub
- راجع [Discussions](https://github.com/mfarouk/inventory-management-system/discussions)
- ابحث في الإنترنت

## 🔍 البحث عن المساعدة

### في GitHub
```
# البحث في Issues
is:issue is:open label:bug
is:issue is:open label:question

# البحث في Discussions
is:discussion category:Q&A
is:discussion category:General
```

### في الوثائق
- استخدم Ctrl+F للبحث في الملفات
- راجع الفهرس في كل ملف
- اتبع الروابط الداخلية

## ❓ الأسئلة الشائعة (FAQ)

### التثبيت والتشغيل

**س: كيف أقوم بتثبيت النظام؟**
ج: اتبع الخطوات في [README.md](README.md#البدء-السريع)

**س: ما هي متطلبات النظام؟**
ج: Python 3.8+, SQLite3, متصفح ويب حديث

**س: كيف أقوم بتشغيل النظام؟**
ج: `python run.py` أو `make run`

### قاعدة البيانات

**س: كيف أقوم بإنشاء نسخة احتياطية؟**
ج: `make backup` أو `python -c "from app.models.database import backup_database; backup_database()"`

**س: كيف أقوم باستعادة النسخة الاحتياطية؟**
ج: `make restore` أو `python -c "from app.models.database import restore_database; restore_database()"`

**س: كيف أقوم بتهيئة قاعدة البيانات؟**
ج: `make init-db` أو `python -c "from app.models.database import init_db; init_db()"`

### الميزات

**س: كيف أقوم بإضافة صنف جديد؟**
ج: انتقل إلى الأصناف > إضافة صنف جديد

**س: كيف أقوم بإنشاء فاتورة؟**
ج: انتقل إلى المبيعات > نقطة البيع

**س: كيف أقوم بطباعة الفاتورة؟**
ج: من قائمة الفواتير، اضغط على عرض > طباعة

### الأخطاء

**س: النظام لا يعمل، ماذا أفعل؟**
ج: تحقق من السجلات، تأكد من تثبيت المتطلبات، راجع [Troubleshooting](#troubleshooting)

**س: رسالة خطأ "Module not found"**
ج: تأكد من تثبيت المتطلبات: `pip install -r requirements.txt`

**س: رسالة خطأ "Database is locked"**
ج: تأكد من عدم تشغيل النظام في مكان آخر، أعد تشغيل النظام

## 🔧 استكشاف الأخطاء

### مشاكل شائعة

#### 1. خطأ في التثبيت
```bash
# تحقق من إصدار Python
python --version

# تأكد من تثبيت pip
pip --version

# حدث pip
pip install --upgrade pip

# تثبيت المتطلبات
pip install -r requirements.txt
```

#### 2. خطأ في قاعدة البيانات
```bash
# تحقق من وجود قاعدة البيانات
ls -la inventory.db

# تحقق من الصلاحيات
chmod 644 inventory.db

# أعد تهيئة قاعدة البيانات
make init-db
```

#### 3. خطأ في الصلاحيات
```bash
# إصلاح صلاحيات الملفات
chmod -R 755 app/
chmod -R 755 uploads/
chmod -R 755 logs/
```

#### 4. خطأ في الذاكرة
```bash
# تحقق من استخدام الذاكرة
free -h

# أعد تشغيل النظام
sudo reboot
```

### سجلات الأخطاء

#### 1. سجلات التطبيق
```bash
# عرض السجلات
tail -f logs/app.log

# عرض السجلات مع الأخطاء فقط
grep -i error logs/app.log
```

#### 2. سجلات النظام
```bash
# عرض سجلات النظام
sudo journalctl -u inventory -f

# عرض سجلات Nginx
sudo tail -f /var/log/nginx/error.log
```

#### 3. سجلات Python
```bash
# تشغيل مع debug
FLASK_DEBUG=1 python run.py

# تشغيل مع verbose
python -v run.py
```

## 📞 التواصل

### للدعم الفوري
- **البريد الإلكتروني:** support@example.com
- **الهاتف:** +1-234-567-8900
- **الرسائل النصية:** +1-234-567-8900

### للدعم التجاري
- **البريد الإلكتروني:** sales@example.com
- **الهاتف:** +1-234-567-8901
- **الموقع:** [www.example.com](https://www.example.com)

### للدعم التقني
- **البريد الإلكتروني:** tech@example.com
- **GitHub:** [@mfarouk](https://github.com/mfarouk)
- **LinkedIn:** [محمد فاروق](https://linkedin.com/in/mfarouk)

## ⏰ أوقات الدعم

### الدعم المجاني
- **الأحد - الخميس:** 9:00 ص - 5:00 م (توقيت الرياض)
- **الجمعة - السبت:** 10:00 ص - 2:00 م (توقيت الرياض)

### الدعم المدفوع
- **24/7** - متاح على مدار الساعة
- **استجابة فورية** - خلال 15 دقيقة
- **دعم متقدم** - فريق متخصص

## 🎯 نصائح للحصول على مساعدة أفضل

### 1. كن محدداً
- اذكر الخطأ بالضبط
- أرفق رسائل الخطأ
- وصف ما كنت تفعله

### 2. قدم السياق
- إصدار النظام
- نظام التشغيل
- المتصفح المستخدم
- الخطوات السابقة

### 3. أرفق الأدلة
- لقطات الشاشة
- ملفات السجلات
- ملفات التكوين
- أمثلة على الكود

### 4. كن صبوراً
- امنحنا وقتاً للرد
- تحقق من الوثائق أولاً
- ابحث عن الحلول

## 📚 موارد إضافية

### الوثائق الرسمية
- [Python Documentation](https://docs.python.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

### المجتمعات
- [Python Community](https://www.python.org/community/)
- [Flask Community](https://flask.palletsprojects.com/community/)
- [Stack Overflow](https://stackoverflow.com/)
- [Reddit Python](https://www.reddit.com/r/Python/)

### الدورات التدريبية
- [Python for Beginners](https://www.python.org/about/gettingstarted/)
- [Flask Tutorial](https://flask.palletsprojects.com/tutorial/)
- [Web Development](https://developer.mozilla.org/en-US/docs/Learn)

---

**شكراً لاستخدام نظام إدارة المخزون!** 🎉

**تم إنشاء هذا الدليل بواسطة:** محمد فاروق  
**آخر تحديث:** 2025-01-01
