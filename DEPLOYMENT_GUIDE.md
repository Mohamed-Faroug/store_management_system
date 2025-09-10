# دليل النشر - Deployment Guide

## نظرة عامة

هذا الدليل يوضح كيفية نشر نظام إدارة المخزون على خوادم الإنتاج المختلفة.

## متطلبات النظام

### الحد الأدنى
- **CPU:** 1 core
- **RAM:** 512 MB
- **Storage:** 1 GB
- **OS:** Linux (Ubuntu 20.04+), Windows Server 2019+, macOS 10.15+

### الموصى به
- **CPU:** 2+ cores
- **RAM:** 2+ GB
- **Storage:** 10+ GB SSD
- **OS:** Ubuntu 22.04 LTS

## طرق النشر

### 1. النشر المحلي (Local Development)

#### التثبيت
```bash
# استنساخ المشروع
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل التطبيق
python run.py
```

#### الوصول
```
http://localhost:5000
```

### 2. النشر على خادم VPS

#### إعداد الخادم (Ubuntu 22.04)

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python و pip
sudo apt install python3 python3-pip python3-venv nginx -y

# تثبيت PostgreSQL (اختياري)
sudo apt install postgresql postgresql-contrib -y

# إنشاء مستخدم للتطبيق
sudo adduser inventory
sudo usermod -aG sudo inventory
```

#### إعداد التطبيق

```bash
# تسجيل الدخول كمستخدم inventory
su - inventory

# استنساخ المشروع
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system

# إنشاء بيئة افتراضية
python3 -m venv venv
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt

# إعداد متغيرات البيئة
cp .env.example .env
nano .env
```

#### ملف .env
```env
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///inventory.db
# أو لـ PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost/inventory_db
```

#### إعداد Gunicorn

```bash
# تثبيت Gunicorn
pip install gunicorn

# إنشاء ملف Gunicorn config
nano gunicorn.conf.py
```

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

#### إنشاء Systemd Service

```bash
sudo nano /etc/systemd/system/inventory.service
```

```ini
[Unit]
Description=Inventory Management System
After=network.target

[Service]
User=inventory
Group=inventory
WorkingDirectory=/home/inventory/inventory-management-system
Environment="PATH=/home/inventory/inventory-management-system/venv/bin"
ExecStart=/home/inventory/inventory-management-system/venv/bin/gunicorn --config gunicorn.conf.py run:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل الخدمة
sudo systemctl daemon-reload
sudo systemctl enable inventory
sudo systemctl start inventory
sudo systemctl status inventory
```

#### إعداد Nginx

```bash
sudo nano /etc/nginx/sites-available/inventory
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/inventory/inventory-management-system/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /home/inventory/inventory-management-system/uploads;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/inventory /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. النشر على Docker

#### إنشاء Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعيين مجلد العمل
WORKDIR /app

# تثبيت متطلبات النظام
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# نسخ متطلبات Python
COPY requirements.txt .

# تثبيت متطلبات Python
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء مستخدم غير root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# فتح المنفذ
EXPOSE 8000

# تشغيل التطبيق
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]
```

#### إنشاء docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://inventory:password@db:5432/inventory_db
    depends_on:
      - db
    volumes:
      - ./uploads:/app/uploads
      - ./inventory.db:/app/inventory.db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=inventory_db
      - POSTGRES_USER=inventory
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
```

#### تشغيل Docker

```bash
# بناء الصور
docker-compose build

# تشغيل الخدمات
docker-compose up -d

# عرض السجلات
docker-compose logs -f

# إيقاف الخدمات
docker-compose down
```

### 4. النشر على Heroku

#### إعداد Heroku

```bash
# تثبيت Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# تسجيل الدخول
heroku login

# إنشاء تطبيق
heroku create inventory-management-system

# إعداد متغيرات البيئة
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# إضافة قاعدة بيانات PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# نشر التطبيق
git push heroku main

# تشغيل migrations
heroku run python manage.py db upgrade
```

#### ملف Procfile

```
web: gunicorn run:app
```

### 5. النشر على AWS

#### إعداد EC2 Instance

```bash
# إنشاء EC2 instance (Ubuntu 22.04)
# Security Group: HTTP (80), HTTPS (443), SSH (22)

# الاتصال بالخادم
ssh -i your-key.pem ubuntu@your-ec2-ip

# تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# استنساخ المشروع
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system

# تشغيل Docker Compose
docker-compose up -d
```

#### إعداد RDS (PostgreSQL)

```bash
# إنشاء RDS instance
# Engine: PostgreSQL
# Instance class: db.t3.micro
# Storage: 20 GB
# Security group: Allow inbound on port 5432

# تحديث DATABASE_URL
export DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/inventory_db
```

### 6. النشر على DigitalOcean

#### إعداد Droplet

