from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User
from rec.decorators import requires_login
from rec import forms

mod = Blueprint('Developer', __name__, url_prefix='/dev')


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_login' in session:
        g.user = User.query.get(session['user_login'])


@mod.route('/TakeOvertime', methods=['GET', 'POST'])
def TakeOvertime():
    return render_template("tools/Developer/TakeOvertime.html")

@mod.route('/ReplaceTime', methods=['GET', 'POST'])
def ReplaceTime():
    return render_template("tools/Developer/ReplaceTime.html")

@mod.route('/Stats', methods=['GET', 'POST'])
def Stats():
    return render_template("tools/Developer/Stats.html")

@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    session.clear()
    return redirect('/')
