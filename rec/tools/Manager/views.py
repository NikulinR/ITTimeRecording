from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User
from rec.decorators import requires_login
from rec import forms

mod = Blueprint('Manager', __name__, url_prefix='/manager')

@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_login' in session:
        g.user = User.query.get(session['user_login'])


@mod.route('/ChangeUserActivity', methods=['GET', 'POST'])
def ChangeUserActivity():
    return render_template("tools/Manager/ChangeUserActivity.html")

@mod.route('/ManageWorkday', methods=['GET', 'POST'])
def ManageWorkday():
    return render_template("tools/Manager/ManageWorkday.html")

@mod.route('/Stats', methods=['GET', 'POST'])
def Stats():
    return render_template("tools/Manager/Stats.html")


@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    session.clear()
    return redirect('/')
