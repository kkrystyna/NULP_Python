from Models.ModelCourse import Course, CourseSchema
from Models.ModelStudent import Student
from Models.ModelLecturer import Lecturer
from marshmallow import ValidationError
from flask import jsonify
from Database import db

class CourseController(object):

    def create(self, course_data=None):
        name = course_data.get('name')
        amount = course_data.get('amount')

        course = Course(name, amount)
        student_id = course_data.get('student_id')
        student = Student.query.filter_by(id=student_id).first()
        if student is True:
            return jsonify(message="You do not have access!", status=403)

        try:
            result = CourseSchema().load(course_data)
        except ValidationError as err:
            return jsonify(message="Error", status=400)

        if name and amount:
            db.session.add(course)
            db.session.commit()
            return jsonify(message="The course is created !", status=200)
        else:
            return jsonify(message="Missing values !", status=404)

    def read(self, course_id=None):
        course = Course.query.filter_by(id=course_id).first()
        #car = Cars()
        if course is None:
            return jsonify(message="The course was not found", status=404)
        else:
            course.read_from_db(course_id)
            return jsonify({'Name': course.name, 'price': course.amount, 'status': 200})

    def read_all(self, course_id=None):
        return Course.query.filter_by().all()

    def update_course(self, course_id=None, course_data=None):
        new_amount = course_data.get('new_amount')
        course = Course.query.filter_by(id=course_id).first()
        student_id = course_data.get('student_id')
        student = Student.query.filter_by(id=student_id).first()
        if student is True:
            return jsonify(message="You do not have access!", status=403)

        if new_amount:
            course.amount = new_amount
            db.session.add(course)
            db.session.commit()
            return jsonify(message="Car was updated !", status=200)
        else:
            return jsonify(message="Missing values !", status=404)

    def delete(self, course_id=None, student_id=None, lecturer_id=None):
        course = Course.query.filter_by(id=course_id).first()
        student = Student.query.filter_by(id=student_id).first()
        if student is True:
            return jsonify(message="You do not have access!", status=403)
        if course is None:
            return jsonify(message="The course was not found", status=404)
        else:
            course.delete_from_db(course_id)
            return jsonify(message="Course was deleted !", status=200)


