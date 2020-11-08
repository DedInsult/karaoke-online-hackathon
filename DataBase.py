from flask_security import MongoEngineUserDatastore, Security, UserMixin, RoleMixin, login_required
from karaoke_online_hakaton import db

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    #username = db.StringField(max_length=40)
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])