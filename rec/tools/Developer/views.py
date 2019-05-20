from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User, Workday, Manager, Developer, Holyday,  fix_all_func
import time
from rec.decorators import requires_login
from rec import forms

mod = Blueprint('Developer', __name__, url_prefix='/dev')
date = datetime.date.today()
cal = ''
menu = []

@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_login' in session:
        g.user = User.query.get(session['user_login'])
        global cal
        day = Day(date, 1, 1, g.user.login)
        cal = Calendar.get_month(day, g.user.login)

    if g.user.role != "Developer":
        return redirect('/')

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
        menu.append(['Calculate salaries', 'Calculate'])

    session['now'] = time.monotonic()
    quant = session['time']
    session['time'] = session['now'] - session['start']
    workday = Workday.query.filter_by(date=date.toordinal(), user=g.user.login).first()

    if (workday.ended == 1):
        session['time'] = 0

    #fix_all_func(session['time'] - quant)
    #g.user.fix_time(session['time'] - quant)
@mod.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for("rec.home"))


@mod.route('/TakeOvertime', methods=['GET', 'POST'])
def TakeOvertime():
    if ('date' not in request.form):
        workdays = Workday.query.filter_by(date=datetime.date.today().toordinal())
        workdict = {}
        for workday in workdays:
            workdict[workday.user] = workday
        return render_template("tools/Developer/TakeOvertime.html",
                               user=g.user,
                               menu=menu,
                               date=datetime.date.today(),
                               cal=cal,
                               norms=session['normative'],
                               curtime=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                               workdays=workdict
                               )
    else:
        date = request.form['date']

        tyear = int(date[0:4])
        tmonth = int(date[5:7])
        tdate = int(date[8:10])

        target = datetime.date(tyear, tmonth, tdate)

        if target.toordinal() > datetime.date.today().toordinal():
            vacation = Holyday.query.filter_by(user=g.user.login, date=target.toordinal()).first()
            if vacation:
                vacation.delete()
                g.user.order_overtime(target.toordinal(), 'Standart')
            else:
                g.user.order_overtime(target.toordinal(), 'Overtime')
        return redirect('/')

@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    return url_for("rec.login.exit")
    #session.clear()
    #return redirect('/')
