from datetime import datetime

from flask_security import MongoEngineUserDatastore, Security, UserMixin, RoleMixin, login_required
from karaoke_online_hakaton import db

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    def __str__(self):
        return self.name


class Song(db.Document):
    name = db.StringField(max_length=255, required=True)
    duration = db.IntField(required=True)
    lyrics = db.StringField(required=True)
    difficulty = db.IntField(required=True)
    path = db.StringField()
    author = db.StringField()
    language = db.StringField(choices=(('eng', 'en-US'), ('ru', 'ru-RU')), required=True)


class SungSong(db.EmbeddedDocument):
    song = db.ReferenceField(Song)
    score = db.IntField(required=True)
    date = db.DateTimeField(default=datetime.utcnow())

    def get_author(self):
        return self._instance


class User(db.Document, UserMixin):
    #username = db.StringField(max_length=40)
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])