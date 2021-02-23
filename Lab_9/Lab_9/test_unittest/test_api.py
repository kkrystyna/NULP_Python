from datetime import datetime
from unittest import TestCase
from unittest.mock import ANY

from flask import url_for
from flask_bcrypt import generate_password_hash

from Models import Lecturer, Student, Course, Application, Session
from flask_sqlalchemy import Model

from Lab_9 import app, db_utils
from Lab_9.models import engine


class BaseTestCase(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.client = None
        self.student_2_data = None

    def setUp(self):
        super().setUp()
        self.create_tables()

        self.lecturer_credentials = {
            "lecturername": "lecturer-aec8084845b41a6952d46cbaa1c9b798659487ffd133796d95d05ba45d9096c2",
            "password": "super-secret",
        }

        self.student_1_data = {
            "email": "test_1@example.com",
            "password": "123",
            "first_name": "First1",
            "last_name": "Last1",
        }
        self.student_1_data_hashed = {
            **self.student_1_data,
            "password": generate_password_hash(self.student_1_data["password"]),
        }
        self.student_1_credentials = {
            "studentname": self.student_1_data["email"],
            "password": self.student_1_data["password"],
        }

        selfstudent_2_data = {
            "email": "test_2@example.com",
            "password": "123",
            "first_name": "First2",
            "last_name": "Last2",
        }
        self.student_2_data_hashed = {
            **self.student_2_data,
            "password": generate_password_hash(self.student_2_data["password"]),
        }
        self.student_2_credentials = {
            "studentname": self.student_2_data["email"],
            "password": self.student_2_data["password"],
        }

        self.course_1_data = {"name": "Course A", "lecturer_id": None, "amount": 0}
        self.course_2_data = {"name": "Course B", "lecturer_id": None, "amount": 0}
        self.course_3_data = {"name": "Course B", "lecturer_id": None, "amount": 0}

    def tearDown(self):
        self.close_session()

    def create_tables(self):
        Model.metadata.drop_all(engine)
        Model.metadata.create_all(engine)

    def close_session(self):
        Session().close()

    def create_app(self):
        return app

    def get_auth_headers(self, credentials):
        resp = self.client.post(url_for("auth"), json=credentials)
        access_token = resp.json["access_token"]
        return {'AUthorization': f'JWT {access_token}'}


class TestAuthentication(BaseTestCase):
    def test_lecturer_auth(self):
        resp = self.client.post(url_for("auth"), json=self.lecturer_credentials)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"access_token": ANY})

    def test_student_auth(self):
        db_utils.create_entry(Student, **self.student_1_data_hashed)

        resp = self.client.post(url_for("auth"), json=self.student_1_credentials)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"access_token": ANY})


class TestListStudents(BaseTestCase):
    def test_list_students(self):
        db_utils.create_entry(Student, **self.student_1_data_hashed)
        db_utils.create_entry(Student, **self.student_2_data_hashed)

        resp = self.client.get(
            url_for("api.list_students"),
            headers=self.get_auth_headers(self.lecturer_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, [
            {
                'id': ANY,
                'email': self.student_1_data['email'],
                'first_name': self.student_1_data['first_name'],
                'last_name': self.student_1_data['last_name'],
            },
            {
                'id': ANY,
                'email': self.student_2_data['email'],
                'first_name': self.student_2_data['first_name'],
                'last_name': self.student_2_data['last_name'],
            },
        ])

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.list_students"))
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })

    def test_not_admin(self):
        db_utils.create_entry(Student, **self.student_1_data_hashed)

        resp = self.client.get(
            url_for("api.list_students"),
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })


