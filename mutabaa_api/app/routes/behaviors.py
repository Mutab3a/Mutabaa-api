"""
مسارات السلوكيات (Behaviors)
"""
from flask import Blueprint, request, jsonify
from config.supabase_config import get_supabase
from datetime import datetime

bp = Blueprint('behaviors', __name__, url_prefix='/api/behaviors')

@bp.route('/types', methods=['GET'])
def get_behavior_types():
    """الحصول على أنواع السلوكيات"""
    try:
        supabase = get_supabase()
        category = request.args.get('category')  # positive أو negative
        
        query = supabase.table('behavior_types').select('*').eq('is_active', True)
        
        if category:
            query = query.eq('category', category)
        
        response = query.execute()
        
        return jsonify({
            'behavior_types': response.data,
            'count': len(response.data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/records', methods=['GET'])
def get_behavior_records():
    """الحصول على سجلات السلوك"""
    try:
        supabase = get_supabase()
        
        # معاملات البحث
        student_id = request.args.get('student_id')
        class_id = request.args.get('class_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 100)
        
        # بناء الاستعلام
        query = supabase.table('behavior_records').select('''
            *,
            students(id, full_name, student_number, classes(class_name)),
            behavior_types(name_ar, category, points),
            users(full_name)
        ''')
        
        if student_id:
            query = query.eq('student_id', student_id)
        
        if start_date:
            query = query.gte('behavior_date', start_date)
        
        if end_date:
            query = query.lte('behavior_date', end_date)
        
        query = query.order('behavior_date', desc=True).order('behavior_time', desc=True).limit(limit)
        
        response = query.execute()
        
        return jsonify({
            'records': response.data,
            'count': len(response.data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/records', methods=['POST'])
def create_behavior_record():
    """تسجيل سلوك جديد"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['student_id', 'behavior_type_id', 'points_awarded']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'الحقل {field} مطلوب'}), 400
        
        # إضافة التاريخ والوقت إذا لم يكن موجوداً
        if 'behavior_date' not in data:
            data['behavior_date'] = datetime.now().date().isoformat()
        
        if 'behavior_time' not in data:
            data['behavior_time'] = datetime.now().time().isoformat()
        
        supabase = get_supabase()
        response = supabase.table('behavior_records').insert(data).execute()
        
        return jsonify({
            'message': 'تم تسجيل السلوك بنجاح',
            'record': response.data[0]
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/records/<int:record_id>', methods=['PUT'])
def update_behavior_record(record_id):
    """تحديث سجل سلوك"""
    try:
        data = request.get_json()
        
        supabase = get_supabase()
        response = supabase.table('behavior_records').update(data).eq('id', record_id).execute()
        
        if not response.data:
            return jsonify({'error': 'السجل غير موجود'}), 404
        
        return jsonify({
            'message': 'تم تحديث السجل بنجاح',
            'record': response.data[0]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/records/<int:record_id>', methods=['DELETE'])
def delete_behavior_record(record_id):
    """حذف سجل سلوك"""
    try:
        supabase = get_supabase()
        response = supabase.table('behavior_records').delete().eq('id', record_id).execute()
        
        if not response.data:
            return jsonify({'error': 'السجل غير موجود'}), 404
        
        return jsonify({
            'message': 'تم حذف السجل بنجاح'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

