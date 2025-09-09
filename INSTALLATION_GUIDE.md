# دليل التثبيت والإعداد

## 🚀 التثبيت السريع

### **1. تثبيت المتطلبات الأساسية:**
```bash
# تثبيت المتطلبات الأساسية فقط
pip install -r requirements.txt
```

### **2. تثبيت جميع المتطلبات (اختياري):**
```bash
# تثبيت جميع المتطلبات بما في ذلك أدوات التحويل
pip install -r requirements_complete.txt
```

## 📋 المتطلبات

### **المتطلبات الأساسية:**
- **Python 3.8+** - متوفر على [python.org](https://python.org)
- **Flask 2.3.3** - إطار عمل الويب
- **Werkzeug 2.3.7** - مكتبة الأمان والمرافق
- **SQLite3** - قاعدة البيانات (مدمجة مع Python)

### **المتطلبات الإضافية:**
- **schedule 1.2.0** - للنسخ الاحتياطي التلقائي
- **pyinstaller 6.3.0** - لتحويل التطبيق إلى EXE
- **cryptography 41.0.7** - للتشفير والأمان
- **python-dateutil 2.8.2** - للتعامل مع التواريخ
- **requests 2.31.0** - للتعامل مع HTTP
- **psutil 5.9.6** - لمراقبة النظام

## 🔧 خطوات التثبيت

### **الخطوة 1: تثبيت Python**
```bash
# تحقق من إصدار Python
python --version

# يجب أن يكون 3.8 أو أحدث
```

### **الخطوة 2: إنشاء بيئة افتراضية (اختياري)**
```bash
# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# على Windows:
venv\Scripts\activate
# على Linux/Mac:
source venv/bin/activate
```

### **الخطوة 3: تثبيت المتطلبات**
```bash
# تثبيت المتطلبات الأساسية
pip install -r requirements.txt

# أو تثبيت جميع المتطلبات
pip install -r requirements_complete.txt
```

### **الخطوة 4: تشغيل التطبيق**
```bash
# تشغيل التطبيق
python main.py

# أو استخدام الملفات الجاهزة
# على Windows:
start_app.bat
# على Linux/Mac:
./start_app.sh
```

## 🐛 حل المشاكل الشائعة

### **مشكلة: "No matching distribution found for sqlite3"**
```bash
# الحل: sqlite3 مدمجة مع Python، لا تحتاج تثبيت
# استخدم requirements.txt بدلاً من requirements_complete.txt
pip install -r requirements.txt
```

### **مشكلة: "Invalid requirement"**
```bash
# الحل: تأكد من أن الملف لا يحتوي على مكتبات مدمجة
# استخدم الملف المحدث requirements.txt
```

### **مشكلة: "ModuleNotFoundError"**
```bash
# الحل: تأكد من تثبيت جميع المتطلبات
pip install --upgrade -r requirements.txt
```

### **مشكلة: "Permission denied"**
```bash
# الحل: استخدم --user
pip install --user -r requirements.txt

# أو استخدم sudo على Linux/Mac
sudo pip install -r requirements.txt
```

## 📦 ملفات المتطلبات

### **1. requirements.txt (الأساسي):**
```
Flask==2.3.3
Werkzeug==2.3.7
schedule==1.2.0
pyinstaller==6.3.0
cryptography==41.0.7
python-dateutil==2.8.2
requests==2.31.0
psutil==5.9.6
```

### **2. requirements_complete.txt (الكامل):**
```
# جميع المتطلبات بما في ذلك أدوات التحويل
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3
schedule==1.2.0
pyinstaller==6.3.0
auto-py-to-exe==2.43.3
buildozer==1.5.0
python-for-android==0.12.0
cryptography==41.0.7
bcrypt==4.1.2
python-dateutil==2.8.2
pathlib2==2.3.7
simplejson==3.19.2
requests==2.31.0
urllib3==2.0.7
psutil==5.9.6
traceback2==1.4.0
```

## 🎯 التحقق من التثبيت

### **1. فحص المكتبات المثبتة:**
```bash
# فحص Flask
python -c "import flask; print(flask.__version__)"

# فحص Werkzeug
python -c "import werkzeug; print(werkzeug.__version__)"

# فحص SQLite3
python -c "import sqlite3; print(sqlite3.version)"
```

### **2. تشغيل التطبيق:**
```bash
# تشغيل التطبيق
python main.py

# يجب أن تظهر رسالة:
# * Running on http://127.0.0.1:8080
```

### **3. فتح المتصفح:**
```
http://127.0.0.1:8080
```

## 🔄 التحديث

### **تحديث المكتبات:**
```bash
# تحديث جميع المكتبات
pip install --upgrade -r requirements.txt

# تحديث مكتبة محددة
pip install --upgrade Flask
```

### **تحديث التطبيق:**
```bash
# سحب التحديثات من Git
git pull origin main

# تثبيت المتطلبات الجديدة
pip install -r requirements.txt
```

## 📱 التثبيت على أنظمة مختلفة

### **Windows:**
```cmd
# تثبيت Python من python.org
# تشغيل Command Prompt كمدير
pip install -r requirements.txt
python main.py
```

### **Linux (Ubuntu/Debian):**
```bash
# تثبيت Python
sudo apt update
sudo apt install python3 python3-pip

# تثبيت المتطلبات
pip3 install -r requirements.txt
python3 main.py
```

### **macOS:**
```bash
# تثبيت Python
brew install python3

# تثبيت المتطلبات
pip3 install -r requirements.txt
python3 main.py
```

## 🛠️ التطوير

### **بيئة التطوير:**
```bash
# تثبيت أدوات التطوير
pip install -r requirements_complete.txt

# تشغيل في وضع التطوير
python main.py
```

### **الاختبار:**
```bash
# تشغيل الاختبارات
python -m pytest

# أو تشغيل التطبيق واختباره يدوياً
python main.py
```

## 📊 استكشاف الأخطاء

### **1. فحص المتطلبات:**
```bash
# فحص المكتبات المثبتة
pip list

# فحص المكتبات المفقودة
pip check
```

### **2. فحص الأخطاء:**
```bash
# تشغيل مع تفاصيل الأخطاء
python -v main.py

# أو تشغيل مع debug
python -c "import sys; print(sys.path)"
```

### **3. إعادة التثبيت:**
```bash
# إعادة تثبيت جميع المكتبات
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

**تم تطوير هذا النظام بواسطة: محمد فاروق**  
**تاريخ آخر تحديث: 9/9/2025**  
**جميع الحقوق محفوظة © 2025**
