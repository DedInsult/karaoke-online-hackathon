from flask import Flask, render_template, Blueprint, url_for, redirect, session, request
from flask_security import login_required

general = Blueprint('general', __name__)


@general.route('/')
def index():
    return render_template("mainpage.html")


@general.route('/speech')
@login_required
def speech():
    return render_template('speech.html')