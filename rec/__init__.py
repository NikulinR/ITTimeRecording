# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, g, redirect, render_template, session, url_for, request
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os
import threading

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
if os.path.exists(os.path.join(basedir, 'timerec.db')):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'timerec.db')
else:
    file = open(os.path.join(basedir, 'timerec.db'), 'w')
    file.close()
    conn = sqlite3.connect(os.path.join(basedir, 'timerec.db'))
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""CREATE TABLE `ACTIVITY` (
                        `NAME`	TEXT NOT NULL,
                        `COEFF`	REAL NOT NULL,
                        PRIMARY KEY(`NAME`)
                    );""")
    cursor.execute("""CREATE TABLE `BANK_HOLYDAYS` (
                        `DATE`	INTEGER,
                        `USER`	TEXT,
                        `DESCRIPTION`	TEXT,
                        PRIMARY KEY(`DATE`,`USER`)
                    );""")
    cursor.execute("""CREATE TABLE `USER` (
                        `LOGIN`	TEXT NOT NULL UNIQUE,
                        `PASSWORD`	TEXT NOT NULL,
                        `ROLE_NAME`	TEXT NOT NULL,
                        `USERNAME`	TEXT NOT NULL,
                        `SALARY`	INTEGER NOT NULL DEFAULT 0,
                        `WORKTIME`	INTEGER NOT NULL DEFAULT 0,
                        PRIMARY KEY(`LOGIN`)
                    );""")
    cursor.execute("""CREATE TABLE `WORKDAY` (
                        `ID`	INTEGER UNIQUE,
                        `TIME`	INTEGER,
                        `DATE`	INTEGER NOT NULL,
                        `ACTIVITY_NAME`	TEXT,
                        `USER_LOGIN`	TEXT,
                        `ENDED`	INTEGER DEFAULT 0,
                        `CALCULATED`	INTEGER DEFAULT 0,
                        PRIMARY KEY(`ID`),
                        FOREIGN KEY(`ACTIVITY_NAME`) REFERENCES `ACTIVITY`(`NAME`) ON UPDATE CASCADE
                    );""")
    cursor.execute("""INSERT INTO `USER` VALUES ('Manager','123','Manager','Manager', 0, 0);""")
    cursor.execute("""INSERT INTO `USER` VALUES ('Pasha','123','Manager','Pavel', 0, 0);""")
    cursor.execute("""INSERT INTO `USER` VALUES ('Petr','123','Developer','Petro', 0, 0);""")
    cursor.execute("""INSERT INTO `ACTIVITY` VALUES ('Sick', 0.8);""")
    cursor.execute("""INSERT INTO `ACTIVITY` VALUES ('Assignment', 1.5);""")
    cursor.execute("""INSERT INTO `ACTIVITY` VALUES ('Standard', 1.0);""")
    cursor.execute("""INSERT INTO `ACTIVITY` VALUES ('Vacation', 0.9);""")
    cursor.execute("""INSERT INTO `ACTIVITY` VALUES ('Overtime', 1.3);""")
    conn.commit()
db = SQLAlchemy(app)

print(os.path.join(basedir, 'timerec.db'))


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
        mod.fix_all_func(quant/1)
        time.sleep(quant)

timer = threading.Thread(target=commit, args=(quant,))
timer.setDaemon(True)
timer.start()

