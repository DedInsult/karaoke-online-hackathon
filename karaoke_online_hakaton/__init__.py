from flask import Flask
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView

import config

db = MongoEngine()

admin = Admin()

from DataBase import  Role, User, AdminView, HomeAdminView

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security()


def create_app(debug=False):
    # creating app
    app = Flask(__name__, instance_relative_config=False)
    app.debug = debug

    # flask security
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['SECURITY_PASSWORD_SALT'] = 'salt'
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

    # mongoDb
    app.config['MONGODB_DB'] = 'karaoke_online'
    app.config['MONGODB_HOST'] = 'localhost'
    app.config['MONGODB_PORT'] = 27017
    db.init_app(app)

    # admin
    admin.init_app(app)
    admin.add_view(AdminView(User, endpoint="user"))
    admin.add_view(AdminView(Role, endpoint="role"))


    security.init_app(app, user_datastore)

    app.config.from_object(config.Config)

    from .application import routes
    app.register_blueprint(routes.general)


    return app
