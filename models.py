from dbinit import db


class Lecturer(db.Model):
    __tablename__ = "lecturer"

    id_lecturer = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birthday = db.Column(db.DateTime)
    department = db.Column(db.String)


class Student(db.Model):
    __tablename__ = "student"

    id_student = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birthday = db.Column(db.DateTime)
    collective = db.Column(db.String)


class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    amount_of_students = db.Column(db.Integer)


class Application(db.Model):
    __tablename__ = "application"

    id_application = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, primary_key=True)
    student = db.relationship("Student", backref="student")
    id_lecturer = db.Column(db.Integer, primary_key=True)
    lector = db.relationship("Lector", backref="lector")
    id_course = db.Column(db.Integer, primary_key=True)
    course = db.relationship("Course", backref="course")