from flask import Flask, render_template, Blueprint, url_for, redirect, session, request
from flask_security import login_required
from DataBase import Song

general = Blueprint('general', __name__)


@general.route('/')
def index():
    return "what's up!"


@general.route('/speech')
@login_required
def speech(song_id):
    try:
        song = Song.objects(id=song_id)[0]
        print(song.name)
        return render_template('speech.html', song=song)

    except mongoengine.errors.ValidationError:
        abort(404)
