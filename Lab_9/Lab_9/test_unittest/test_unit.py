from unittest import TestCase
from unittest.mock import patch, Mock

from flask_bcrypt import generate_password_hash

from auth import LecturerIdentity, authenticate, StudentModelIdentity

from Lab_9 import app


@patch('auth.Session')
class TestAuthenticate(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.student_password = None
        self.student_username = None
        self.hashed_student_password = None

    def setUp(self):
        app.config['SECRET_KEY'] = 'super-secret'
        self.lecturer_username = "admin-aec8084845b41a6952d46cbaa1c9b798659487ffd133796d95d05ba45d9096c2"
        self.lecturer_password = app.config['SECRET_KEY']
        self.user_username = "my-user"
        self.user_password = "my-password"
        self.hashed_user_password = generate_password_hash(self.user_password)

    def test_authenticate_lecturer(self, _Session):
        identity = authenticate(self.lecturer_username, self.lecturer_password)
        self.assertIsInstance(identity, LecturerIdentity)

    def test_authenticate_lecturer_failed(self, Session):
        Session().query().filter_by().one.return_value = Mock(
            password=self.hashed_user_password
        )
        identity = authenticate(self.lecturer_username, "invalid_password")
        self.assertIsNone(identity)

    def test_authenticate_student(self, Session):
        Session().query().filter_by().one.return_value = Mock(
            password=self.hashed_student_password
        )
        identity = authenticate(self.student_username, self.student_password)
        self.assertIsInstance(identity, StudentModelIdentity)

    def test_authenticate_student_failed(self, Session):
        Session().query().filter_by().one.return_value = Mock(
            password=self.hashed_student_password
        )
        identity = authenticate(self.student_username, "invalid_password")
        self.assertIsNone(identity)
