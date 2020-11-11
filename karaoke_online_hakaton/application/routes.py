import mongoengine
from flask import Flask, render_template, Blueprint, url_for, redirect, session, request, send_from_directory, abort
from flask_security import login_required, roles_required
from DataBase import *
from helper_function import spanify_text

general = Blueprint('general', __name__)


@general.route('/')
def index():
    return render_template("mainpage.html")


@general.route('/lobby')
@login_required
def lobby():
    q = request.args.get("q")

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        songs = Song.objects(name__contains=q)
    else:
        songs = Song.objects

    pages = songs.paginate(page=page, per_page=1)

    return render_template("lobby.html", songs=songs, pages=pages)


@general.route('/<song_id>')
@login_required
def speech(song_id):
    try:
        song = Song.objects(id=song_id)[0]

        text = spanify_text(song)

        return render_template('speech.html', song=song, ly=text)

    except mongoengine.errors.ValidationError:
        abort(404)
