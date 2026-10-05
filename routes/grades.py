from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from extensions import db
from models import Grade, Student, Course, User


grades_bp = Blueprint("grades", __name__, url_prefix="/api/grades")


def admin_required():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or user.role != "admin":
        return None

    return user


# GET ALL GRADES
@grades_bp.route("", methods=["GET"])
@jwt_required()
def get_grades():

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    grades = Grade.query.all()

    data = []

    for grade in grades:
        data.append({
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date.isoformat()
        })

    return jsonify({
        "status": "success",
        "data": data
    }), 200


# CREATE GRADE
@grades_bp.route("", methods=["POST"])
@jwt_required()
def create_grade():

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON data is required"
        }), 400

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    score = data.get("score")
    grade_date = data.get("date")

    if student_id is None or course_id is None or score is None:
        return jsonify({
            "status": "error",
            "message": "student_id, course_id and score are required"
        }), 400

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "status": "error",
            "message": "Student not found"
        }), 404

    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "status": "error",
            "message": "Course not found"
        }), 404

    if score < 0 or score > 100:
        return jsonify({
            "status": "error",
            "message": "Score must be between 0 and 100"
        }), 400

    if grade_date:
        try:
            parsed_date = datetime.strptime(
                grade_date,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Date must be in YYYY-MM-DD format"
            }), 400
    else:
        parsed_date = datetime.today().date()

    grade = Grade(
        student_id=student_id,
        course_id=course_id,
        score=score,
        date=parsed_date
    )

    db.session.add(grade)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Grade created successfully",
        "data": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date.isoformat()
        }
    }), 201


# GET GRADE BY ID
@grades_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_grade(id):

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    grade = Grade.query.get(id)

    if not grade:
        return jsonify({
            "status": "error",
            "message": "Grade not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date.isoformat()
        }
    }), 200


# PUT - FULL UPDATE
@grades_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_grade(id):

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    grade = Grade.query.get(id)

    if not grade:
        return jsonify({
            "status": "error",
            "message": "Grade not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON data is required"
        }), 400

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    score = data.get("score")
    grade_date = data.get("date")

    if student_id is None or course_id is None or score is None:
        return jsonify({
            "status": "error",
            "message": "student_id, course_id and score are required"
        }), 400

    if not Student.query.get(student_id):
        return jsonify({
            "status": "error",
            "message": "Student not found"
        }), 404

    if not Course.query.get(course_id):
        return jsonify({
            "status": "error",
            "message": "Course not found"
        }), 404

    if score < 0 or score > 100:
        return jsonify({
            "status": "error",
            "message": "Score must be between 0 and 100"
        }), 400

    try:
        parsed_date = datetime.strptime(
            grade_date,
            "%Y-%m-%d"
        ).date()
    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "message": "Date must be in YYYY-MM-DD format"
        }), 400

    grade.student_id = student_id
    grade.course_id = course_id
    grade.score = score
    grade.date = parsed_date

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Grade updated successfully",
        "data": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date.isoformat()
        }
    }), 200


# PATCH - PARTIAL UPDATE
@grades_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_grade(id):

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    grade = Grade.query.get(id)

    if not grade:
        return jsonify({
            "status": "error",
            "message": "Grade not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON data is required"
        }), 400

    if "student_id" in data:

        if not Student.query.get(data["student_id"]):
            return jsonify({
                "status": "error",
                "message": "Student not found"
            }), 404

        grade.student_id = data["student_id"]

    if "course_id" in data:

        if not Course.query.get(data["course_id"]):
            return jsonify({
                "status": "error",
                "message": "Course not found"
            }), 404

        grade.course_id = data["course_id"]

    if "score" in data:

        if data["score"] < 0 or data["score"] > 100:
            return jsonify({
                "status": "error",
                "message": "Score must be between 0 and 100"
            }), 400

        grade.score = data["score"]

    if "date" in data:

        try:
            grade.date = datetime.strptime(
                data["date"],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Date must be in YYYY-MM-DD format"
            }), 400

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Grade partially updated successfully",
        "data": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date.isoformat()
        }
    }), 200


# DELETE GRADE
@grades_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_grade(id):

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    grade = Grade.query.get(id)

    if not grade:
        return jsonify({
            "status": "error",
            "message": "Grade not found"
        }), 404

    db.session.delete(grade)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Grade deleted successfully"
    }), 200