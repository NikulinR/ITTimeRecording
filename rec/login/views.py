from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User
from rec.decorators import requires_login
from rec import forms

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
    return render_template("homepage.html", user=g.user, menu=menu, date=date, cal = cal)


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_login' in session:
        g.user = User.query.get(session['user_login'])


@mod.route('/', methods=['GET', 'POST'])
def login():
    if 'user_login' in session:
        return redirect('login/me')
    form = forms.LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and (user.password == form.password.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            session['user_login'] = user.login
            session['date'] = datetime.date.today()
            g.date = datetime.date.today()
            flash('Welcome, %s' % user.login)
            return redirect(url_for('rec.home'))
        flash('Wrong email or password', 'error-message')
    return render_template("login/login.html", form=form)


@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    session.clear()
    return redirect('/')
