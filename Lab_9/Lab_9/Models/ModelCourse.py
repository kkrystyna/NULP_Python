from Database import db
from marshmallow import Schema, fields, validate, ValidationError


class Course(db.Model):

    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)


    def __init__(self, name=None, amount=None):
        self.name = name
        self.amount = amount

    def add_car_to_db(self):
        data = Course(self.name, self.amount)
        db.session.add(data)
        db.session.commit()

    def read_from_db(self, course_id, read_course=None):
        read_car = Course.query.filter_by(id=course_id).first()
        self.name = read_course.name
        self.amount = read_course.amount

    def read_from_db_all(self, course_id):
        read_course = Course.query.filter_by().all()
        self.id =read_course.id
        self.name = read_course.name
        self.amount = read_course.amount

    def update_db(self, course_id):
        update_course = Course.query.filter_by(id=course_id).first()
        self.amount = update_course.new_amount

    def delete_from_db(self, course_id):
        delete_course = Course.query.filter_by(id=course_id).first()
        db.session.delete(delete_course)
        db.session.commit()


class CourseSchema(Schema):
    name = fields.Str(validate=validate.Length(max=30), required=True)
    amount = fields.Int(validate=[validate.Range(min=1,max=5)], required=True)
