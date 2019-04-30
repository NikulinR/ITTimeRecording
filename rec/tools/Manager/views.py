from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User, Workday
import time
from rec.decorators import requires_login
from rec import forms

mod = Blueprint('Manager', __name__, url_prefix='/manager')
date = datetime.date.today()
day = Day(date, 1, 1)
cal = Calendar.get_month(day)
menu = []

@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_login' in session:
        g.user = User.query.get(session['user_login'])

    global menu
    menu = []

    if g.user.role == 'Developer':
        menu.append(['Order overtime', 'TakeOvertime'])
    if g.user.role == 'Manager':
        menu.append(['Change user activity', 'ChangeUserActivity'])
        menu.append(['Workday managing', 'ManageWorkday'])
        menu.append(['View new registration requests', 'ViewRequests'])
        menu.append(['Registration of new worker', 'Register'])
        menu.append(['Delete user', 'Delete'])

    session['now'] = time.monotonic()
    session['time'] = session['now'] - session['start']

@mod.route('/ChangeUserActivity', methods=['GET', 'POST'])
def ChangeUserActivity():
    return render_template("tools/Manager/ChangeUserActivity.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])

@mod.route('/ManageWorkday', methods=['GET', 'POST'])
def ManageWorkday():
    return render_template("tools/Manager/ManageWorkday.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])

@mod.route('/ViewRequests', methods=['GET', 'POST'])
def ViewRequests():
    return render_template("tools/Manager/ViewRequests.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])

@mod.route('/Register', methods=['GET', 'POST'])
def Register():
    return render_template("tools/Manager/Register.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])

@mod.route('/Delete', methods=['GET', 'POST'])
def Delete():
    return render_template("tools/Manager/Delete.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])
@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    return url_for("rec.login.exit")
