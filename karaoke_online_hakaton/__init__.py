import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security
from flask_admin import Admin
from flask_avatars import Avatars

import config

avatars = Avatars()
db = MongoEngine()
admin = Admin()

from DataBase import  *

user_datastore = MongoEngineUserDatastore(db, User, Role)

security = Security()



def create_app(debug=True):
    # app
    app = Flask(__name__, instance_relative_config=False)
    app.debug = debug
    app.config.from_object(config.Config)



    # flask avatars
    app.config['AVATARS_SAVE_PATH'] = 'karaoke_online_hakaton/static/avatars'

    avatars.init_app(app)

    # flask security
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['SECURITY_PASSWORD_SALT'] = 'salt'
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    security.init_app(app, user_datastore)


    # DB
    app.config['MONGODB_DB'] = 'karaoke_online'
    app.config['MONGODB_HOST'] = 'localhost'
    app.config['MONGODB_PORT'] = 27017
    db.init_app(app)


    # Admin
    admin.init_app(app)
    admin.add_view(AdminView(User, endpoint="user"))
    admin.add_view(AdminView(Role, endpoint="role"))
    admin.add_view((AdminView(Achievement, endpoint="Achievements")))
    admin.add_view(SongCustomAdminView(Song, endpoint="Song"))
    admin.add_view(AdminView(Shop, endpoint="shop"))



    from .application import routes
    app.register_blueprint(routes.general)

    return app

