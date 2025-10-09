from flask import Blueprint, request, jsonify, session
from pymongo import MongoClient
from bson.objectid import ObjectId

course_bp = Blueprint("course_bp", __name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
courses_collection = db["courses"]

@course_bp.route("/", methods=["POST"])
def add_course():
    if "user_id" not in session:
        return jsonify({"message": "กรุณา login"}), 401
    
    data = request.json
    required_fields = ["title", "subject", "dueDate", "time", "spareTime", "detail", "level", "email"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"message": "กรอกข้อมูลให้ครบ"}), 400

    # แปลง level เป็น int
    try:
        level = int(data["level"])
        if level < 1 or level > 3:
            return jsonify({"message": "level ต้องอยู่ระหว่าง 1 ถึง 3"}), 400
    except:
        return jsonify({"message": "level ต้องเป็นตัวเลข"}), 400

    courses_collection.insert_one({
        "user_id": ObjectId(session["user_id"]),
        **{k: data[k] for k in required_fields if k != "level"},
        "level": level
    })

    return jsonify({"message": "บันทึกวิชาเรียบร้อย"}), 201
