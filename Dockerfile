FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# تعيين مجلد العمل
WORKDIR /app

# تثبيت متطلبات النظام
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# نسخ متطلبات Python
COPY requirements.txt .

# تثبيت متطلبات Python
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء مجلدات مطلوبة
RUN mkdir -p uploads logs backups

# إنشاء مستخدم غير root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# فتح المنفذ
EXPOSE 8000

# تشغيل التطبيق
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "run:app"]
