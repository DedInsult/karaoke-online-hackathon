import mongoengine
from flask import Flask, render_template, Blueprint, url_for, redirect, session, request, send_from_directory, abort, jsonify
from flask_security import login_required, roles_required
from DataBase import *
from forms import *
from helper_function import spanify_text
from fuzzywuzzy import fuzz

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


@general.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template('profile.html')


@general.route("/profile/SungSongs")
def SungSongs():
    q = request.args.get("q")

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        songs = current_user.sung_songs(name__contains=q)
    else:
        songs = current_user.sung_songs

    pages = songs.paginate(page=page, per_page=2)
    return render_template('sungsongs.html', pages=pages)


@general.route('/<song_id>')
@login_required
def speech(song_id):
    try:
        song = Song.objects(id=song_id)[0]

        text = spanify_text(song)

        return render_template('speech.html', song=song, ly=text)

    except mongoengine.errors.ValidationError:
        abort(404)


@general.route('/submit_song', methods=('POST', 'GET'))
def submit_song():
    data = request.json

    user = User.objects(id=current_user.id)[0]
    song = Song.objects(id=data['song_id'])[0]

    sung = SungSong(song=song, score=data['percentage'])

    user.score += data['percentage'] * 1.5 ** song.difficulty

    user.sung_songs.append(sung)
    user.save()

    return jsonify('Your result has been saved!')


@general.route('/profile/edit', methods=('POST', 'GET'))
def editprofile():

    form = NewUserNameForm()
    if form.validate_on_submit():
        new_name = form.username.data
        user = User.objects(id__contains=current_user.id)
        user.update(set__username=str(new_name))
        return redirect(url_for("general.profile"))

    return render_template("editprofile.html", form=form)