class TestCreateStudent(BaseTestCase):
    def test_create_student(self):
        resp = self.client.post(
            url_for("api.create_student"),
            json=self.student_1_data,
            headers=self.get_auth_headers(self.lecturer_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'id': ANY,
            'email': self.student_1_data['email'],
            'first_name': self.student_1_data['first_name'],
            'last_name': self.student_1_data['last_name'],
        })
        self.assertTrue(
            Session().query(Student).filter_by(email=self.student_1_data['email']).one()
        )

    def test_unauthorized(self):
        resp = self.client.post(url_for("api.create_student"), json=self.student_1_data)

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertFalse(
            Course().query(Student).filter_by(email=self.student_1_data['email']).one_or_none()
        )

    def test_not_lecturer(self):
        db_utils.create_entry(Student, **self.student_1_data_hashed)

        resp = self.client.post(
            url_for("api.create_student"),
            json=self.student_2_data,
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertFalse(
            Session().query(Student).filter_by(email=self.student_2_data['email']).one_or_none()
        )


class TestGetStudent(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.student = db_utils.create_entry(Student, **self.student_1_data_hashed)

    def test_get_student_by_id(self):
        resp = self.client.get(
            url_for("api.get_student_by_id", student_id=self.student.id),
            headers=self.get_auth_headers(self.lecturer_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'id': self.student.id,
            'email': self.student_1_data['email'],
            'first_name': self.student_1_data['first_name'],
            'last_name': self.student_1_data['last_name'],
        })

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.get_student_by_id", student_id=self.student.id))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })

    def test_not_lecturerf(self):
        resp = self.client.get(
            url_for("api.get_student_by_id", student_id=self.student.id),
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'id': self.student.id,
            'email': self.student_1_data['email'],
            'first_name': self.student_1_data['first_name'],
            'last_name': self.student_1_data['last_name'],
        })


class TestUpdateStudent(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.student_1 = db_utils.create_entry(Student, **self.student_1_data_hashed)
        self.student_2 = db_utils.create_entry(Student, **self.student_2_data_hashed)

    def test_update_student(self):
        resp = self.client.put(
            url_for("api.update_student", student_id=self.student_1.id),
            json={
                **self.student_1_data,
                "first_name": "UpdatedFirst"
            },
            headers=self.get_auth_headers(self.lecturer_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
            'message': ANY
        })
        self.assertTrue(
            Session().query(Student).filter_by(first_name='UpdatedFirst').one()
        )

    def test_unauthorized(self):
        resp = self.client.put(
            url_for("api.update_student", student_id=self.student_1.uid),
            json={
                **self.student_1_data,
                "first_name": "UpdatedFirst"
            },
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertFalse(
            Session().query(Student).filter_by(first_name='UpdatedFirst').one_or_none()
        )

    def test_self_update(self):
        resp = self.client.put(
            url_for("api.update_student", student_id=self.student_1.id),
            json={
                **self.student_1_data,
                "first_name": "UpdatedFirst"
            },
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
            'message': ANY
        })
        self.assertTrue(
            Session().query(Student).filter_by(first_name='UpdatedFirst').one()
        )

    def test_update_another_student(self):
        resp = self.client.put(
            url_for("api.update_student", student_id=self.student_2.id),
            json={
                **self.student_2_data,
                "first_name": "UpdatedFirst"
            },
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertFalse(
            Session().query(Student).filter_by(first_name='UpdatedFirst').one_or_none()
        )


class TestDeleteStudent(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.student_1 = db_utils.create_entry(Student, **self.student_1_data_hashed)
        self.student_2 = db_utils.create_entry(Student, **self.student_2_data_hashed)

    def test_delete_student(self):
        resp = self.client.delete(
            url_for("api.delete_student", student_id=self.student_1.id),
            headers=self.get_auth_headers(self.lecturer_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
            'message': ANY
        })
        self.assertFalse(
            Session().query(Student).filter_by(id=self.student_1.id).one_or_none()
        )

    def test_unauthorized(self):
        resp = self.client.delete(url_for("api.delete_student", student_id=self.student_1.id))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertTrue(
            Session().query(Student).filter_by(id=self.student_1.id).one_or_none()
        )

    def test_self_delete(self):
        resp = self.client.delete(
            url_for("api.delete_student", student_id=self.student_1.id),
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
            'message': ANY
        })
        self.assertFalse(
            Session().query(Student).filter_by(id=self.student_1.id).one_or_none()
        )

    def test_update_another_student(self):
        resp = self.client.delete(
            url_for("api.delete_student", student_id=self.student_2.id),
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertTrue(
            Session().query(Student).filter_by(id=self.student_2.id).one_or_none()
        )


class TestListCourse(BaseTestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.lecturer_1_credentials = None

    def setUp(self):
        super().setUp()
        self.lecturer_1 = db_utils.create_entry(Lecturer, **self.lecturer_1_data_hashed)
        self.lecturer_2 = db_utils.create_entry(Lecturer, **self.lecturer_2_data_hashed)
        db_utils.create_entry(Course, **{
            **self.course_1_data, 'lecturer_id': self.lecturer_1.id
        })
        db_utils.create_entry(Course, **{
            **self.course_2_data, 'lecturer_id': self.lecturer_2.id
        })

    def test_list_course(self):
        resp = self.client.get(
            url_for("api.list_course"),
            headers=self.get_auth_headers(self.lecturer_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, [
            {
                'id': ANY,
                'name': self.course_1_data['name'],
                'amount': self.course_1_data['amount'],
                'owner_id': self.lecturer_1.id
            },
        ])

    def test_list_course_by_lecturer(self):
        resp = self.client.get(
            url_for("api.list_course"),
            headers=self.get_auth_headers(self.lecturer_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, [
            {
                'id': ANY,
                'name': self.course_1_data['name'],
                'amount': self.course_1_data['amount'],
                'owner_id': self.lecturer_1.id
            },
            {
                'id': ANY,
                'name': self.course_2_data['name'],
                'amount': self.course_2_data['amount'],
                'owner_id': self.lecturer_2.id
            },
        ])

    def test_unauthorized(self):
        resp = self.client.get(url_for("api.list_course"))

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })


class TestCreateCourse(BaseTestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.lecturer_1_credentials = None
        self.lecturer_1_data_hashed = None

    def setUp(self):
        super().setUp()
        self.lecturer_1 = db_utils.create_entry(Lecturer, **self.lecturer_1_data_hashed)

    def test_create_course(self):
        resp = self.client.post(
            url_for("api.create_course"),
            json={"name": self.course_1_data["name"]},
            headers=self.get_auth_headers(self.lecturer_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'id': ANY,
            'name': self.course_1_data['name'],
            'amount': 0,
            'owner_id': self.lecturer_1.id
        })

    def test_unauthorized(self):
        resp = self.client.post(
            url_for("api.create_course"),
            json={"name": self.course_1_data["name"]},
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })


class TestGetCourse(BaseTestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.lecturer_2_credentials = None
        self.lecturer_1_credentials = None
        self.lecturer_2_data_hashed = None
        self.lecturer_1_data_hashed = None

    def setUp(self):
        super().setUp()
        self.lecturer_1 = db_utils.create_entry(Lecturer, **self.lecturer_1_data_hashed)
        self.lecturer_2 = db_utils.create_entry(Lecturer, **self.lecturer_2_data_hashed)
        self.course = db_utils.create_entry(Course, **{
            **self.course_1_data, 'owner_id': self.lecturer_1.id
        })

    def test_get_course(self):
        resp = self.client.get(
            url_for("api.get_course_by_id", course_id=self.course.id),
            headers=self.get_auth_headers(self.lecturer_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'id': ANY,
            'name': self.course_1_data['name'],
            'amount': 0,
            'owner_id': self.lecturer_1.id
        })

    def test_get_course_by_wrong_lecturer(self):
        resp = self.client.get(
            url_for("api.get_course_by_id", course_id=self.course.id),
            headers=self.get_auth_headers(self.lecturer_2_credentials),
        )

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json, {
            'code': 404,
            'type': 'NOT_FOUND',
            'message': ANY
        })

    def test_unauthorized(self):
        resp = self.client.get(
            url_for("api.get_course_by_id", course_id=self.course.id)
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })


class TestUpdateCourse(BaseTestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.lecturer_2_credentials = None
        self.lecturer_1_credentials = None
        self.lecturer_1_data_hashed = None
        self.lecturer_2_data_hashed = None

    def setUp(self):
        super().setUp()
        self.lecturer_1 = db_utils.create_entry(Lecturer, **self.lecturer_1_data_hashed)
        self.lecturer_2 = db_utils.create_entry(Lecturer, **self.lecturer_2_data_hashed)
        self.course = db_utils.create_entry(Course, **{
            **self.course_1_data, 'owner_id': self.lecturer_1.id
        })

    def test_update_course(self):
        resp = self.client.put(
            url_for("api.update_course", course_id=self.course.id),
            json={"name": "Updated Course A"},
            headers=self.get_auth_headers(self.lecturer_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
            'message': ANY
        })
        self.assertTrue(
            Session().query(Course).filter_by(name="Updated Course A").one()
        )

    def test_update_course_by_wrong_lecturer(self):
        resp = self.client.put(
            url_for("api.update_course", course_id=self.course.id),
            json={"name": "Updated Course A"},
            headers=self.get_auth_headers(self.lecturer_2_credentials),
        )

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json, {
            'code': 404,
            'type': 'NOT_FOUND',
            'message': ANY
        })
        self.assertFalse(
            Session().query(Course).filter_by(name="Updated Course A").one_or_none()
        )

    def test_unauthorized(self):
        resp = self.client.put(
            url_for("api.update_course", course_id=self.course.id),
            json={"name": "Updated Course A"},
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertFalse(
            Session().query(Course).filter_by(name="Updated Course A").one_or_none()
        )


class TestDeleteCourse(BaseTestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.lecturer_2_credentials = None
        self.lecturer_1_credentials = None
        self.lecturer_2_data_hashed = None
        self.lecturer_1_data_hashed = None
        self.student_1 = None

    def setUp(self):
        super().setUp()
        self.lecturer_1 = db_utils.create_entry(Lecturer, **self.lecturer_1_data_hashed)
        self.lecturer_2 = db_utils.create_entry(Lecturer, **self.lecturer_2_data_hashed)
        self.course = db_utils.create_entry(Course, **{
            **self.course_1_data, 'owner_id': self.student_1.id
        })

    def test_delete_course(self):
        resp = self.client.delete(
            url_for("api.delete_course", course_id=self.course.id),
            headers=self.get_auth_headers(self.lecturer_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'code': 200,
            'type': 'OK',
            'message': ANY
        })
        self.assertFalse(
            Session().query(Course).filter_by(id=self.course.id).one_or_none()
        )

    def test_delete_course_by_wrong_lecturer(self):
        resp = self.client.delete(
            url_for("api.delete_course", course_id=self.course.id),
            headers=self.get_auth_headers(self.lecturer_2_credentials),
        )

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json, {
            'code': 404,
            'type': 'NOT_FOUND',
            'message': ANY
        })
        self.assertTrue(
            Session().query(Course).filter_by(id=self.course.id).one_or_none()
        )

    def test_unauthorized(self):
        resp = self.client.delete(
            url_for("api.delete_course", course_id=self.course.id),
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertTrue(
            Session().query(Course).filter_by(id=self.course.id).one_or_none()
        )


class TestSendApplication(BaseTestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.course_2 = None
        self.course_1 = None
        self.application_1_data = None
        self.lecturer_1_data_hashed = None

    def setUp(self):
        super().setUp()
        self.student_1 = db_utils.create_entry(Student, **self.student_1_data_hashed)
        self.lecturer_1 = db_utils.create_entry(Lecturer, **self.lecturer_1_data_hashed)
        self.application_1 = db_utils.create_entry(Application, **{
            **self.application_1_data, 'owner_id': self.student_1.id, 
        })


    def test_send_application(self):
        resp = self.client.post(
            url_for("api.send_application", application_id=self.application_1.id),
            json={"to_course": self.course_1.id},
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {
            'uid': ANY,
            'from_student': self.student_1.id,
            'to_course': self.course_1.id,
            'datetime': ANY
        })
        self.assertTrue(
            Session().query(Application).filter_by(id=resp.json['id']).one()
        )


    def test_send_application_with_wrong_student(self):
        resp = self.client.post(
            url_for("api.send_application", course_id=self.course_1.id),
            json={"to_course": self.course_2.id},
            headers=self.get_auth_headers(self.student_2_credentials),
        )

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json, {
            'code': 404,
            'type': 'NOT_FOUND',
            'message': ANY
        })
        self.assertEqual(
            Session().query(Application).filter_by(id=self.course_1.id).one().application,

        )

    def test_unauthorized(self):
        resp = self.client.post(
            url_for("api.send_application", course_id=self.course_1.id),
            json={"to_course": self.course_2.id},
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
        self.assertEqual(
            Session().query(Application).filter_by(id=self.course_1.id).one().application,

        )


class TestListCourseApplication(BaseTestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.student_2 = None
        self.lecturer_2 = None
        self.lecturer_1_data_hashed = None

    def setUp(self):
        super().setUp()

        self.student_1 = db_utils.create_entry(Student, **self.student_1_data_hashed)
        self.lecturer_1 = db_utils.create_entry(Lecturer, **self.lecturer_1_data_hashed)

        self.course_1 = db_utils.create_entry(Course, **{
            **self.course_1_data, 'owner_id': self.lecturer_1.id, "application": 1
        })
        self.course_2 = db_utils.create_entry(Course, **{
            **self.course_2_data, 'owner_id': self.lecturer_2.id
        })
        self.course_3 = db_utils.create_entry(Course, **{
            **self.course_3_data, 'owner_id': self.lecturer_1.id
        })

        self.course_1_application_1_data = {
            "from_student_id": self.student_1.id,
            "to_course_id": self.course_1.id,
            "amount": 1,
            "datetime": datetime.now(),
        }
        self.course_1_application_1 = db_utils.create_entry(
            Application, **self.course_1_application_1_data
        )

        self.course_1_application_2_data = {
            "from_student_id": self.student_2.id,
            "to_course_id": self.course_1.id,
            "amount": 1,
            "datetime": datetime.now(),
        }
        self.course_1_application_2 = db_utils.create_entry(
            Application, **self.course_1_application_2_data
        )

        self.course_2_application_1_data = {
            "from_student_id": self.student_1.id,
            "to_course_id": self.course_2.id,
            "amount": 1,
            "datetime": datetime.now(),
        }
        self.course_2_application_1 = db_utils.create_entry(
            Application, **self.course_2_application_1_data
        )

        self.course_2_application_2_data = {
            "from_student_id": self.student_2.id,
            "to_course_id": self.course_2.id,
            "amount": 1,
            "datetime": datetime.now(),
        }
        self.course_2_application_2 = db_utils.create_entry(
            Application, **self.course_2_application_2_data
        )

    def test_list_course_application(self):
        resp = self.client.get(
            url_for("api.list_course_application", course_id=self.course_1.id),
            headers=self.get_auth_headers(self.student_1_credentials),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, [
            {
                'id': ANY,
                "from_student": self.course_1_application_1_data["from_student_id"],
                "to_course": self.course_1_application_1_data["to_couse_id"],
                "amount": self.course_1_application_1_data["amount"],
                "datetime": self.course_1_application_1_data["datetime"].isoformat(),
            },
            {
                'id': ANY,
                "from_student": self.course_1_application_2_data["from_student_id"],
                "to_course": self.course_1_application_2_data["to_couse_id"],
                "amount": self.course_1_application_2_data["amount"],
                "datetime": self.course_1_application_2_data["datetime"].isoformat(),
            },
            {
                'id': ANY,
                "from_student": self.course_2_application_1_data["from_student_id"],
                "to_course": self.course_2_application_1_data["to_couse_id"],
                "amount": self.course_2_application_1_data["amount"],
                "datetime": self.course_2_application_1_data["datetime"].isoformat(),
            },
        ])

    def test_list_course_application_with_wrong_student(self):
        resp = self.client.get(
            url_for("api.list_course_application", course_id=self.course_1.id),
            headers=self.get_auth_headers(self.student_2_credentials),
        )

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json, {
            'code': 404,
            'type': 'NOT_FOUND',
            'message': ANY
        })

    def test_unauthorized(self):
        resp = self.client.get(
            url_for("api.list_course_application", course_id=self.course_1.id)
        )

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json, {
            'code': 401,
            'type': 'NOT_AUTHORIZED',
            'message': ANY
        })
