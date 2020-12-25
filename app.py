from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from dbinit import db
db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import Lecturer, Student, Course, Application

@app.route('/')
def hello_world():
    return 'Hello World!'



app.run()
