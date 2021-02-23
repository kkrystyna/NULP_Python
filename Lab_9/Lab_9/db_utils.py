import os
import sys

from models import Session, Student, Lecturer, Course, Application

sys.path.append(os.getcwd())

def list_lecturer(email=None, first_name=None, last_name=None):
    session = Session()
    filters = []
    if email:
        filters.append(Lecturer.email.like(email))
    if first_name:
        filters.append(Lecturer.email.like(first_name))
    if last_name:
        filters.append(Lecturer.email.like(last_name))
    return session.query(Lecturer).filter(*filters).all()


def list_student(email=None, first_name=None, last_name=None):
    session = Session()
    filters = []
    if email:
        filters.append(Student.email.like(email))
    if first_name:
        filters.append(Student.email.like(first_name))
    if last_name:
        filters.append(Student.email.like(last_name))
    return session.query(Student).filter(*filters).all()


def list_course(*filters):
    session = Session()
    return (
        session.query(Course)
        .join(Student)
        .filter(*filters)
        .all()
    )


def list_application_for_course(student_id, course_id, lecturer_id, application_from):
    session = Session()
    session.query(Course).filter_by(id=course_id, owner_id=lecturer_id).one()
    transactions_from = (
        session.query(Application)
        .join(Course, Application.from_student_id == Student.id)
        .filter(
            Course.owner_id == lecturer_id, Application.from_student_id == student_id
        )
    )
    application_to = (
        session.query(Application)
        .join(Course, Application.to_course_uid == Course.id)
        .filter(
            Course.owner_id == lecturer_id, Application.to_course_id == course_id
        )
    )
    return (
        application_from.union(application_to)
        .order_by(Application.datetime)
        .all()
    )


def create_entry(model_class, *, commit=True, **kwargs):
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


def get_entry_by_id(model_class, id, **kwargs):
    session = Session()
    return session.query(model_class).filter_by(id=id, **kwargs).one()


def update_entry(entry, *, commit=True, **kwargs):
    session = Session()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry


def delete_entry(model_class, id, *, commit=True, **kwargs):
    session = Session()
    session.query(model_class).filter_by(id=id, **kwargs).delete()
    if commit:
        session.commit()
