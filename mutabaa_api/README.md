# تطبيق متابعة - API

نظام إدارة سلوك الطلاب - الواجهة الخلفية (Backend API)

## المميزات

- ✅ مصادقة JWT
- ✅ إدارة الطلاب
- ✅ تسجيل السلوكيات
- ✅ إحصائيات وتقارير
- ✅ لوحة تحكم شاملة
- ✅ اتصال مباشر بـ Supabase

## المتطلبات

- Python 3.9+
- Supabase Account

## التثبيت المحلي

```bash
# تثبيت المكتبات
pip install -r requirements.txt

# إنشاء ملف .env
cp .env.example .env

# تحديث المتغيرات البيئية في .env
# SUPABASE_URL=...
# SUPABASE_KEY=...

# تشغيل التطبيق
python run.py
```

## النشر على Render

1. ارفع الكود على GitHub
2. أنشئ Web Service جديد في Render
3. اربط GitHub repository
4. أضف المتغيرات البيئية
5. انشر!

## API Endpoints

### المصادقة
- `POST /api/auth/login` - تسجيل الدخول
- `GET /api/auth/profile` - معلومات المستخدم

### الطلاب
- `GET /api/students` - قائمة الطلاب
- `GET /api/students/:id` - معلومات طالب
- `POST /api/students` - إضافة طالب
- `PUT /api/students/:id` - تحديث طالب
- `GET /api/students/:id/statistics` - إحصائيات طالب

### السلوكيات
- `GET /api/behaviors/types` - أنواع السلوكيات
- `GET /api/behaviors/records` - سجلات السلوك
- `POST /api/behaviors/records` - تسجيل سلوك
- `PUT /api/behaviors/records/:id` - تحديث سجل
- `DELETE /api/behaviors/records/:id` - حذف سجل

### لوحة التحكم
- `GET /api/dashboard/overview` - نظرة عامة
- `GET /api/dashboard/statistics` - إحصائيات
- `GET /api/dashboard/classes` - قائمة الصفوف

## تسجيل الدخول الافتراضي

```
Username: admin
Password: admin123
```

⚠️ **مهم:** غيّر كلمة المرور بعد أول تسجيل دخول!

## الترخيص

MIT License

