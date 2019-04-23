from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import datetime
from rec.mycalendar import Calendar, Day
from rec.models import User
from rec.decorators import requires_login
from rec import forms

mod = Blueprint('Top-Manager', __name__, url_prefix='/top')


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_login' in session:
        g.user = User.query.get(session['user_login'])


@mod.route('/ViewData', methods=['GET', 'POST'])
def ViewData():
    return render_template("tools/Top-Manager/ViewData.html")

@mod.route('/ChangeWorkday', methods=['GET', 'POST'])
def ChangeWorkday():
    return render_template("tools/Top-Manager/ChangeWorkday.html")

@mod.route('/ChangeCoeffs', methods=['GET', 'POST'])
def ChangeCoeffs():
    return render_template("tools/Top-Manager/ChangeCoeffs.html")

@mod.route('/exit', methods=['POST', 'GET'])
def exit():
    session.clear()
    return redirect('/')
