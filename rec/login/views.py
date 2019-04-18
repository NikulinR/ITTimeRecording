from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from rec.login.models import User
from rec.login.decorators import requires_login
from rec.login import forms

mod = Blueprint('rec', __name__, url_prefix='/login')


@mod.route('/me/')
@requires_login
def home():
    return render_template("homepage.html", user=g.user)


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and (user.password == form.password.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            session['user_id'] = user.login
            flash('Welcome %s' % user.username)
            return redirect(url_for('app.home'))
        flash('Wrong email or password', 'error-message')
    return render_template("login/login.html", form=form)