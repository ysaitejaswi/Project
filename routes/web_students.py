from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Student


web_students_bp = Blueprint(
    "web_students",
    __name__
)


# =========================
# LIST STUDENTS
# =========================

@web_students_bp.route("/students", methods=["GET"])
def student_list():

    search = request.args.get("search", "").strip()

    if search:
        students = Student.query.filter(
            (Student.name.ilike(f"%{search}%")) |
            (Student.email.ilike(f"%{search}%"))
        ).all()
    else:
        students = Student.query.all()

    return render_template(
        "students/list.html",
        students=students,
        search=search
    )

# =========================
# NEW STUDENT FORM
# =========================

@web_students_bp.route("/students/new", methods=["GET"])
def student_new():

    return render_template(
        "students/new.html"
    )


# =========================
# CREATE STUDENT
# =========================

@web_students_bp.route("/students", methods=["POST"])
def student_create():

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Name and email are required", 400

    existing_student = Student.query.filter_by(
        email=email
    ).first()

    if existing_student:
        return "Email already exists", 409

    student = Student(
        name=name,
        email=email
    )

    db.session.add(student)
    db.session.commit()

    return redirect(
        url_for("web_students.student_list")
    )


# =========================
# STUDENT DETAILS
# =========================

@web_students_bp.route("/students/<int:id>", methods=["GET"])
def student_detail(id):

    student = Student.query.get(id)

    if not student:
        return "Student not found", 404

    return render_template(
        "students/detail.html",
        student=student
    )


# =========================
# EDIT FORM
# =========================

@web_students_bp.route("/students/<int:id>/edit", methods=["GET"])
def student_edit(id):

    student = Student.query.get(id)

    if not student:
        return "Student not found", 404

    return render_template(
        "students/edit.html",
        student=student
    )


# =========================
# UPDATE STUDENT
# =========================
@web_students_bp.route(
    "/students/<int:id>",
    methods=["POST"]
)
def student_update(id):
    student = Student.query.get(id)

    if not student:
        return "Student not found", 404

    method = request.form.get("_method", "POST").upper()

    if method not in ["PUT", "PATCH"]:
        return "Invalid method", 405

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Name and email are required", 400

    student.name = name
    student.email = email

    db.session.commit()

    return redirect(
        url_for("web_students.student_detail", id=student.id)
    )


@web_students_bp.route(
    "/students/<int:id>/delete",
    methods=["POST"]
)
def student_delete(id):
    student = Student.query.get(id)

    if not student:
        return "Student not found", 404

    method = request.form.get("_method", "POST").upper()

    if method != "DELETE":
        return "Invalid method", 405

    db.session.delete(student)
    db.session.commit()

    return redirect(
        url_for("web_students.student_list")
    )