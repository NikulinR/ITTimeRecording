import sqlite3
from flask import Flask, g, redirect, render_template, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'timerec.db')
print(os.path.join(basedir, 'timerec.db'))
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def main():
    g.user = None
    return redirect('/login/')





import rec.login
import rec.tools.Developer as dev
import rec.tools.HR as hr
import rec.tools.Manager as man
import rec.tools.TopManager as tman
app.register_blueprint(login.views.mod)
app.register_blueprint(dev.views.mod)
app.register_blueprint(hr.views.mod)
app.register_blueprint(man.views.mod)
app.register_blueprint(tman.views.mod)
