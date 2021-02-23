from functools import wraps

import jwt as jwt
from flask import request, jsonify
from Models.ModelLecturer import Lecturer
from Controller.ApplicationController import ApplicationController
from Controller.CourseController import CourseController
from Controller.StudentController import StudentController
from Controller.LecturerController import LecturerController
from app import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':  'Token is missing!!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Lecturer.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': token + ' Token is invalid!!!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated

@app.route("/start")
def hello():
    return "Hello world !"

# link to try: http://127.0.0.1:5000/LecturerCreate?email=khrystyna@gmail.com&password=11111&first_name=Khrystyna&last_name=Oh&birthday=2002-09-26&department=ais


@app.route('/LecturerCreate', methods=['GET'])
def hello_lecturer():
    lecturer_data = request.args
    lecturer_controller = LecturerController()
    if lecturer_controller.create(lecturer_data):
        return "Success!"
    else:
        return "Create failed!"

# link to try: http://127.0.0.1:5000/StudentCreate?email=khrystyna@gmail.com&password=11111&first_name=Khrystyna&last_name=Oh&birthday=2002-09-26&collective=aa


@app.route('/StudentCreate', methods=['GET'])
def hello_student():
    student_data = request.args
    student_controller = StudentController()
    if student_controller.create(student_data):
        return "Success!"
    else:
        return "Create failed!"

# link to try: http://127.0.0.1:5000/CourseCreate?name=ap&amount_of_student=3


@app.route('/CourseCreate', methods=['GET'])
def hello_course():
    course_data = request.args
    course_controller = CourseController()
    if course_controller.create(course_data):
        return "Success!"
    else:
        return "Create failed!"

# link to try: http://127.0.0.1:5000/ApplicationCreate?application_id=1


@app.route('/ApplicationCreate/<int:student_id>/<int:course_id>', methods=['GET'])
def hello_application(student_id, course_id):
    application_data = request.args
    application_controller = ApplicationController()
    return application_controller.create(application_data, student_id, course_id)

# link to try: http://127.0.0.1:5000/CarRead?id=1


@app.route('/CourseRead', methods=['GET'])
def read_course():
    course_id = request.args.get('id')
    course_controller = CourseController()
    read_course = course_controller.read(course_id)
    #return "Name : " + str(read_course.name) + "   Amount of students : " + str(read_course.amount)
    return course_controller.read(course_id)

# link to try: http://127.0.0.1:5000/LecturerRead?id=1


@app.route('/LecturerRead', methods=['GET'])
def read_lecturer():
    lecturer_id = request.args.get('id')
    lecturer_controller = LecturerController()
    read_lecturer = lecturer_controller.read(lecturer_id)
    return lecturer_controller.read(lecturer_id)


# link to try: http://127.0.0.1:5000/StudentRead?id=1


@app.route('/StudentRead', methods=['GET'])
def read_user():
    student_id = request.args.get('id')
    student_controller = StudentController()
    read_student = student_controller.read(student_id)
    return student_controller.read(student_id)

# link to try: http://127.0.0.1:5000/CourseRead


@app.route('/CourseRead', methods=['GET'])
def read_course():
    course_controller = CourseController()
    read_course = course_controller.read_all()
    output = ""
    for i in range(len(read_course)):
        output += "Name : " + str(read_course[i].name) + "   Amount of students : " + str(read_course[i].amount) + "\n"
    return output

# link to try: http://127.0.0.1:5000/NotBookedRead


@app.route('/NotAppliedRead', methods=['GET'])
def not_applied_read():
    application_controller = ApplicationController()
    read_application = application_controller.read()
    course_controller = CourseController()
    read_course = course_controller.read_all()
    output = ""
    for i in range(len(read_course)):
        k = 1
        for j in range(len(read_application)):
            a = read_application[j].course_id
            b = read_course[i].id
            if a == b:
                k = 0
        if k == 1:
            output += "Name : " + str(read_course[i].name) + "   Amount of students : " + str(read_course[i].amount) + "\n"
    return output

# link to try: http://127.0.0.1:5000/CourseUpdate?id=2&lecturer_id=8&new_amount=5


@app.route('/CourseUpdate', methods=['PUT'])
def update_course():
    course_id = request.args.get('id')
    course_data = request.args
    course_controller = CourseController()
    return course_controller.update_course(course_id, course_data)

# link to try: http://127.0.0.1:5000/CarDelete?id=1&lecturer_id=10&user_id=10


@app.route('/CourseDelete', methods=['DELETE'])
def delete_course():
    course_id = request.args.get('id')
    lecturer_id = request.args.get('lecturer_id')
    course_controller = CourseController()
    return course_controller.delete(course_id, course_id)


# link to try: http://127.0.0.1:5000/LecturerDelete?id=1


@app.route('/LecturerDelete', methods=['DELETE'])
def delete_lecturer():
    lecturer_id = request.args.get('id')
    lecturer_controller = LecturerController()
    return lecturer_controller.delete(lecturer_id)

# link to try: http://127.0.0.1:5000/StudentDelete?id=1


@app.route('/StudentDelete', methods=['DELETE'])
def delete_student():
    student_id = request.args.get('id')
    student_controller = StudentController()
    return student_controller.delete(student_id)