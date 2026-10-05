from flask import Flask,request,render_template
from config import Config
from extensions import db, jwt
from models import User, Student, Course, Grade
from routes.auth import auth_bp
from routes.students import students_bp
from routes.courses import courses_bp
from routes.grades import grades_bp
from routes.web_students import web_students_bp
from routes.web_courses import web_courses_bp
from routes.web_grades import web_grades_bp
from routes.analytics import analytics_bp
from routes.upload import upload_bp
from routes.reports import reports_bp
from routes.student_profile import student_profile_bp
def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(grades_bp)
    app.register_blueprint(web_students_bp)
    app.register_blueprint(web_courses_bp)
    app.register_blueprint(web_grades_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(student_profile_bp)
    with app.app_context():
        db.create_all()
        @app.route("/")
        def home():
            return render_template("home.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
