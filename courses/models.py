import enum

from courses import db, bcrypt


class UserRole(enum.Enum):
    STUDENT = 'student'
    LECTURER = 'lecturer'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone_num = db.Column(db.String(64), nullable=True)
    birth_date = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default='UserRole.STUDENT')

    def __init__(self, first_name, last_name, password, email, role, phone_num=None, birth_date=None):
        self.first_name = first_name
        self.last_name = last_name
        self.password = bcrypt.generate_password_hash(password)
        self.phone_num = phone_num
        self.email = email
        self.birth_date = birth_date
        self.role = role

    def __repr__(self):
        return '<User %s>' % self.first_name
