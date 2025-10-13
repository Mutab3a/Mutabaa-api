"""
تطبيق متابعة - Flask API
نظام إدارة سلوك الطلاب
"""
from flask import Flask
from flask_cors import CORS
from config.supabase_config import init_supabase

def create_app():
    """إنشاء وتهيئة التطبيق"""
    app = Flask(__name__)
    
    # تفعيل CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # تهيئة Supabase
    try:
        init_supabase()
        print("✅ تم الاتصال بـ Supabase بنجاح")
    except Exception as e:
        print(f"❌ خطأ في الاتصال بـ Supabase: {e}")
    
    # تسجيل المسارات (Blueprints)
    from app.routes import auth, students, behaviors, dashboard
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(students.bp)
    app.register_blueprint(behaviors.bp)
    app.register_blueprint(dashboard.bp)
    
    # الصفحة الرئيسية
    @app.route('/')
    def index():
        return {
            'message': 'مرحباً بك في تطبيق متابعة API',
            'version': '1.0.0',
            'status': 'running'
        }
    
    # فحص الصحة
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'التطبيق يعمل بشكل صحيح'}
    
    return app

