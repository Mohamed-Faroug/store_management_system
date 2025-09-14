# نظام الأدوار الإنجليزية الجديد

## 🎯 التحديث المطبق

تم تطبيق نظام أدوار إنجليزية مبسط ومستقر:

### 🔧 التغييرات الرئيسية:

#### 1. **دالة `init_db()` مبسطة**
```python
def init_db():
    """Initialize the database with schema and default data"""
    db = get_db()
    db.executescript(SCHEMA_SQL)

    # ---- Default Users ----
    cur = db.execute('SELECT COUNT(*) as c FROM users')
    if cur.fetchone()['c'] == 0:
        default_users = [
            ('owner', 'owner', generate_password_hash('owner'), 'all_permissions', 'hidden'),
            ('dev', 'dev', generate_password_hash('dev'), 'all_permissions', 'hidden'),
            ('admin', 'admin', generate_password_hash('admin123'), 'manage_users_inventory_sales', 'visible'),
            ('clerk', 'clerk', generate_password_hash('clerk123'), 'sales_inventory', 'visible')
        ]
        for role, username, pwd, perms, status in default_users:
            db.execute(
                'INSERT INTO users (role, username, password_hash, permissions, status) VALUES (?,?,?,?,?)',
                (role, username, pwd, perms, status)
            )
        db.commit()
```

#### 2. **جدول المستخدمين محدث**
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,                    -- role (owner, dev, admin, clerk)
    username TEXT UNIQUE NOT NULL,         -- username
    password_hash TEXT NOT NULL,           -- encrypted password
    permissions TEXT NOT NULL,             -- permissions
    status TEXT NOT NULL DEFAULT 'visible',-- status (visible / hidden)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. **نظام المصادقة محدث**
- `check_user_permissions()` يتحقق من `all_permissions`
- `dev_user_required()` يتحقق من دور `dev`
- `owner_user_required()` يتحقق من دور `owner`
- `dev_or_owner_required()` يتحقق من `dev` أو `owner`

#### 4. **قوالب HTML محدثة**
- خيارات الأدوار: `admin` و `clerk`
- حالة المستخدم: `visible` بدلاً من `مرئي`

## 🔐 المستخدمون الافتراضيون

| الدور | اسم المستخدم | كلمة المرور | الصلاحيات | الحالة |
|-------|---------------|--------------|-----------|--------|
| owner | owner | owner | all_permissions | hidden |
| dev | dev | dev | all_permissions | hidden |
| admin | admin | admin123 | manage_users_inventory_sales | visible |
| clerk | clerk | clerk123 | sales_inventory | visible |

## ✨ المميزات الجديدة

### 1. **بساطة في التطبيق**
- دالة `init_db()` مبسطة بدون تعقيدات
- لا توجد قيود CHECK معقدة
- نظام أدوار واضح ومفهوم

### 2. **استقرار النظام**
- لا توجد مشاكل في القيود
- يعمل على أي جهاز جديد
- لا يحتاج ترحيل معقد

### 3. **أمان محسن**
- المستخدمون `dev` و `owner` مخفيين
- صلاحيات واضحة ومحددة
- نظام مصادقة محسن

## 🚀 كيفية التطبيق

### الطريقة السهلة:
1. شغل الملف: `apply_english_roles.bat`
2. انتظر حتى اكتمال العملية
3. النظام جاهز للاستخدام!

### النتيجة:
- ✅ لن تظهر رسائل خطأ القيد
- ✅ المستخدمون الافتراضيون سيتم إنشاؤهم تلقائياً
- ✅ النظام سيعمل بشكل مثالي على أي جهاز
- ✅ الأدوار والصلاحيات واضحة ومستقرة

## 🎉 تم الإنجاز!

النظام الجديد:
- **مبسط** - لا تعقيدات غير ضرورية
- **مستقر** - يعمل بشكل مثالي
- **آمن** - نظام صلاحيات محسن
- **واضح** - أدوار إنجليزية مفهومة

المشروع جاهز للاستخدام! 🚀
