from contextlib import contextmanager
from functools import wraps

from flask import jsonify
from flask_jwt import current_identity

from Lab_9.models import Session


def db_lifecycle(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with db_session_context():
            return func(*args, **kwargs)
    return inner


@contextmanager
def db_session_context():
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    else:
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise


class StatusResponse(object):
    pass


def only_lecturer_access(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not current_identity.is_lecturer:
            return jsonify(StatusResponse().dump({
                "code": 401,
                "type": "NOT_AUTHORIZED",
                "message": "Only Lecturer is allowed to access this endpoint",
            })), 401
        return func(*args, **kwargs)
    return inner


def only_target_authorized_student_access_or_lecturer(func):
    @wraps(func)
    def inner(student_id, *args, **kwargs):
        if current_identity.id != student_id and not current_identity.is_lecturer:
            return jsonify(StatusResponse().dump({
                "code": 401,
                "type": "NOT_AUTHORIZED",
                "message": f"You're trying to access endpoint only available for student {student_id}",
            })), 401
        return func(student_id, *args, **kwargs)
    return inner
