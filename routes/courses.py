from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Course, User


courses_bp = Blueprint("courses", __name__, url_prefix="/api/courses")


def admin_required():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or user.role != "admin":
        return None

    return user


# GET ALL COURSES
@courses_bp.route("", methods=["GET"])
@jwt_required()
def get_courses():

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    courses = Course.query.all()

    data = []

    for course in courses:
        data.append({
            "id": course.id,
            "name": course.name,
            "code": course.code
        })

    return jsonify({
        "status": "success",
        "data": data
    }), 200


# CREATE COURSE
@courses_bp.route("", methods=["POST"])
@jwt_required()
def create_course():

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

    name = data.get("name")
    code = data.get("code")

    if not name or not code:
        return jsonify({
            "status": "error",
            "message": "Name and code are required"
        }), 400

    existing_course = Course.query.filter_by(code=code).first()

    if existing_course:
        return jsonify({
            "status": "error",
            "message": "Course code already exists"
        }), 409

    course = Course(
        name=name,
        code=code
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Course created successfully",
        "data": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 201


# GET COURSE BY ID
@courses_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_course(id):

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    course = Course.query.get(id)

    if not course:
        return jsonify({
            "status": "error",
            "message": "Course not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 200


# PUT - FULL UPDATE
@courses_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_course(id):

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    course = Course.query.get(id)

    if not course:
        return jsonify({
            "status": "error",
            "message": "Course not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON data is required"
        }), 400

    name = data.get("name")
    code = data.get("code")

    if not name or not code:
        return jsonify({
            "status": "error",
            "message": "Name and code are required for PUT"
        }), 400

    existing_course = Course.query.filter(
        Course.code == code,
        Course.id != id
    ).first()

    if existing_course:
        return jsonify({
            "status": "error",
            "message": "Course code already belongs to another course"
        }), 409

    course.name = name
    course.code = code

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Course updated successfully",
        "data": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 200


# PATCH - PARTIAL UPDATE
@courses_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_course(id):

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    course = Course.query.get(id)

    if not course:
        return jsonify({
            "status": "error",
            "message": "Course not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON data is required"
        }), 400

    if "name" in data:
        if not data["name"]:
            return jsonify({
                "status": "error",
                "message": "Name cannot be empty"
            }), 400

        course.name = data["name"]

    if "code" in data:

        if not data["code"]:
            return jsonify({
                "status": "error",
                "message": "Code cannot be empty"
            }), 400

        existing_course = Course.query.filter(
            Course.code == data["code"],
            Course.id != id
        ).first()

        if existing_course:
            return jsonify({
                "status": "error",
                "message": "Course code already exists"
            }), 409

        course.code = data["code"]

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Course partially updated successfully",
        "data": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 200


# DELETE COURSE
@courses_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):

    if not admin_required():
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    course = Course.query.get(id)

    if not course:
        return jsonify({
            "status": "error",
            "message": "Course not found"
        }), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Course deleted successfully"
    }), 200