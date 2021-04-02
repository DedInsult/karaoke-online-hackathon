import mongoengine
from flask import Flask, render_template, Blueprint, send_from_directory, abort, jsonify
from flask_security import login_required
from DataBase import *
from forms import *
from helper_function import spanify_text
from config import Config
import datetime
import stripe

stripe.api_key = "sk_test_51ICUYQBfTYBgs6VwHo83UJHU3bHRslQjyB8ghSSK0QNXQ0WSLx5IFBg79s2FGgUBGP16VDTWSGpeJoCoz7BQrS2L00GCcjuzWi"

default_timer = datetime.datetime(year=2018, month=7, day=12, hour=7, minute=9, second=33)

from karaoke_online_hakaton import avatars

general = Blueprint('general', __name__)

def ranking():
    ranker = 1
    users = User.objects().order_by('-points')
    for user in users:
        user.rank = ranker
        ranker += 1
        user.save()


def check_energy():
    user = User.objects(id=current_user.id)[0]

    energy = user.energy

    timedelta = datetime.datetime.now() - user.energy_date

    if energy < 10:
        if user.energy_date == default_timer:
            user.energy_date = datetime.datetime.now()
        elif timedelta.days >= 1 and user.energy_date != default_timer:
            user.energy = 10
            user.energy_date = default_timer
    user.save()


def daily_gift():
    user = User.objects(id=current_user.id)[0]

    if user.daily_gift_date == default_timer:
        user.daily_gift_date = datetime.datetime.now()
        user.points += 500

    timedelta = datetime.datetime.now() - user.daily_gift_date

    if timedelta.days >= 1 and user.daily_gift_date != default_timer:
        user.daily_gift_date = default_timer

    user.save()


@general.route('/')
def index():
    return render_template("mainpage.html", default_timer=default_timer)


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
        songs = Song.objects(name_contains=q)
    else:
        songs = Song.objects()

    pages = songs.paginate(page=page, per_page=10)

    user = User.objects(id=current_user.id)[0]

    energy = user.energy

    check_energy()

    daily_gift()

    return render_template("lobby.html", songs=songs, pages=pages, energy=energy, daily_gift_date=user.daily_gift_date,
                           default_timer=default_timer)


@general.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template('profile.html')


@general.route("/profile/SungSongs")
def SungSongs():
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
        style = Shop.objects(id=style_id)[0]
        if user.points >= style.cost and not style in user.bought_styles:
            user.points = user.points - style.cost
            user.bought_styles.append(style)
            user.save()
            return redirect(url_for("general.index"))

    return render_template("shop.html", pages=pages, form=form)


@general.route("/mystuff", methods=["GET", "POST"])
def mystuff():
    q = request.args.get("q")


    if q:
        things = Shop.objects(name__contains=q, )
    else:
        things = Shop.objects()




    return render_template("mystuff.html", things=things)


@general.route('/<song_id>')
@login_required
def speech(song_id):
    try:
        song = Song.objects(id=song_id)[0]

        text = spanify_text(song)

        user = User.objects(id=current_user.id)[0]

        user.energy -= 1
        energy = user.energy
        user.save()

        return render_template('speech.html', song=song, ly=text)

    except mongoengine.errors.ValidationError as e:
        print(e)
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


@general.route('/premium')
def premium():
    return render_template('premium.html')


@general.route('/stripe_pay/<product_id>')
def stripe_pay(product_id):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': product_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=url_for('general.thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('general.premium', _external=True, product_id=product_id),
    )
    return {'checkout_session_id': session['id'], 'checkout_public_key': Config.STRIPE_PUBLIC_KEY}


@general.route('/thanks')
def thanks():
    return render_template('thanks.html')

@general.route('/leaderboard')
def leaderboard():

    q = request.args.get("q")

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        users = User.objects(username__contains=q).order_by('-points')
    else:
        users = User.objects(points__gt=0).order_by('-points')


    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1


    pages = users.paginate(page=page, per_page=10)

    ranking()

    return render_template('LeaderBoard.html', pages=pages, users=users)
