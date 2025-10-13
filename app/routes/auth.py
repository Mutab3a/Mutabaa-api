"""
مسارات المصادقة (Authentication)
"""
from flask import Blueprint, request, jsonify
from config.supabase_config import get_supabase
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

@bp.route('/login', methods=['POST'])
def login():
    """تسجيل الدخول"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبة'}), 400
        
        # البحث عن المستخدم
        supabase = get_supabase()
        response = supabase.table('users').select('*').eq('username', username).execute()
        
        if not response.data:
            return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401
        
        user = response.data[0]
        
        # التحقق من كلمة المرور
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401
        
        # إنشاء توكن JWT
        token = jwt.encode({
            'user_id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(days=7)
        }, SECRET_KEY, algorithm='HS256')
        
        # تحديث آخر تسجيل دخول
        supabase.table('users').update({
            'last_login': datetime.now().isoformat()
        }).eq('id', user['id']).execute()
        
        return jsonify({
            'message': 'تم تسجيل الدخول بنجاح',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'full_name': user['full_name'],
                'role': user['role'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['GET'])
def profile():
    """الحصول على معلومات المستخدم الحالي"""
    try:
        # الحصول على التوكن من الهيدر
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'التوكن مطلوب'}), 401
        
        token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
        
        # فك تشفير التوكن
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'التوكن منتهي الصلاحية'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'التوكن غير صالح'}), 401
        
        # الحصول على معلومات المستخدم
        supabase = get_supabase()
        response = supabase.table('users').select('id, username, email, full_name, role, phone, last_login').eq('id', payload['user_id']).execute()
        
        if not response.data:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        return jsonify({
            'user': response.data[0]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

