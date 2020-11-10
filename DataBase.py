from datetime import datetime
from flask_admin.contrib.mongoengine import ModelView
from flask_admin import AdminIndexView
from flask_security import MongoEngineUserDatastore, Security, UserMixin, RoleMixin, login_required, current_user
from flask import redirect, url_for, request
from karaoke_online_hakaton import db
from mongoengine import connect


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
    username = db.StringField(max_length=40)
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])

    sung_songs = db.EmbeddedDocumentListField(SungSong)



class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('general.index', next=request.url))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('general.index', next=request.url))



if __name__ == '__main__':
    connect('test')

    u = User.objects[0]
    print(u.sung_songs[0].get_author())


    # FOR DEBUG PURPOSES, DELETE LATER
    # ss = SungSong()
    # son = Song.objects[0]
    # ss.song = son
    # ss.score = 9
    # u = User.objects[0]
    # u.sung_songs.append(ss)
    # u.save()

    # For test, delete later
    # connect('test')
    # s = Song()
    # s.name = 'Батарейка2'
    # s.duration = 122
    # s.lyrics = '''
    #  Оо ия иё Батарейка
    #  Оо ия иё Батарейка'''
    # s.difficulty = 3
    # s.path = '1.mp3'
    # s.author = 'Жуки'
    # s.language = 'ru'
    # s.save()
