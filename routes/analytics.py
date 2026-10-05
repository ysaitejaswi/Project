from flask import Blueprint, render_template, request

import pandas as pd
import numpy as np

from models import Grade, Student, Course


analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("/analytics", methods=["GET"])
def analytics():

    course_id = request.args.get("course_id")
    student_id = request.args.get("student_id")

    # Get all grades
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

    # Create DataFrame
    df = pd.DataFrame(data)

    courses = Course.query.all()
    students = Student.query.all()

    # Empty data handling
    if df.empty:

        return render_template(
            "analytics.html",
            courses=courses,
            students=students,
            selected_course=course_id,
            selected_student=student_id,
            average_by_course=[],
            rankings=[],
            mean=0,
            median=0,
            std_dev=0
        )

    # Filter by course
    if course_id:
        df = df[
            df["course_id"] == int(course_id)
        ]

    # Filter by student
    if student_id:
        df = df[
            df["student_id"] == int(student_id)
        ]

    # Statistics
    mean = np.mean(df["score"])
    median = np.median(df["score"])
    std_dev = np.std(df["score"])

    # Average grade by course
    average_by_course = (
        df.groupby("course_name")["score"]
        .mean()
        .reset_index()
    )

    average_by_course = average_by_course.to_dict(
        "records"
    )

    # Student ranking
    rankings = (
        df.groupby(
            ["student_id", "student_name"]
        )["score"]
        .mean()
        .reset_index()
        .sort_values(
            "score",
            ascending=False
        )
    )

    rankings = rankings.to_dict(
        "records"
    )

    return render_template(
        "analytics.html",
        courses=courses,
        students=students,
        selected_course=course_id,
        selected_student=student_id,
        average_by_course=average_by_course,
        rankings=rankings,
        mean=round(float(mean), 2),
        median=round(float(median), 2),
        std_dev=round(float(std_dev), 2)
    )