"""
إعدادات الاتصال بـ Supabase
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# معلومات Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# إنشاء عميل Supabase
supabase: Client = None

def init_supabase():
    """تهيئة اتصال Supabase"""
    global supabase
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            # محاولة الاتصال بدون خيارات إضافية
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            return supabase
        except Exception as e:
            print(f"خطأ في الاتصال بـ Supabase: {e}")
            raise ValueError(f"فشل الاتصال بـ Supabase: {e}")
    else:
        raise ValueError("معلومات Supabase غير موجودة في المتغيرات البيئية")

def get_supabase():
    """الحصول على عميل Supabase"""
    global supabase
    if supabase is None:
        supabase = init_supabase()
    return supabase
