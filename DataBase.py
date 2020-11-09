from flask_security import MongoEngineUserDatastore, Security, UserMixin, RoleMixin, login_required
from karaoke_online_hakaton import db
from mongoengine import connect

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    #username = db.StringField(max_length=40)
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])


class Song(db.Document):
    name = db.StringField(max_length=255, required=True)
    duration = db.IntField(required=True)
    lyrics = db.StringField(required=True)
    difficulty = db.IntField(required=True)
    path = db.StringField()
    author = db.StringField()
    language = db.StringField(choices=(('eng', 'en-US'), ('ru', 'ru-RU')), required=True)
    
    
if __name__ == '__main__':
    connect('test')
    s = Song()
    s.name='Батарейка2'
    s.duration=122
    s.lyrics='''Холодный ветер с дождём
     Усилился стократно
     Всё говорит об одном
     Что нет пути обратно
     Что ты не мой Лопушок
     А я не твой Андрейка
     Что у любви у нашей
     Села батарейка.
     
     Припев:
     
     Оо ия иё Батарейка
     Оо ия иё Батарейка
     
     
     II куплет:
     
     Я тосковал по тебе
     В минуты расставанья
     Ты возвращалась ко мне
     Сквозь сны и расстоянья
     Но несмотря ни на что,
     Пришла судьба злодейка
     И у любви у нашей
     Села батарейка.
     
     Припев:
     
     Оо ия иё Батарейка
     Оо ия иё Батарейка
     
     
     III куплет:
     
     И вроде всё как всегда
     Всё те же чашки ложки
     Всё та же в кране вода
     Всё тот же стул без ножки
     И всё о том же с утра
     Щебечет канарейка
     Лишь у любви у нашей
     Села Батарейка.
     
     Припев:
     
     Оо ия иё Батарейка
     Оо ия иё Батарейка
     Оо ия иё Батарейка
     Оо ия иё Батарейка
     
     Оо ия иё Батарейка
     Оо ия иё Батарейка
     Оо ия иё Батарейка
     Оо ия иё Батарейка'''

    s.difficulty = 3
    s.path = '1.mp3'
    s.author = 'Жуки'
    s.language = 'ru'
    s.save()