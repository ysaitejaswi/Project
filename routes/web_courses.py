from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Course

web_courses_bp = Blueprint("web_courses", __name__)


# =========================
# COURSE LIST + SEARCH
# =========================
@web_courses_bp.route("/courses", methods=["GET"])
def course_list():

    search = request.args.get("search", "").strip()

    if search:
        courses = Course.query.filter(
            (Course.name.ilike(f"%{search}%")) |
            (Course.code.ilike(f"%{search}%"))
        ).all()
    else:
        courses = Course.query.all()

    return render_template(
        "courses/list.html",
        courses=courses,
        search=search
    )


# =========================
# NEW COURSE PAGE
# =========================
@web_courses_bp.route("/courses/new", methods=["GET"])
def course_new():
    return render_template("courses/new.html")


# =========================
# CREATE COURSE
# =========================
@web_courses_bp.route("/courses", methods=["POST"])
def course_create():

    name = request.form.get("name")
    code = request.form.get("code")

    if not name or not code:
        return "Course name and code are required", 400

    existing_course = Course.query.filter_by(code=code).first()

    if existing_course:
        return "Course code already exists", 409

    course = Course(
        name=name,
        code=code
    )

    db.session.add(course)
    db.session.commit()

    return redirect(url_for("web_courses.course_list"))


# =========================
# COURSE DETAIL
# =========================
@web_courses_bp.route("/courses/<int:id>", methods=["GET"])
def course_detail(id):

    course = Course.query.get(id)

    if not course:
        return "Course not found", 404

    return render_template(
        "courses/detail.html",
        course=course
    )


# =========================
# COURSE EDIT PAGE
# =========================
@web_courses_bp.route("/courses/<int:id>/edit", methods=["GET"])
def course_edit(id):

    course = Course.query.get(id)

    if not course:
        return "Course not found", 404

    return render_template(
        "courses/edit.html",
        course=course
    )


# =========================
# UPDATE COURSE
# =========================
@web_courses_bp.route("/courses/<int:id>", methods=["POST"])
def course_update(id):

    course = Course.query.get(id)

    if not course:
        return "Course not found", 404

    method = request.form.get("_method", "POST").upper()

    if method not in ["PUT", "PATCH"]:
        return "Invalid method", 405

    name = request.form.get("name")
    code = request.form.get("code")

    if not name or not code:
        return "Course name and code are required", 400

    existing_course = Course.query.filter(
        Course.code == code,
        Course.id != id
    ).first()

    if existing_course:
        return "Course code already exists", 409

    course.name = name
    course.code = code

    db.session.commit()

    return redirect(
        url_for(
            "web_courses.course_detail",
            id=course.id
        )
    )


# =========================
# DELETE COURSE
# =========================
@web_courses_bp.route("/courses/<int:id>/delete", methods=["POST"])
def course_delete(id):

    course = Course.query.get(id)

    if not course:
        return "Course not found", 404

    method = request.form.get("_method", "POST").upper()

    if method != "DELETE":
        return "Invalid method", 405

    db.session.delete(course)
    db.session.commit()

    return redirect(
        url_for("web_courses.course_list")
    )