import hashlib
from abc import ABC, abstractmethod

from flask import session
from flask_bcrypt import check_password_hash

from models import Lecturer, Student, Course


class BaseUserIdentity(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def is_lecturer(self):
        return False


class BaseStudentIdentity(object):
    pass


class StudentModelIdentity(BaseStudentIdentity):
    def __init__(self, model):
        self.model = model

    @property
    def id(self):
        return self.model.id

    @property
    def is_lecturer(self):
        return False


class BaseLecturerIdentity(object):
    pass


class LecturerUserIdentity(BaseLecturerIdentity):
    @property
    def id(self):
        from app import app
        return hashlib.sha256(app.config['SECRET_KEY'].encode()).hexdigest()

    @property
    def is_lecturer(self):
        return True


def authenticate(username, password, lecturer_identity=None):
    from app import app
    lecturer = Lecturer()
    course = Course()
    admin_identity = LecturerIdentity()
    if username == f'lecturer-{lecturer_identity.id}' and password == app.config['SECRET_KEY']:
        return lecturer_identity
    else:
        student = course.query(Student).filter_by(email=username).one()
        if student and check_password_hash(student.password, password):
            return StudentModelIdentity(student)


class LecturerIdentity(object):
    pass


def identity(application, lecturer_identity=None):
    admin_identity = LecturerIdentity()
    if application['identity'] == lecturer_identity.id:
        return lecturer_identity
    else:
        course = Course()
        return StudentModelIdentity(
            session.query(Student).filter_by(id=application['identity']).one()
        )