```bash
# إنشاء Droplet (Ubuntu 22.04)
# Size: 1GB RAM, 1 CPU
# Region: Choose closest to your users

# الاتصال بالخادم
ssh root@your-droplet-ip

# تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# إعداد التطبيق
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system
docker-compose up -d
```

## إعداد SSL/HTTPS

### باستخدام Let's Encrypt

```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx -y

# الحصول على شهادة SSL
sudo certbot --nginx -d your-domain.com

# تجديد تلقائي
sudo crontab -e
# إضافة: 0 12 * * * /usr/bin/certbot renew --quiet
```

### باستخدام Cloudflare

1. أضف دومينك إلى Cloudflare
2. غيّر nameservers
3. فعّل SSL/TLS
4. فعّل "Always Use HTTPS"

## النسخ الاحتياطي

### نسخ احتياطي لقاعدة البيانات

```bash
# SQLite
cp inventory.db backup/inventory_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL
pg_dump inventory_db > backup/inventory_$(date +%Y%m%d_%H%M%S).sql
```

### نسخ احتياطي للملفات

```bash
# إنشاء نسخة احتياطية
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz \
    inventory.db \
    uploads/ \
    *.json

# رفع إلى S3
aws s3 cp backup_$(date +%Y%m%d_%H%M%S).tar.gz s3://your-backup-bucket/
```

### سكريبت النسخ الاحتياطي التلقائي

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/inventory/backups"
APP_DIR="/home/inventory/inventory-management-system"

# إنشاء مجلد النسخ الاحتياطي
mkdir -p $BACKUP_DIR

# نسخ قاعدة البيانات
cp $APP_DIR/inventory.db $BACKUP_DIR/inventory_$DATE.db

# نسخ الملفات
tar -czf $BACKUP_DIR/files_$DATE.tar.gz -C $APP_DIR uploads/ *.json

# حذف النسخ القديمة (أكثر من 30 يوم)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# إضافة إلى crontab
crontab -e
# إضافة: 0 2 * * * /home/inventory/backup.sh
```

## المراقبة والمراجعة

### مراقبة الأداء

```bash
# مراقبة استخدام الموارد
htop
iostat -x 1
df -h

# مراقبة التطبيق
sudo journalctl -u inventory -f
tail -f /var/log/nginx/access.log
```

### إعدادات المراقبة

```python
# monitoring.py
import psutil
import time
import logging

def monitor_system():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    logging.info(f"CPU: {cpu_percent}%, Memory: {memory.percent}%, Disk: {disk.percent}%")
    
    if cpu_percent > 80:
        logging.warning("High CPU usage detected")
    if memory.percent > 80:
        logging.warning("High memory usage detected")
    if disk.percent > 90:
        logging.critical("Low disk space detected")
```

## استكشاف الأخطاء

### مشاكل شائعة

1. **خطأ في الاتصال بقاعدة البيانات**
   ```bash
   # تحقق من حالة PostgreSQL
   sudo systemctl status postgresql
   
   # تحقق من الاتصال
   psql -h localhost -U inventory -d inventory_db
   ```

2. **خطأ في الصلاحيات**
   ```bash
   # إصلاح صلاحيات الملفات
   sudo chown -R inventory:inventory /home/inventory/inventory-management-system
   sudo chmod -R 755 /home/inventory/inventory-management-system
   ```

3. **خطأ في الذاكرة**
   ```bash
   # زيادة swap
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### سجلات الأخطاء

```bash
# سجلات التطبيق
sudo journalctl -u inventory -n 100

# سجلات Nginx
sudo tail -f /var/log/nginx/error.log

# سجلات النظام
sudo dmesg | tail
```

## التحديثات

### تحديث التطبيق

```bash
# إيقاف الخدمة
sudo systemctl stop inventory

# نسخ احتياطي
./backup.sh

# تحديث الكود
git pull origin main

# تثبيت المتطلبات الجديدة
source venv/bin/activate
pip install -r requirements.txt

# تشغيل migrations (إذا لزم الأمر)
python manage.py db upgrade

# إعادة تشغيل الخدمة
sudo systemctl start inventory
```

### تحديث النظام

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# إعادة تشغيل الخادم
sudo reboot
```

## الأمان

### إعدادات الأمان الأساسية

```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# إعداد firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# تعطيل تسجيل الدخول بـ root
sudo nano /etc/ssh/sshd_config
# PermitRootLogin no
sudo systemctl restart ssh

# إعداد fail2ban
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### إعدادات Flask الأمنية

```python
# config.py
import os

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///inventory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات الأمان
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # إعدادات CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
```

## الدعم

للحصول على الدعم في النشر:
- **GitHub Issues:** [رابط GitHub]
- **Email:** support@example.com
- **Documentation:** [رابط الوثائق]

---

**تم إنشاء هذا الدليل بواسطة:** محمد فاروق  
**آخر تحديث:** 2025-01-01