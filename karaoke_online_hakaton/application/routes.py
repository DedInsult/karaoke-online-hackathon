from flask import Flask, render_template, Blueprint, url_for, redirect, session, request
from flask_security import login_required
from karaoke_online_hakaton import user_datastore

general = Blueprint('general', __name__)


@general.route('/')
def index():
    return "what's up!"


@general.route('/speech')
@login_required
def speech():
    return render_template('speech.html')

@general.before_app_first_request()
def restrict_admin_url():
    endpoint = "admin.index"
    url = url_for(endpoint)
    admin_index = general.view_functions.pop(endpoint)