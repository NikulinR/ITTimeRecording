from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User, Workday, Manager, Developer
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
        g.user = Developer.query.get(session['user_login'])
        menu.append(['Order overtime', 'TakeOvertime'])
    if g.user.role == 'Manager':
        g.user = Manager.query.get(session['user_login'])
        menu.append(['Change user activity', 'ChangeUserActivity'])
        menu.append(['Workday managing', 'ManageWorkday'])
        menu.append(['Registration of new worker', 'Register'])
        menu.append(['Delete user', 'Delete'])

    session['now'] = time.monotonic()
    session['time'] = session['now'] - session['start']

@mod.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for("rec.home"))

@mod.route('/ChangeUserActivity', methods=['GET', 'POST'])
def ChangeUserActivity():
    if ('userlogin' in request.form and 'activity' in request.form):
        g.user.choose_dev_activity(request.form['userlogin'],request.form['activity'])
    everyone = User.query.all()
    return render_template("tools/Manager/ChangeUserActivity.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                           workers = everyone)

@mod.route('/ManageWorkday', methods=['GET', 'POST'])
def ManageWorkday():
    everyone = User.query.all()
    return render_template("tools/Manager/ManageWorkday.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                           workers = everyone)


@mod.route('/Register', methods=['GET', 'POST'])
def Register():
    form = forms.RegisterForm(request.form)
    if form.validate_on_submit():
        if not User.query.filter_by(login=form.login.data).first():
            g.user.register_new_user(form.login.data, form.password.data, form.username.data, form.role.data)
            flash("User registered")
        flash("User already exists")

    return render_template("tools/Manager/Register.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'], form=form)

@mod.route('/Delete', methods=['GET', 'POST'])
def Delete():
    if ('userlogin' in request.form):
        g.user.delete_user(request.form['userlogin'])
    everyone = User.query.all()
    return render_template("tools/Manager/Delete.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'],
                           workers = everyone)


@mod.route('/begin_day', methods=['GET', 'POST'])
def begin_day():
    if ('userlogin' in request.form):
        g.user.start_dev_day(request.form['userlogin'], 'Standart')
    return ManageWorkday()

@mod.route('/end_day', methods=['GET', 'POST'])
def end_day():
    if ('userlogin' in request.form):
        g.user.end_dev_day(request.form['userlogin'])
    return ManageWorkday()


@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    return url_for("rec.login.exit")
