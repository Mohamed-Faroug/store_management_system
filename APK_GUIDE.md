# دليل التحويل إلى ملف APK

## نظام إدارة المخزون - مخزن الزينة

**جميع الحقوق محفوظة © 2025**  
**تم تطوير هذا النظام بواسطة**: محمد فاروق  
**تاريخ آخر تحديث**: 9/9/2025  

---

## 📋 المتطلبات

### 1. تثبيت Python
```bash
# تحميل Python 3.8+ من python.org
# تأكد من إضافة Python إلى PATH
```

### 2. تثبيت Android SDK
```bash
# تحميل Android Studio
# تثبيت Android SDK
# إضافة SDK إلى PATH
```

### 3. تثبيت المكتبات المطلوبة
```bash
pip install -r requirements_complete.txt
pip install buildozer
pip install python-for-android
```

---

## 🚀 خطوات التحويل

### الخطوة 1: تحضير الملفات
تأكد من وجود الملفات التالية:
```
project/
├── main.py
├── app/
├── buildozer.spec
├── requirements_complete.txt
└── README.md
```

### الخطوة 2: تعديل ملف buildozer.spec
افتح ملف `buildozer.spec` وتأكد من الإعدادات:
```ini
[app]
title = نظام إدارة المخزون
package.name = inventory_manager
package.domain = com.mfh.inventory
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.1
requirements = python3,flask,werkzeug,jinja2,markupsafe,itsdangerous,click,blinker,sqlite3,schedule,cryptography,bcrypt,python-dateutil,pathlib2,simplejson,requests,urllib3,psutil,traceback2
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 33
minapi = 21
ndk = 25b
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

### الخطوة 3: بناء ملف APK
```bash
# بناء ملف APK للتطوير
buildozer android debug

# بناء ملف APK للإنتاج
buildozer android release
```

### الخطوة 4: توقيع ملف APK
```bash
# إنشاء مفتاح التوقيع
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000

# توقيع ملف APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore inventory_manager-0.1-release-unsigned.apk alias_name
```

### الخطوة 5: تحسين ملف APK
```bash
# تحسين ملف APK
zipalign -v 4 inventory_manager-0.1-release-unsigned.apk inventory_manager-0.1-release.apk
```

---

## 🔧 تحسينات إضافية

### تحسين الأداء
```ini
# في ملف buildozer.spec
[app]
orientation = portrait
fullscreen = 0
```

### إضافة الصلاحيات
```ini
# في ملف buildozer.spec
[android]
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
```

### تخصيص الأيقونة
```ini
# في ملف buildozer.spec
[app]
icon.filename = icon.png
```

---

## 🐛 حل المشاكل الشائعة

### مشكلة: "SDK not found"
**الحل**: تأكد من تثبيت Android SDK وإضافته إلى PATH

### مشكلة: "NDK not found"
**الحل**: تثبيت Android NDK من Android Studio

### مشكلة: "Permission denied"
**الحل**: تأكد من صلاحيات الكتابة في المجلد

### مشكلة: "Build failed"
**الحل**: راجع ملف buildozer.spec وتأكد من صحة الإعدادات

---

## 📱 تثبيت التطبيق

### على الجهاز
1. **تفعيل المصادر غير المعروفة** في إعدادات Android
2. **نقل ملف APK** إلى الجهاز
3. **فتح ملف APK** وتثبيته

### عبر ADB
```bash
# تثبيت ملف APK
adb install inventory_manager-0.1-release.apk

# إلغاء تثبيت التطبيق
adb uninstall com.mfh.inventory
```

---

## 🎯 نصائح مهمة

1. **اختبر التطبيق على أجهزة مختلفة**
2. **تأكد من صلاحيات التطبيق**
3. **اختبر جميع الوظائف**
4. **احتفظ بنسخة احتياطية من الكود**

---

## 📦 توزيع التطبيق

### Google Play Store
1. **إنشاء حساب مطور**
2. **تحضير ملف APK**
3. **رفع التطبيق**
4. **مراجعة الموافقة**

### توزيع مباشر
1. **رفع ملف APK** إلى موقع ويب
2. **مشاركة الرابط** مع المستخدمين
3. **توفير تعليمات التثبيت**

---

## 📞 الدعم

للمساعدة أو الاستفسارات، يرجى مراجعة الكود المصدري أو التواصل مع المطور.

---

**جميع الحقوق محفوظة © 2025**  
**تم تطوير هذا النظام بواسطة**: محمد فاروق  
**تاريخ آخر تحديث**: 9/9/2025
