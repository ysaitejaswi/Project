from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import User, Student, Grade


student_profile_bp = Blueprint(
    "student_profile",
    __name__,
    url_prefix="/api/student"
)


@student_profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def student_profile():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    student = Student.query.filter_by(
        email=user.email
    ).first()

    if not student:
        return jsonify({
            "status": "error",
            "message": "Student profile not found"
        }), 404

    grades = Grade.query.filter_by(
        student_id=student.id
    ).all()

    data = []

    for grade in grades:
        data.append({
            "course": grade.course.name,
            "course_code": grade.course.code,
            "score": grade.score,
            "date": str(grade.date)
        })

    return jsonify({
        "status": "success",
        "data": {
            "student": {
                "id": student.id,
                "name": student.name,
                "email": student.email
            },
            "grades": data
        }
    }), 200