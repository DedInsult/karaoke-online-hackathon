from flask import Flask, render_template, Blueprint, url_for, redirect, session, request

general = Blueprint('general', __name__)


@general.route('/')
def index():
    return "what's up!"