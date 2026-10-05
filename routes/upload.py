from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd

from extensions import db
from models import Grade, Student, Course


upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload/grades", methods=["GET"])
def upload_grades_page():
    return render_template("upload_grades.html")


@upload_bp.route("/upload/grades", methods=["POST"])
def upload_grades():
    file = request.files.get("file")

    if not file:
        return "Please select a CSV file", 400

    if file.filename == "":
        return "No file selected", 400

    if not file.filename.lower().endswith(".csv"):
        return "Only CSV files are allowed", 400

    try:
        df = pd.read_csv(file)

        required_columns = [
            "student_id",
            "course_id",
            "score",
            "date"
        ]

        for column in required_columns:
            if column not in df.columns:
                return f"Missing column: {column}", 400

        for _, row in df.iterrows():

            student = Student.query.get(int(row["student_id"]))
            course = Course.query.get(int(row["course_id"]))

            if not student:
                return f"Student ID {row['student_id']} not found", 404

            if not course:
                return f"Course ID {row['course_id']} not found", 404

            score = float(row["score"])

            if score < 0 or score > 100:
                return f"Invalid score: {score}", 400

            grade = Grade(
                student_id=int(row["student_id"]),
                course_id=int(row["course_id"]),
                score=score,
                date=row["date"]
            )

            db.session.add(grade)

        db.session.commit()

        return redirect(url_for("web_grades.grade_list"))

    except Exception as e:
        db.session.rollback()
        return f"Upload failed: {str(e)}", 400