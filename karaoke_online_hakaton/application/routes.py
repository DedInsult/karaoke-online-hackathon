import mongoengine
from flask import Flask, render_template, Blueprint, url_for, redirect, session, request, send_from_directory, abort, \
    jsonify
from flask_mongoengine import ListFieldPagination
from flask_security import login_required, roles_required
from DataBase import *
from forms import *
from helper_function import spanify_text
from fuzzywuzzy import fuzz

from karaoke_online_hakaton import avatars

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
        songs = Song.objects()

    pages = songs.paginate(page=page, per_page=1)

    return render_template("lobby.html", songs=songs, pages=pages)


@general.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template('profile.html')


@general.route("/profile/SungSongs")
def SungSongs():
    # q = request.args.get("q")

    # page = request.args.get('page')

    # if page and page.isdigit():
    # page = int(page)
    # else:
    # page = 1

    # if q:
    # songs = User.objects(sung_sungs_contains=q)
    # else:
    # user = current_user

    # print(user)

    # pages = ListFieldPagination(queryset=user, field_name=User.sung_songs, page=page, per_page=1, doc_id=idk)

    user = User.objects(id=current_user.id)[0]
    return render_template('sungsongs.html', songs=user.sung_songs)

@general.route("/shop", methods=["GET", "POST"])
def shop():
    q = request.args.get("q")

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        things = Shop.objects(name__contains=q)
    else:
        things = Shop.objects()

    pages = things.paginate(page=page, per_page=1)

    form = BuyStyleForm()
    if form.validate_on_submit():
        style_id = form.bthing.data
        user = User.objects(id=current_user.id)[0]
        style = Shop.objects(id=style_id).get()
        user.bought_styles.append(style)
        user.save()



    return render_template("shop.html", pages=pages, form=form)




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
    print(user.points)
    print(type(user.points))
    user.points += data['percentage'] * 1.5 ** song.difficulty

    user.sung_songs.append(sung)
    user.save()

    return jsonify('Your result has been saved!')


@general.route('/avatars/<path:filename>')
def get_avatar(filename):
    print('lmao')
    print(send_from_directory('karaoke_online_hakaton/static/avatars', filename))
    return send_from_directory('karaoke_online_hakaton/static/avatars', filename)

@general.route('/profile/edit', methods=('POST', 'GET'))
def editprofile():

    form = NewUserNameForm()
    if form.validate_on_submit():
        new_name = form.username.data
        user = User.objects(id__contains=current_user.id)
        user.update(set__username=str(new_name))
        return redirect(url_for("general.profile"))

    avatar_form = UploadAvatarForm()
    if request.method == 'POST':
        f = request.files.get('file')
        raw_filename = avatars.save_avatar(f)
        user = User.objects(id=current_user.id)[0]
        user.avatar_filename = raw_filename
        user.save()
        return redirect(url_for("general.profile"))

    return render_template("editprofile.html", form=form, avatar_form=avatar_form)

@general.route('/about')
def about_us():
    return render_template('about.html')