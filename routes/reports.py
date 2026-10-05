from flask import Blueprint, send_file
import pandas as pd
from io import BytesIO

from models import Grade


reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/grades/csv", methods=["GET"])
def export_csv():

    grades = Grade.query.all()

    data = []

    for grade in grades:
        data.append({
            "student_id": grade.student_id,
            "student_name": grade.student.name,
            "course_id": grade.course_id,
            "course_name": grade.course.name,
            "score": grade.score,
            "date": grade.date
        })

    df = pd.DataFrame(data)

    output = BytesIO()

    df.to_csv(output, index=False)

    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="grades_report.csv"
    )


@reports_bp.route("/reports/grades/excel", methods=["GET"])
def export_excel():

    grades = Grade.query.all()

    data = []

    for grade in grades:
        data.append({
            "student_id": grade.student_id,
            "student_name": grade.student.name,
            "course_id": grade.course_id,
            "course_name": grade.course.name,
            "score": grade.score,
            "date": grade.date
        })

    df = pd.DataFrame(data)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Grades"
        )

    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="grades_report.xlsx"
    )