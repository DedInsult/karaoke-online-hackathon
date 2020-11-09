from flask import Flask
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security

import config

db = MongoEngine()

from DataBase import  Role, User

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security()


def create_app(debug=True):
    app = Flask(__name__, instance_relative_config=False)
    app.debug = debug

    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['SECURITY_PASSWORD_SALT'] = 'salt'
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

    db.init_app(app)
    security.init_app(app, user_datastore)

    app.config.from_object(config.Config)

    from .application import routes
    app.register_blueprint(routes.general)

    return app
