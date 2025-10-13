"""
مسارات لوحة التحكم (Dashboard)
"""
from flask import Blueprint, request, jsonify
from config.supabase_config import get_supabase

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/overview', methods=['GET'])
def get_overview():
    """الحصول على نظرة عامة"""
    try:
        supabase = get_supabase()
        
        # عدد الطلاب
        students_response = supabase.table('students').select('id', count='exact').eq('is_active', True).execute()
        total_students = students_response.count
        
        # عدد الصفوف
        classes_response = supabase.table('classes').select('id', count='exact').eq('is_active', True).execute()
        total_classes = classes_response.count
        
        # عدد المستخدمين
        users_response = supabase.table('users').select('id', count='exact').eq('is_active', True).execute()
        total_users = users_response.count
        
        # عدد السلوكيات اليوم
        from datetime import date
        today = date.today().isoformat()
        behaviors_today_response = supabase.table('behavior_records').select('id', count='exact').eq('behavior_date', today).execute()
        behaviors_today = behaviors_today_response.count
        
        return jsonify({
            'overview': {
                'total_students': total_students,
                'total_classes': total_classes,
                'total_users': total_users,
                'behaviors_today': behaviors_today
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    """الحصول على إحصائيات مفصلة"""
    try:
        supabase = get_supabase()
        
        # توزيع مستويات السلوك
        levels_response = supabase.table('students').select('behavior_level').eq('is_active', True).execute()
        
        levels_count = {}
        for student in levels_response.data:
            level = student['behavior_level']
            levels_count[level] = levels_count.get(level, 0) + 1
        
        # أفضل 10 طلاب
        top_students_response = supabase.table('students').select('id, full_name, student_number, total_points, behavior_level').eq('is_active', True).order('total_points', desc=True).limit(10).execute()
        
        # آخر السلوكيات
        recent_behaviors_response = supabase.table('behavior_records').select('''
            *,
            students(full_name, student_number),
            behavior_types(name_ar, category)
        ''').order('behavior_date', desc=True).order('behavior_time', desc=True).limit(10).execute()
        
        return jsonify({
            'statistics': {
                'behavior_levels_distribution': levels_count,
                'top_students': top_students_response.data,
                'recent_behaviors': recent_behaviors_response.data
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/classes', methods=['GET'])
def get_classes():
    """الحصول على قائمة الصفوف"""
    try:
        supabase = get_supabase()
        response = supabase.table('classes').select('*').eq('is_active', True).execute()
        
        return jsonify({
            'classes': response.data,
            'count': len(response.data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

