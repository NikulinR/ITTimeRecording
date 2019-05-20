from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User, Normative, Workday, Holyday, VacationsPermittion, fix_all_func
from rec.decorators import requires_login
from rec import forms
import time

mod = Blueprint('rec', __name__, url_prefix='/home')
date = datetime.date.today()

menu = []

@mod.route('/me/', methods=['POST', 'GET'])
@requires_login
def home():
    global menu
    menu = []
    if g.user.role == 'Developer':
        menu.append(['Order overtime', 'TakeOvertime'])
    if g.user.role == 'Manager':
        menu.append(['Change user activity', 'ChangeUserActivity'])
        menu.append(['Workday managing', 'ManageWorkday'])
        menu.append(['Registration of new worker', 'Register'])
        menu.append(['Delete user', 'Delete'])
        menu.append(['Calculate salaries', 'Calculate'])

    workdays = Workday.query.filter_by(date=date.toordinal())
    workdict = {}
    for workday in workdays:
        workdict[workday.user] = workday

    return render_template("homepage.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           curtime=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                           workdays=workdict)


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
        session['now'] = time.monotonic()
        quant = session['time']
        session['time'] = session['now'] - session['start']
        workday = Workday.query.filter_by(date=date.toordinal(), user=g.user.login).first()
        if (workday.ended == 1):
            session['time'] = 0
        #workday = Workday.query.filter_by(date=date.toordinal(), user=g.user.login).first()

        #fix_all_func(session['time'] - quant)


@mod.route('/sudo_exit', methods=['POST', 'GET'])
def sudo_exit():
    session.clear()
    return redirect('/')


@mod.route('/', methods=['GET', 'POST'])
def login():
    if 'user_login' in session:
        return redirect(url_for('rec.home'))
    form = forms.LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and (user.password == form.password.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            session['user_login'] = user.login
            session['date'] = datetime.date.today()
            session['normative'] = Normative
            g.date = datetime.date.today()
            #flash('Welcome, %s' % user.login)
            start = time.monotonic()
            now = time.monotonic()
            session['now'] = now
            session['start'] = start
            session['time'] = 0
            if Workday.query.filter_by(date=datetime.date.today().toordinal(), user=user.login).first():
                session["workday_id"] = Workday.query.filter_by(date=datetime.date.today().toordinal(), user=user.login).first().id
            else:
                newDay = user.start_day('Standart')
                session["workday_id"] = newDay.id
            return redirect(url_for('rec.home'))

        flash('Wrong email or password', 'error-message')
    return render_template("login/login.html", form=form)

@mod.route('/activity', methods=['POST', 'GET'])
@requires_login
def activity():
    g.user.choose_activity(request.form['activity'])
    return redirect('/')

@mod.route('/begin_day', methods=['GET', 'POST'])
@requires_login
def begin_day():
    session['start'] = time.monotonic()
    session['now'] = time.monotonic()
    g.user.start_day('Standart')
    return redirect('/')

@mod.route('/end_day', methods=['GET', 'POST'])
@requires_login
def end_day():
    g.user.end_day()
    return redirect('/')

@mod.route('/TakeOvertime', methods=['GET', 'POST'])
@requires_login
def TakeOvertime():
    tyear = int(request.form['year'])
    tmonth = int(request.form['month'])
    tdate = int(request.form['date'])
    target = datetime.date(tyear, tmonth, tdate)

    if request.form['action'] == 'overtime':
        if target.toordinal() > datetime.date.today().toordinal():
            vacation = Holyday.query.filter_by( user=g.user.login, date=target.toordinal()).first()
            if vacation:
                vacation.delete()
                g.user.order_overtime(target.toordinal(), 'Standart')
            else:
                g.user.order_overtime(target.toordinal(), 'Overtime')
    elif request.form['action'] == 'sick':
        g.user.take_sick(target.toordinal())
    return redirect('/')

@mod.route('/ReplaceWorkday', methods=['GET', 'POST'])
@requires_login
def ReplaceWorkday():
    tyear = int(request.form['year'])
    tmonth = int(request.form['month'])
    tdate = int(request.form['date'])
    target = datetime.date(tyear, tmonth, tdate)

    if request.form['action'] == 'replace':
        if target.toordinal() > datetime.date.today().toordinal():
            if Holyday.query.filter(Holyday.user == g.user.login,
                                        Holyday.date >= datetime.datetime(date.year,
                                                                          date.month,
                                                                          1).toordinal(),
                                        Holyday.date < datetime.datetime(date.year,
                                                                         date.month+1,
                                                                         1).toordinal()).count() < VacationsPermittion:

                vacation = Holyday(target.toordinal(), g.user.login)
                g.user.replace_worktime(target.toordinal())
            else:
                flash('You reserved too much vacations!')
    elif request.form['action'] == 'sick':
        g.user.take_sick(target.toordinal())

    return redirect('/')


@mod.route('/exit', methods=['POST', 'GET'])
@requires_login
def exit():
    g.user.end_day()
    session.clear()
    return redirect('/')
