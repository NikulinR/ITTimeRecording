from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User
from rec.decorators import requires_login
from rec import forms

mod = Blueprint('HR', __name__, url_prefix='/hr')


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_login' in session:
        g.user = User.query.get(session['user_login'])


@mod.route('/ViewRequests', methods=['GET', 'POST'])
def ViewRequests():
    return render_template("")

@mod.route('/Register', methods=['GET', 'POST'])
def Register():
    return render_template("tools/HR/Register.html")

@mod.route('/Delete', methods=['GET', 'POST'])
def Delete():
    return render_template("tools/HR/Delete.html")

@mod.route('/Stats', methods=['GET', 'POST'])
def Stats():
    return render_template("tools/HR/Stats.html")


@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    session.clear()
    return redirect('/')
