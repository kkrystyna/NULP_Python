from Models.ModelLecturer import Lecturer, LecturerSchema
from marshmallow import ValidationError
from flask import jsonify
from Database import db, bcrypt
import datetime


class LecturerController(object):

    def create(self, lecturer_data=None):
        email = lecturer_data.get('email')
        password = lecturer_data.get('password')
        pw_hash = bcrypt.generate_password_hash('password')
        first_name = lecturer_data.get('first_name')
        last_name = lecturer_data.get('last_name')
        birthday = lecturer_data.get('birthday')
        courses = lecturer_data.get('courses')
        department = lecturer_data.get('department')
        birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
        lecturer = Lecturer(email, pw_hash, first_name, last_name, birthday_date, courses, department)

        try:
            result = LecturerSchema().load(lecturer_data)
        except ValidationError as err:
            return jsonify(message="Error!", status=400)

        if email and password and first_name and last_name and birthday and courses and department:
            db.session.add(lecturer)
            db.session.commit()
            return jsonify(message="The user is created !", status=200)
        else:
            return jsonify(message="Missing values !", status=404)

    def read(self,lecturer_id=None):
        lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        if lecturer is None:
            return jsonify(message="The user was not found", status=404)
        else:
            return jsonify({'   first_name': lecturer.first_name, '   last name':  lecturer.last_name, '   birthday': lecturer.birthday,'   courses': lecturer.courses, '  department': lecturer.department, '   status': 200})

    def delete(self, lecturer_id=None):
        lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        if lecturer is None:
            return jsonify(message="The user was not found", status=404)
        else:
            lecturer.delete_from_db(lecturer_id)
            return jsonify(message="User was deleted !", status=200)
