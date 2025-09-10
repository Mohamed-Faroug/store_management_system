# دليل النشر - Deployment Guide

## 📋 نظرة عامة

هذا الدليل يوضح كيفية نشر نظام إدارة المخزون في بيئات مختلفة.

## 🖥️ النشر المحلي (Local Deployment)

### المتطلبات
- **Python 3.7+**
- **Windows 10/11** (موصى به)
- **متصفح ويب حديث**

### الخطوات

#### 1. تحميل المشروع
```bash
git clone https://github.com/Mohamed-Faroug/store_management_system.git
cd store_management_system
```

#### 2. إعداد البيئة الافتراضية
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# أو
source venv/bin/activate  # Linux/Mac
```

#### 3. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

#### 4. تشغيل التطبيق
```bash
# الطريقة السهلة
INSTALL_AND_RUN.bat

# أو الطريقة المباشرة
python run.py
```

#### 5. الوصول للتطبيق
- **الرابط**: http://localhost:5000
- **بيانات الدخول**: admin/admin123

## 🌐 النشر على الخادم (Server Deployment)

### المتطلبات
- **خادم Linux/Windows**
- **Python 3.7+**
- **Nginx** (اختياري)
- **Gunicorn** (للإنتاج)

### الخطوات

#### 1. إعداد الخادم
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python
sudo apt install python3 python3-pip python3-venv -y

# تثبيت Git
sudo apt install git -y
```

#### 2. تحميل المشروع
```bash
git clone https://github.com/Mohamed-Faroug/store_management_system.git
cd store_management_system
```

#### 3. إعداد البيئة الافتراضية
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. تثبيت المكتبات
```bash
pip install -r requirements.txt
pip install gunicorn
```

#### 5. إعداد قاعدة البيانات
```bash
python -c "from app.models.database import init_db; init_db()"
```

#### 6. تشغيل التطبيق
```bash
# للتطوير
python run.py

# للإنتاج
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🐳 النشر باستخدام Docker

### إنشاء Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### إنشاء docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./inventory.db:/app/inventory.db
    environment:
      - FLASK_ENV=production
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
    restart: unless-stopped
```

### تشغيل Docker
```bash
# بناء الصورة
docker build -t store-management .

# تشغيل الحاوية
docker run -p 5000:5000 store-management

# أو استخدام docker-compose
docker-compose up -d
```

## ☁️ النشر على السحابة (Cloud Deployment)

### Heroku

#### 1. إعداد Heroku
```bash
# تثبيت Heroku CLI
# تحميل من https://devcenter.heroku.com/articles/heroku-cli

# تسجيل الدخول
heroku login

# إنشاء التطبيق
heroku create store-management-system
```

#### 2. إعداد ملفات Heroku
**Procfile:**
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

**runtime.txt:**
```
python-3.9.7
```

#### 3. نشر التطبيق
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### DigitalOcean

#### 1. إنشاء Droplet
- **نظام التشغيل**: Ubuntu 20.04
- **الحجم**: 1GB RAM, 1 CPU
- **التخزين**: 25GB SSD

#### 2. إعداد الخادم
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python
sudo apt install python3 python3-pip python3-venv -y

# تثبيت Git
sudo apt install git -y

# تثبيت Nginx
sudo apt install nginx -y
```

#### 3. نشر التطبيق
```bash
# تحميل المشروع
git clone https://github.com/Mohamed-Faroug/store_management_system.git
cd store_management_system

# إعداد البيئة
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# تشغيل التطبيق
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### AWS EC2

#### 1. إنشاء Instance
- **نظام التشغيل**: Amazon Linux 2
- **نوع المثيل**: t2.micro
- **مفتاح الأمان**: إنشاء مفتاح جديد

#### 2. إعداد الخادم
```bash
# تحديث النظام
sudo yum update -y

# تثبيت Python
sudo yum install python3 python3-pip -y

# تثبيت Git
sudo yum install git -y
```

#### 3. نشر التطبيق
```bash
# تحميل المشروع
git clone https://github.com/Mohamed-Faroug/store_management_system.git
cd store_management_system

# إعداد البيئة
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# تشغيل التطبيق
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🔧 إعداد Nginx

### ملف nginx.conf
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### تفعيل Nginx
```bash
# نسخ الملف
sudo cp nginx.conf /etc/nginx/sites-available/store-management

# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/store-management /etc/nginx/sites-enabled/

# إعادة تشغيل Nginx
sudo systemctl restart nginx
```

## 🔒 إعداد SSL

### Let's Encrypt
```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx -y

# الحصول على شهادة SSL
sudo certbot --nginx -d your-domain.com

# تجديد تلقائي
sudo crontab -e
# إضافة: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 مراقبة الأداء

### PM2 (Process Manager)
```bash
# تثبيت PM2
npm install -g pm2

# تشغيل التطبيق
pm2 start gunicorn --name "store-management" -- -w 4 -b 0.0.0.0:5000 run:app

# حفظ الإعدادات
pm2 save
pm2 startup
```

### مراقبة النظام
```bash
# مراقبة العمليات
pm2 monit

# مراقبة السجلات
pm2 logs

# إعادة تشغيل التطبيق
pm2 restart store-management
```

## 🔄 النسخ الاحتياطية

### نسخ احتياطية تلقائية
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
APP_DIR="/path/to/your/app"

# إنشاء مجلد النسخ الاحتياطية
mkdir -p $BACKUP_DIR

# نسخ قاعدة البيانات
cp $APP_DIR/inventory.db $BACKUP_DIR/inventory_$DATE.db

# نسخ الملفات المرفوعة
cp -r $APP_DIR/uploads $BACKUP_DIR/uploads_$DATE

# ضغط النسخة الاحتياطية
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz $BACKUP_DIR/inventory_$DATE.db $BACKUP_DIR/uploads_$DATE

# حذف الملفات المؤقتة
rm $BACKUP_DIR/inventory_$DATE.db
rm -rf $BACKUP_DIR/uploads_$DATE

# حذف النسخ القديمة (أكثر من 7 أيام)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: backup_$DATE.tar.gz"
```

### جدولة النسخ الاحتياطية
```bash
# إضافة إلى crontab
crontab -e

# نسخ احتياطية يومية في الساعة 2 صباحاً
0 2 * * * /path/to/backup.sh
```

## 🚨 استكشاف الأخطاء

### مشاكل شائعة

#### خطأ في المنفذ
```
Address already in use
```
**الحل:**
```bash
# البحث عن العملية
lsof -i :5000

# إنهاء العملية
kill -9 <PID>
```

#### خطأ في الصلاحيات
```
Permission denied
```
**الحل:**
```bash
# تغيير صلاحيات الملفات
chmod +x run.py
chmod 755 app/
```

#### خطأ في قاعدة البيانات
```
Database is locked
```
**الحل:**
```bash
# إعادة تشغيل التطبيق
pm2 restart store-management
```

### سجلات الأخطاء
```bash
# سجلات التطبيق
tail -f /var/log/store-management.log

# سجلات Nginx
tail -f /var/log/nginx/error.log

# سجلات النظام
journalctl -u store-management
```

## 📈 تحسين الأداء

### تحسين قاعدة البيانات
```python
# إضافة فهارس
CREATE INDEX idx_items_name ON items(name);
CREATE INDEX idx_sales_date ON sales(created_at);
CREATE INDEX idx_purchases_date ON purchases(created_at);
```

### تحسين التطبيق
```python
# إعدادات Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --worker-class gevent --worker-connections 1000 run:app
```

### تحسين Nginx
```nginx
# ضغط الملفات
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# ذاكرة التخزين المؤقت
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 🔐 الأمان

### إعدادات الأمان
```python
# في config.py
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
DEBUG = False
```

### حماية الخادم
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت UFW
sudo apt install ufw -y

# إعداد الجدار الناري
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 📞 الدعم

### معلومات التواصل
- **البريد الإلكتروني**: [mfh1134@gmail.com](mailto:mfh1134@gmail.com)
- **GitHub**: [@Mohamed-Faroug](https://github.com/Mohamed-Faroug)
- **المستودع**: [store_management_system](https://github.com/Mohamed-Faroug/store_management_system)

### طلب المساعدة
1. تحقق من سجلات الأخطاء
2. راجع هذا الدليل
3. ابحث في Issues على GitHub
4. تواصل مع المطور

---

**آخر تحديث**: 10 سبتمبر 2025
**الإصدار**: 1.0.0
**المطور**: محمد فاروق

*هذا الدليل يغطي جميع طرق النشر الشائعة. للمزيد من المعلومات، يرجى التواصل معنا.*
