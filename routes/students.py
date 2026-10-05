from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Student, User


students_bp = Blueprint("students", __name__, url_prefix="/api/students")


# Check whether logged-in user is an Admin
def admin_required():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return None

    if user.role != "admin":
        return None

    return user


# ---------------------------------------------------
# GET ALL STUDENTS
# GET /api/students
# ---------------------------------------------------
@students_bp.route("", methods=["GET"])
@jwt_required()
def get_students():

    user = admin_required()

    if not user:
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    students = Student.query.all()

    data = []

    for student in students:
        data.append({
            "id": student.id,
            "name": student.name,
            "email": student.email
        })

    return jsonify({
        "status": "success",
        "data": data
    }), 200


# ---------------------------------------------------
# CREATE STUDENT
# POST /api/students
# ---------------------------------------------------
@students_bp.route("", methods=["POST"])
@jwt_required()
def create_student():

    user = admin_required()

    if not user:
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
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "status": "error",
            "message": "Name and email are required"
        }), 400

    existing_student = Student.query.filter_by(email=email).first()

    if existing_student:
        return jsonify({
            "status": "error",
            "message": "Student email already exists"
        }), 409

    student = Student(
        name=name,
        email=email
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Student created successfully",
        "data": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 201


# ---------------------------------------------------
# GET ONE STUDENT
# GET /api/students/<id>
# ---------------------------------------------------
@students_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_student(id):

    user = admin_required()

    if not user:
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "status": "error",
            "message": "Student not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 200


# ---------------------------------------------------
# PUT - FULL UPDATE
# PUT /api/students/<id>
# ---------------------------------------------------
@students_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_student(id):

    user = admin_required()

    if not user:
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "status": "error",
            "message": "Student not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "JSON data is required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "status": "error",
            "message": "Name and email are required for PUT"
        }), 400

    existing_student = Student.query.filter(
        Student.email == email,
        Student.id != id
    ).first()

    if existing_student:
        return jsonify({
            "status": "error",
            "message": "Email already belongs to another student"
        }), 409

    student.name = name
    student.email = email

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Student updated successfully",
        "data": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 200


# ---------------------------------------------------
# PATCH - PARTIAL UPDATE
# PATCH /api/students/<id>
# ---------------------------------------------------
@students_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_student(id):

    user = admin_required()

    if not user:
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "status": "error",
            "message": "Student not found"
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

        student.name = data["name"]

    if "email" in data:

        if not data["email"]:
            return jsonify({
                "status": "error",
                "message": "Email cannot be empty"
            }), 400

        existing_student = Student.query.filter(
            Student.email == data["email"],
            Student.id != id
        ).first()

        if existing_student:
            return jsonify({
                "status": "error",
                "message": "Email already belongs to another student"
            }), 409

        student.email = data["email"]

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Student partially updated successfully",
        "data": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 200


# ---------------------------------------------------
# DELETE STUDENT
# DELETE /api/students/<id>
# ---------------------------------------------------
@students_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_student(id):

    user = admin_required()

    if not user:
        return jsonify({
            "status": "error",
            "message": "Admin access required"
        }), 403

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "status": "error",
            "message": "Student not found"
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Student deleted successfully"
    }), 200