import random
import math
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo 

exam_plan_bp = Blueprint('exam_plan_api', __name__)


def get_duration_minutes(start_str, end_str):
    """คำนวณเวลาเป็นนาที จาก 'HH:MM' สองค่า"""
    try:
        FMT = '%H:%M'
        tdelta = datetime.strptime(end_str, FMT) - datetime.strptime(start_str, FMT)
        return tdelta.total_seconds() / 60
    except Exception:
        return 0


@exam_plan_bp.route('/api/exam-plan/', methods=['POST'])
@jwt_required()
def create_exam_plan():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        exam_title = data.get('examTitle')
        exam_subjects = data.get('examSubjects') 
        exam_date = data.get('examDate')
        study_plan = data.get('studyPlan')   

        if not all([exam_title, exam_subjects, exam_date, study_plan]):
            return jsonify({'message': 'ข้อมูลไม่ครบถ้วน'}), 400

        BLOCK_DURATION_MINUTES = 60 
        total_available_minutes = 0
        available_days_with_duration = []

        for day in study_plan:
            duration = get_duration_minutes(day['startTime'], day['endTime'])
            if duration > 0:
                total_available_minutes += duration
                available_days_with_duration.append({
                    'date': day['date'],
                    'duration': duration,
                    'num_blocks': math.floor(duration / BLOCK_DURATION_MINUTES) 
                })
        
        if total_available_minutes == 0:
            return jsonify({'message': 'คุณไม่มีเวลาว่างสำหรับเตรียมตัวเลย'}), 400

        total_priority_weight = sum(s.get('priority', 1) for s in exam_subjects)
        if total_priority_weight == 0:
            return jsonify({'message': 'ค่า Priority ของวิชาไม่ถูกต้อง'}), 400
        

        total_blocks = math.floor(total_available_minutes / BLOCK_DURATION_MINUTES)
        study_blocks_list = []

        for subject in exam_subjects:
            subject_name = subject.get('name')
            priority_ratio = subject.get('priority', 1) / total_priority_weight
            
            num_blocks_for_subject = round(priority_ratio * total_blocks) 
            
            study_blocks_list.extend([subject_name] * num_blocks_for_subject)

        random.shuffle(study_blocks_list)

        final_schedule = []
        block_index = 0 

        for day in available_days_with_duration:
            day_schedule = {
                'date': day['date'],
                'slots': []
            }
            
            for _ in range(day['num_blocks']):
                if block_index < len(study_blocks_list):
                    subject_to_study = study_blocks_list[block_index]
                    day_schedule['slots'].append({
                        'subject': subject_to_study,
                        'duration': BLOCK_DURATION_MINUTES
                    })
                    block_index += 1
                else:
                    break
            
            if day_schedule['slots']: 
                final_schedule.append(day_schedule)

        new_plan = {
            'user_id': user_id,
            'exam_title': exam_title,
            'exam_date': exam_date,
            'original_subjects_input': exam_subjects, 
            'generated_schedule': final_schedule,     
            'created_at': datetime.utcnow()
        }

        mongo.db.exam_plans.insert_one(new_plan)

        return jsonify({
            'message': 'สร้างแผนการสอบสำเร็จ!',
            'schedule': final_schedule 
        }), 201

    except Exception as e:
        print(f"Error creating exam plan: {e}")
        return jsonify({'message': f'เกิดข้อผิดพลาด: {str(e)}'}), 500

@exam_plan_bp.route('/api/exam-plans/', methods=['GET'])
@jwt_required()
def get_exam_plans():
    try:
        user_id = get_jwt_identity()
        
        plans = mongo.db.exam_plans.find({'user_id': user_id})
        
        result = []
        for plan in plans:
            plan['_id'] = str(plan['_id'])
            
            result.append(plan)
            
        return jsonify(result), 200

    except Exception as e:
        print(f"Error fetching exam plans: {e}")
        return jsonify({'message': f'เกิดข้อผิดพลาด: {str(e)}'}), 500