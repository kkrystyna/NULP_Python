from .models import *
from marshmallow import Schema, fields, validate, ValidationError
from courses import ma, db


class UserSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    first_name = fields.Str(validate=validate.Length(min=3, max=64))
    last_name = fields.Str(validate=validate.Length(min=3, max=64))
    password = fields.Str(validate=validate.Length(min=3, max=64))
    phone_num = fields.Str(validate=validate.Length(min=3, max=32))
    birth_date = fields.Str(allow_none=True)
    email = fields.Str(validate=validate.Length(min=3, max=60))
    role = fields.Str(allow_none=True, default='UserRole.STUDENT')

    class Meta:
        model = User


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
