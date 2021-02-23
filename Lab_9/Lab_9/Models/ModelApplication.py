from Database import db
from marshmallow import Schema, fields, validate, ValidationError

class Application(db.Model):

    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    lecturer = db.relationship('Lecturer', backref='lecturer')
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    student = db.relationship('Student', backref='student')
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course = db.relationship('Course', backref='course', uselist=False)

    def __init__(self, lecturer=None, course=None, student=None):
        self.lecturer = lecturer
        self.student = student
        self.course = course


    def read_from_db(self, aplication_id):
        read_application = Application.query.filter_by().all()
        self.lecturer = read_application.lecturer
        self.student = read_application.student
        self.course = read_application.course



class ApplicationSchema(Schema):
    lecturer_id = fields.Str(required=True)
    student_id = fields.Str(required=True)
    course_id = fields.Str(required=True)

