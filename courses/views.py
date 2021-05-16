from courses import app, bcrypt
from flask import jsonify, request, abort, render_template, make_response, Blueprint
from .models import *
from .schemas import *


@app.route('/')
def home():
    return '<h1>Hello world</h1>'


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return 'User not found', 404
    return str(user.first_name), 200


@app.route("/users", methods=['POST'])
def create_user():
    email = request.form['email']
    if User.query.filter_by(email=email).first() is not None:
        return jsonify(message='User already exists'), 403

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    phone_num = request.form['phone_num']
    role = request.form['role_choice']

    user = User(first_name=first_name, last_name=last_name, phone_num=phone_num, birth_date=None, password=password,
                role=role, email=email)
    user_data = user_schema.dump(user)
    try:
        UserSchema().load(user_data)
        db.session.add(user)
        db.session.commit()
        # return "User was created", 201
        return user_schema.jsonify(user), 201
    except ValidationError as err:
        return jsonify(message=err.messages), 405


@app.route("/users", methods=['DELETE'])
def delete_user():
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user is None:
        return jsonify(message='Account does not exist'), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message='User was deleted'), 200


@app.route("/users/login", methods=['POST'])
def login():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify(message='Account does not exist'), 404
    password = request.form['password']

    if bcrypt.check_password_hash(user.password, password):
        user_data = user_schema.dump(user)
        try:
            UserSchema().load(user_data)
            db.session.add(user)
            db.session.commit()
            return user_schema.jsonify(user), 200
        except ValidationError as err:
            return jsonify(message=err.messages), 405
