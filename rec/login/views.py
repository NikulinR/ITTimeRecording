from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User, Normative, Workday
from rec.decorators import requires_login
from rec import forms
import time

mod = Blueprint('rec', __name__, url_prefix='/login')

@mod.route('/me/')
@requires_login
def home():
    date = datetime.date.today()
    day = Day(date, 1, 1)
    cal = Calendar.get_month(day)
    menu = []
    if g.user.role == 'Developer':
        menu.append(['Order overtime', 'TakeOvertime'])
    if g.user.role == 'Manager':
        menu.append(['Change user activity', 'ChangeUserActivity'])
        menu.append(['Workday managing', 'ManageWorkday'])
        menu.append(['View new registration requests', 'ViewRequests'])
        menu.append(['Registration of new worker', 'Register'])
        menu.append(['Delete user', 'Delete'])

    return render_template("homepage.html",
                           user=g.user,
                           menu=menu,
                           date=date,
                           cal=cal,
                           norms=session['normative'],
                           time=Workday.query.filter_by(id=session["workday_id"]).first().time + session['time'])


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    if 'start' in session:
        session['now'] = time.monotonic()
        session['time'] = session['now'] - session['start']

    g.user = None
    if 'user_login' in session:
        g.user = User.query.get(session['user_login'])


@mod.route('/sudo_exit', methods=['POST', 'GET'])
def sudo_exit():
    session.clear()
    return redirect('/')


@mod.route('/', methods=['GET', 'POST'])
def login():
    if 'user_login' in session:
        return redirect('login/me')
    form = forms.LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        normative = Normative.query.first()
        if user and (user.password == form.password.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            session['user_login'] = user.login
            session['date'] = datetime.date.today()
            session['normative'] = normative.workday
            g.date = datetime.date.today()
            flash('Welcome, %s' % user.login)
            start = time.monotonic()
            now = time.monotonic()
            session['now'] = now
            session['start'] = start
            if Workday.query.filter_by(date=datetime.date.today().toordinal(), user=user.login).first():
                session["workday_id"] = Workday.query.filter_by(date=datetime.date.today().toordinal(), user=user.login).first().id
            else:
                newDay = Workday(user.login, datetime.date.today().toordinal(), "Standart")
                session["workday_id"] = newDay.id
            return redirect(url_for('rec.home'))

        flash('Wrong email or password', 'error-message')
    return render_template("login/login.html", form=form)


@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    day = Workday.query.filter_by(id=session["workday_id"]).first()
    g.user.EndDay(g.user.worktime + session['time'])
    day.end(session['time'])
    session.clear()
    return redirect('/')
