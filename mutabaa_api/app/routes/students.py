"""
مسارات الطلاب (Students)
"""
from flask import Blueprint, request, jsonify
from config.supabase_config import get_supabase

bp = Blueprint('students', __name__, url_prefix='/api/students')

@bp.route('/', methods=['GET'])
def get_students():
    """الحصول على قائمة الطلاب"""
    try:
        supabase = get_supabase()
        
        # الحصول على معاملات البحث
        class_id = request.args.get('class_id')
        search = request.args.get('search')
        limit = request.args.get('limit', 50)
        
        # بناء الاستعلام
        query = supabase.table('students').select('*, classes(class_name, grade_number)')
        
        if class_id:
            query = query.eq('class_id', class_id)
        
        if search:
            query = query.or_(f'full_name.ilike.%{search}%,student_number.ilike.%{search}%')
        
        query = query.eq('is_active', True).limit(limit)
        
        response = query.execute()
        
        return jsonify({
            'students': response.data,
            'count': len(response.data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """الحصول على معلومات طالب محدد"""
    try:
        supabase = get_supabase()
        response = supabase.table('students').select('*, classes(class_name, grade_number)').eq('id', student_id).execute()
        
        if not response.data:
            return jsonify({'error': 'الطالب غير موجود'}), 404
        
        return jsonify({
            'student': response.data[0]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_student():
    """إضافة طالب جديد"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['student_number', 'first_name', 'last_name', 'full_name', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'الحقل {field} مطلوب'}), 400
        
        supabase = get_supabase()
        response = supabase.table('students').insert(data).execute()
        
        return jsonify({
            'message': 'تم إضافة الطالب بنجاح',
            'student': response.data[0]
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """تحديث معلومات طالب"""
    try:
        data = request.get_json()
        
        supabase = get_supabase()
        response = supabase.table('students').update(data).eq('id', student_id).execute()
        
        if not response.data:
            return jsonify({'error': 'الطالب غير موجود'}), 404
        
        return jsonify({
            'message': 'تم تحديث معلومات الطالب بنجاح',
            'student': response.data[0]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:student_id>/statistics', methods=['GET'])
def get_student_statistics(student_id):
    """الحصول على إحصائيات الطالب"""
    try:
        supabase = get_supabase()
        
        # معلومات الطالب
        student_response = supabase.table('students').select('*').eq('id', student_id).execute()
        
        if not student_response.data:
            return jsonify({'error': 'الطالب غير موجود'}), 404
        
        student = student_response.data[0]
        
        # سجلات السلوك
        behaviors_response = supabase.table('behavior_records').select('*, behavior_types(name_ar, category)').eq('student_id', student_id).execute()
        
        return jsonify({
            'student': {
                'id': student['id'],
                'full_name': student['full_name'],
                'student_number': student['student_number']
            },
            'statistics': {
                'total_points': student['total_points'],
                'positive_behaviors_count': student['positive_behaviors_count'],
                'negative_behaviors_count': student['negative_behaviors_count'],
                'behavior_level': student['behavior_level']
            },
            'recent_behaviors': behaviors_response.data[:10]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

