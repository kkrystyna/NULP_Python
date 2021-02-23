from Models.ModelApplication import Application, ApplicationSchema
from Models.ModelStudent import Student
from Models.ModelLecturer import Lecturer
from Models.ModelCourse import Course
from marshmallow import ValidationError
from flask import jsonify
from Database import db
from re import *
import datetime

class ApplicationController(object):

    def create(self, application_data=None, lecturer_id=None, course_id=None, student_id=None):
        lecturer = Lecturer.query.filter_by(id=lecturer_id).first()
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        application = Application(lecturer, course, student)

        try:
            result = ApplicationSchema().load(application_data)
        except ValidationError as err:
            return jsonify(message="ERROR", status=400)
            #return err.messages

        if student and course :
            db.session.add(course)
            db.session.commit()
            return jsonify(message="The application is created !", status=200)

    def read(self, application_id=None):
        return Application.query.filter_by().all()