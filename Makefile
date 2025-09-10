# Makefile for Inventory Management System

.PHONY: help install install-dev test test-cov lint format clean run build deploy

help: ## عرض المساعدة
	@echo "الأوامر المتاحة:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## تثبيت المتطلبات الأساسية
	pip install -r requirements.txt

install-dev: ## تثبيت متطلبات التطوير
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black isort mypy pre-commit
	pre-commit install

test: ## تشغيل الاختبارات
	python -m pytest tests/ -v

test-cov: ## تشغيل الاختبارات مع تغطية الكود
	python -m pytest tests/ --cov=app --cov-report=html --cov-report=term

lint: ## فحص الكود
	flake8 app/ tests/
	black --check app/ tests/
	isort --check-only app/ tests/
	mypy app/

format: ## تنسيق الكود
	black app/ tests/
	isort app/ tests/

clean: ## تنظيف الملفات المؤقتة
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

run: ## تشغيل التطبيق
	python run.py

run-dev: ## تشغيل التطبيق في وضع التطوير
	FLASK_ENV=development python run.py

run-prod: ## تشغيل التطبيق في وضع الإنتاج
	FLASK_ENV=production gunicorn -w 4 -b 0.0.0.0:8000 run:app

build: ## بناء الحزمة
	python -m build

build-docker: ## بناء صورة Docker
	docker build -t inventory-management .

run-docker: ## تشغيل التطبيق في Docker
	docker-compose up -d

stop-docker: ## إيقاف التطبيق في Docker
	docker-compose down

deploy: ## نشر التطبيق
	@echo "نشر التطبيق..."
	# إضافة أوامر النشر هنا

backup: ## إنشاء نسخة احتياطية
	@echo "إنشاء نسخة احتياطية..."
	python -c "from app.models.database import backup_database; backup_database()"

restore: ## استعادة النسخة الاحتياطية
	@echo "استعادة النسخة الاحتياطية..."
	python -c "from app.models.database import restore_database; restore_database()"

init-db: ## تهيئة قاعدة البيانات
	python -c "from app.models.database import init_db; init_db()"

migrate: ## تشغيل migrations
	@echo "تشغيل migrations..."
	# إضافة أوامر migration هنا

security: ## فحص الأمان
	safety check
	bandit -r app/

docs: ## إنشاء الوثائق
	@echo "إنشاء الوثائق..."
	# إضافة أوامر إنشاء الوثائق هنا

setup: install-dev init-db ## إعداد المشروع للمرة الأولى
	@echo "تم إعداد المشروع بنجاح!"

ci: lint test ## تشغيل CI pipeline
	@echo "تم تشغيل CI pipeline بنجاح!"

pre-commit: ## تشغيل pre-commit hooks
	pre-commit run --all-files

update-deps: ## تحديث المتطلبات
	pip-compile requirements.in
	pip-compile requirements-dev.in

check-deps: ## فحص المتطلبات
	pip check
	safety check

# أوامر مساعدة
.PHONY: help-commands
help-commands: ## عرض جميع الأوامر
	@echo "أوامر التطوير:"
	@echo "  make install      - تثبيت المتطلبات"
	@echo "  make install-dev  - تثبيت متطلبات التطوير"
	@echo "  make test         - تشغيل الاختبارات"
	@echo "  make test-cov     - تشغيل الاختبارات مع التغطية"
	@echo "  make lint         - فحص الكود"
	@echo "  make format       - تنسيق الكود"
	@echo "  make clean        - تنظيف الملفات المؤقتة"
	@echo ""
	@echo "أوامر التشغيل:"
	@echo "  make run          - تشغيل التطبيق"
	@echo "  make run-dev      - تشغيل في وضع التطوير"
	@echo "  make run-prod     - تشغيل في وضع الإنتاج"
	@echo "  make run-docker   - تشغيل في Docker"
	@echo ""
	@echo "أوامر البناء والنشر:"
	@echo "  make build        - بناء الحزمة"
	@echo "  make build-docker - بناء صورة Docker"
	@echo "  make deploy       - نشر التطبيق"
	@echo ""
	@echo "أوامر قاعدة البيانات:"
	@echo "  make init-db      - تهيئة قاعدة البيانات"
	@echo "  make backup       - إنشاء نسخة احتياطية"
	@echo "  make restore      - استعادة النسخة الاحتياطية"
	@echo "  make migrate      - تشغيل migrations"
	@echo ""
	@echo "أوامر الأمان:"
	@echo "  make security     - فحص الأمان"
	@echo "  make check-deps   - فحص المتطلبات"
	@echo ""
	@echo "أوامر أخرى:"
	@echo "  make docs         - إنشاء الوثائق"
	@echo "  make setup        - إعداد المشروع للمرة الأولى"
	@echo "  make ci           - تشغيل CI pipeline"
	@echo "  make pre-commit   - تشغيل pre-commit hooks"
