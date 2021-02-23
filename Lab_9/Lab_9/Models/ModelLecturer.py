from Database import db
from marshmallow import Schema, fields, validate, ValidationError


class Lecturer(db.Model):

    __tablename__ = 'lecturer'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    courses = db.Column(db.ForeignKey, nullable=False)
    department = db.Column(db.String, nullable=False)

    def __init__(self, email=None, password=None, first_name=None,
                 last_name=None, birthday=None, courses=None, department=None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.courses = courses
        self.department = department

    def add_lecturer_to_db(self):
        data = Lecturer(self.email, self.password, self.first_name,
                     self.last_name, self.birthday, self.courses, self.department)

    def read_from_db(self, lecturer_id):
        read_lecturer= Lecturer.query.filter_by(id=lecturer_id).first()
        self.first_name = read_lecturer.first_name
        self.last_name = read_lecturer.last_name
        self.birthday = read_lecturer.birthday
        self.courses = read_lecturer.course
        self.department = read_lecturer.department

    def delete_from_db(self, lecturer_id):
        delete_lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        db.session.delete(delete_lecturer)
        db.session.commit()


class LecturerSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    birthday = fields.Str(required=True)
    courses = fields.Str(required=True)
    department = fields.Str(required=True)

