from Models.ModelStudent import Student, StudentSchema
from marshmallow import ValidationError
from flask import jsonify
from Database import db, bcrypt
import datetime


class StudentController(object):

    def create(self, student_data=None):
        email = student_data.get('email')
        password = student_data.get('password')
        pw_hash = bcrypt.generate_password_hash('password')
        first_name = student_data.get('first_name')
        last_name = student_data.get('last_name')
        birthday = student_data.get('birthday')
        courses = student_data.get('courses')
        collective = student_data.get('collective')
        birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
        student = Student(email, pw_hash, first_name, last_name, birthday_date, courses, collective)

        try:
            result = StudentSchema().load(student_data)
        except ValidationError as err:
            return jsonify(message="Error!", status=400)

        if email and password and first_name and last_name and birthday and courses and collective:
            db.session.add(student)
            db.session.commit()
            return jsonify(message="The user is created !", status=200)
        else:
            return jsonify(message="Missing values !", status=404)

    def read(self, student_id=None):
        student = Student.query.filter_by(id=student_id).first()
        if student is None:
            return jsonify(message="The user was not found", status=404)
        else:
            return jsonify({'   first_name': student.first_name, '   last name':  student.last_name, '   birthday': student.birthday,'   courses': student.courses, '  collective': student.collective, '   status': 200})

    def delete(self, student_id=None):
        student = Student.query.filter_by(id=student_id).first()
        if student is None:
            return jsonify(message="The user was not found", status=404)
        else:
            student.delete_from_db(student_id)
            return jsonify(message="User was deleted !", status=200)
