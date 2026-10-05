from flask import Blueprint, render_template, request, redirect, url_for

from extensions import db
from models import Grade, Student, Course


web_grades_bp = Blueprint(
    "web_grades",
    __name__
)


# =========================
# LIST GRADES
# =========================

@web_grades_bp.route("/grades", methods=["GET"])
def grade_list():

    grades = Grade.query.all()

    return render_template(
        "grades/list.html",
        grades=grades
    )


# =========================
# NEW GRADE FORM
# =========================

@web_grades_bp.route("/grades/new", methods=["GET"])
def grade_new():

    students = Student.query.all()
    courses = Course.query.all()

    return render_template(
        "grades/new.html",
        students=students,
        courses=courses
    )


# =========================
# CREATE GRADE
# =========================

@web_grades_bp.route("/grades", methods=["POST"])
def grade_create():

    student_id = request.form.get("student_id")
    course_id = request.form.get("course_id")
    score = request.form.get("score")
    grade_date = request.form.get("date")

    if not student_id or not course_id or not score or not grade_date:
        return "All fields are required", 400

    student = Student.query.get(student_id)
    course = Course.query.get(course_id)

    if not student:
        return "Student not found", 404

    if not course:
        return "Course not found", 404

    score = float(score)

    if score < 0 or score > 100:
        return "Score must be between 0 and 100", 400

    grade = Grade(
        student_id=student_id,
        course_id=course_id,
        score=score,
        date=grade_date
    )

    db.session.add(grade)
    db.session.commit()

    return redirect(
        url_for("web_grades.grade_list")
    )
# =========================
# EDIT GRADE FORM
# =========================

@web_grades_bp.route("/grades/<int:id>/edit", methods=["GET"])
def grade_edit(id):

    grade = Grade.query.get(id)

    if not grade:
        return "Grade not found", 404

    students = Student.query.all()
    courses = Course.query.all()

    return render_template(
        "grades/edit.html",
        grade=grade,
        students=students,
        courses=courses
    )


# =========================
# UPDATE GRADE
# =========================
@web_grades_bp.route(
    "/grades/<int:id>",
    methods=["POST"]
)
def grade_update(id):
    grade = Grade.query.get(id)

    if not grade:
        return "Grade not found", 404

    method = request.form.get("_method", "POST").upper()

    if method not in ["PUT", "PATCH"]:
        return "Invalid method", 405

    student_id = request.form.get("student_id")
    course_id = request.form.get("course_id")
    score = request.form.get("score")
    grade_date = request.form.get("date")

    if not student_id or not course_id or not score or not grade_date:
        return "All fields are required", 400

    student = Student.query.get(student_id)
    course = Course.query.get(course_id)

    if not student:
        return "Student not found", 404

    if not course:
        return "Course not found", 404

    score = float(score)

    if score < 0 or score > 100:
        return "Score must be between 0 and 100", 400

    grade.student_id = student_id
    grade.course_id = course_id
    grade.score = score
    grade.date = grade_date

    db.session.commit()

    return redirect(
        url_for("web_grades.grade_list")
    )


@web_grades_bp.route(
    "/grades/<int:id>/delete",
    methods=["POST"]
)
def grade_delete(id):
    grade = Grade.query.get(id)

    if not grade:
        return "Grade not found", 404

    method = request.form.get("_method", "POST").upper()

    if method != "DELETE":
        return "Invalid method", 405

    db.session.delete(grade)
    db.session.commit()

    return redirect(
        url_for("web_grades.grade_list")
    )