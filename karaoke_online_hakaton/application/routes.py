from flask import Flask, render_template, Blueprint, url_for, redirect, session, request, send_from_directory
from flask_security import login_required
from DataBase import Song

general = Blueprint('general', __name__)


@general.route('/')
def index():
    return "what's up!"


@general.route('/speech')
@login_required
def speech():
    songs = Song.objects

    return render_template('speech.html', songs=songs)