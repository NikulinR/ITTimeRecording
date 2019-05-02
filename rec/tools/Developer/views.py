from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User, Workday, Manager, Developer
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

    if g.user.role != "Developer":
        return redirect('/')

    session['now'] = time.monotonic()
    session['time'] = session['now'] - session['start']

    global menu
    menu = []
    if g.user.role == 'Developer':
        g.user = Developer.query.get(session['user_login'])
        menu.append(['Order overtime', 'TakeOvertime'])
    if g.user.role == 'Manager':
        g.user = Manager.query.get(session['user_login'])
        menu.append(['Change user activity', 'ChangeUserActivity'])
        menu.append(['Workday managing', 'ManageWorkday'])
        menu.append(['Registration of new worker', 'Register'])
        menu.append(['Delete user', 'Delete'])


@mod.route('/TakeOvertime', methods=['GET', 'POST'])
def TakeOvertime():
    form = forms.OvertimeForm(request.form)
    return render_template("tools/Developer/TakeOvertime.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'], form=form)

@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    return url_for("rec.login.exit")
    #session.clear()
    #return redirect('/')
