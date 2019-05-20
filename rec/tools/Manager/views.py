from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User, Workday, Manager, Developer, fix_all_func, calculate
import time
from rec.decorators import requires_login
from rec import forms

mod = Blueprint('Manager', __name__, url_prefix='/manager')
date = datetime.date.today()

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

    if g.user.role != "Manager":
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
    if(workday.ended == 1):
       session['time'] = 0
    #else:

    #fix_all_func(session['time'] - quant)
    #g.user.fix_time(session['time'] - quant)

@mod.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for("rec.home"))

@mod.route('/ChangeUserActivity', methods=['GET', 'POST'])
def ChangeUserActivity():
    if ('userlogin' in request.form and 'activity' in request.form):
        g.user.choose_dev_activity(request.form['userlogin'],request.form['activity'])
    everyone = User.query.all()
    workdays = Workday.query.filter_by(date=date.toordinal())
    workdict = {}
    for workday in workdays:
        workdict[workday.user] = workday

    return render_template("tools/Manager/ChangeUserActivity.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           curtime=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                           workers=everyone,
                           workdays=workdict)

@mod.route('/ManageWorkday', methods=['GET', 'POST'])
def ManageWorkday():
    everyone = User.query.all()
    workdays = Workday.query.filter_by(date=date.toordinal())
    workdict = {}
    for workday in workdays:
        workdict[workday.user] = workday
    return render_template("tools/Manager/ManageWorkday.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           curtime=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                           workers = everyone,
                           workdays=workdict)


@mod.route('/Register', methods=['GET', 'POST'])
def Register():
    workdays = Workday.query.filter_by(date=date.toordinal())
    workdict = {}
    for workday in workdays:
        workdict[workday.user] = workday
    form = forms.RegisterForm(request.form)
    if form.validate_on_submit():
        if not User.query.filter_by(login=form.login.data).first():
            g.user.register_new_user(form.login.data, form.password.data, form.username.data, form.role.data)
            flash("User registered")
        else:
            flash("User alredy exist!")


    return render_template("tools/Manager/Register.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           curtime=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                           form=form,
                           workdays=workdict)

@mod.route('/Delete', methods=['GET', 'POST'])
def Delete():
    if ('userlogin' in request.form):
        g.user.delete_user(request.form['userlogin'])
    everyone = User.query.all()
    workdays = Workday.query.filter_by(date=date.toordinal())
    workdict = {}
    for workday in workdays:
        workdict[workday.user] = workday
    return render_template("tools/Manager/Delete.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           curtime=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                           workers = everyone,
                           workdays=workdict)


@mod.route('/begin_day', methods=['GET', 'POST'])
def begin_day():
    if ('userlogin' in request.form):
        session['start'] = time.monotonic()
        session['now'] = time.monotonic()
        g.user.start_dev_day(request.form['userlogin'], 'Standart')
    return ManageWorkday()

@mod.route('/end_day', methods=['GET', 'POST'])
def end_day():
    if ('userlogin' in request.form):
        g.user.end_dev_day(request.form['userlogin'])
    return ManageWorkday()

@mod.route('/Calculate', methods=['GET', 'POST'])
def Calculate():
    calculate()
    return redirect(url_for("rec.home"))


@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    return url_for("rec.login.exit")
