from Database import db
from marshmallow import Schema, fields, validate, ValidationError


class Student(db.Model):

    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    courses = db.Column(db.ForeignKey, nullable=False)
    collective = db.Column(db.String, nullable=False)

    def __init__(self, email=None, password=None, first_name=None,
                 last_name=None, birthday=None, collective=None, courses=None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.courses = courses
        self.collective = collective

    def add_student_to_db(self):
        data = Student(self.email, self.password, self.first_name,
                     self.last_name, self.birthday, self.courses, self.collective)

    def read_from_db(self, student_id):
        read_student = Student.query.filter_by(id=student_id).first()
        self.first_name = read_student.first_name
        self.last_name = read_student.last_name
        self.birthday = read_student.birthday
        self.courses = read_student.course
        self.collective = read_student.collective

    def delete_from_db(self, student_id):
        delete_student = Student.query.filter_by(id=student_id).first()
        db.session.delete(delete_student)
        db.session.commit()


class StudentSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    birthday = fields.Str(required=True)
    courses = fields.Str(required=True)
    collective = fields.Str(required=True)


