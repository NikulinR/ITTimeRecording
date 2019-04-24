from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User, Workday
import time
from rec.decorators import requires_login
from rec import forms

mod = Blueprint('Developer', __name__, url_prefix='/dev')
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

    session['now'] = time.monotonic()
    session['time'] = session['now'] - session['start']

    global menu
    menu = []
    if g.user.role == 'Developer':
        menu.append(['Order overtime', 'TakeOvertime'])
        menu.append(['Replace worktime', 'ReplaceTime'])
        menu.append(['Statistics', 'Stats'])
    if g.user.role == 'Manager':
        menu.append(['Change user activity', 'ChangeUserActivity'])
        menu.append(['Workday managing', 'ManageWorkday'])
        menu.append(['Statistics', 'Stats'])
    if g.user.role == 'Top-Manager':
        menu.append(['View user data', 'ViewData'])
        menu.append(['Change working day standards', 'ChangeWorkday'])
        menu.append(['Change coefficients', 'ChangeCoeffs'])
    if g.user.role == 'HR':
        menu.append(['View new registration requests', 'ViewRequests'])
        menu.append(['Registration of new worker', 'Register'])
        menu.append(['Delete user', 'Delete'])
        menu.append(['Statistics', 'Stats'])


@mod.route('/TakeOvertime', methods=['GET', 'POST'])
def TakeOvertime():
    return render_template("tools/Developer/TakeOvertime.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])

@mod.route('/ReplaceTime', methods=['GET', 'POST'])
def ReplaceTime():

    return render_template("tools/Developer/ReplaceTime.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])

@mod.route('/Stats', methods=['GET', 'POST'])
def Stats():
    return render_template("tools/Developer/Stats.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])

@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    return url_for("rec.login.exit")
    #session.clear()
    #return redirect('/')
