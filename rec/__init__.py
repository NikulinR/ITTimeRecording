# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, g, redirect, render_template, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
import threading

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
    return redirect('/home/')

import rec.login
import rec.tools.Developer as dev
import rec.tools.Manager as man
app.register_blueprint(login.views.mod)
app.register_blueprint(dev.views.mod)
app.register_blueprint(man.views.mod)

#куда это засунуть не знаю пока
import rec.models as mod
import time
quant = 1
def commit(quant):
    while(True):
        mod.fix_all_func(quant)
        time.sleep(quant)

timer = threading.Thread(target=commit, args=(quant,))
timer.setDaemon(True)
timer.start()

