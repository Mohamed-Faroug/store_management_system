# استخدام Python 3.12 كصورة أساسية
FROM python:3.12-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# تعيين مجلد العمل
WORKDIR /app

# تثبيت المتطلبات النظام
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات التطبيق
COPY . .

# إنشاء المجلدات المطلوبة
RUN mkdir -p logs backups temp uploads data

# تعيين الصلاحيات
RUN chmod +x main.py

# فتح المنفذ
EXPOSE 8080

# تشغيل التطبيق
CMD ["python", "main.py"]
