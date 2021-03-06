from rec import db
import sqlalchemy
import datetime
import threading
import time

Normative = 40
RubsPerHour = 250
VacationsPermittion = 5
#Quant = 5

#db.create_all()

class Activity(db.Model):
    __tablename__ = 'ACTIVITY'
    name = db.Column('NAME',db.String(15), primary_key=True)
    coeff = db.Column('COEFF', db.REAL, nullable=False)

    def __init__(self, name, coeff):
        self.name = name
        self.coeff = coeff

    def __repr__(self):
        return '<Coeff of %r is %r>' % (self.name, self.coeff)


class Holyday(db.Model):
    __tablename__='BANK_HOLYDAYS'
    date = db.Column('DATE', db.INTEGER, primary_key=True)
    user = db.Column('USER', db.String(20), primary_key=True)
    desc = db.Column('DESCRIPTION', db.String(40))

    def __init__(self, date, user = "ALL"):
        if not Holyday.query.filter_by(date=date, user=user).first():
            self.user = user
            self.date = date
            db.session.add(self)
            print('Holyday '+str(date)+' for '+user+' is setted')
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        print('Holyday '+str(self.date)+' for '+self.user+' is deleted')
        db.session.commit()

class Workday(db.Model):
    __tablename__='WORKDAY'
    id = db.Column('ID', db.INTEGER, primary_key=True, autoincrement= True)
    time = db.Column('TIME', db.INTEGER)
    date = db.Column('DATE', db.INTEGER)
    activity = db.Column('ACTIVITY_NAME', db.String(15), db.ForeignKey('ACTIVITY.NAME'), nullable=False)
    user = db.Column('USER_LOGIN', db.String(20), db.ForeignKey('USER.LOGIN'), nullable=False)
    ended = db.Column('ENDED', db.INTEGER)
    calculated = db.Column('CALCULATED', db.INTEGER)

    def __init__(self, user, date, activity):
        if not Workday.query.filter_by(date=date, user=user).first():
            self.user = user
            self.date = date
            self.time = 0
            self.activity = activity
            self.ended = 0
            self.calculated = 0
            db.session.add(self)
            db.session.commit()
            print('Workday '+str(self.date)+' for '+self.user+' is added')

    def stop(self):
        self.ended = 1
        db.session.commit()
        print('Workday ' + str(self.date) + ' for ' + self.user + ' is fixed. Time: ' + str(self.time))

    def start(self):
        if self.activity != 'Sick':
            self.ended = 0
            db.session.commit()
            print('Workday ' + str(self.date) + ' for ' + self.user + '. Time: ' + str(self.time))

class User(db.Model):
    __tablename__ = 'USER'
    login = db.Column('LOGIN', db.String(20), primary_key=True)
    password = db.Column('PASSWORD', db.String(20), nullable=False)
    salary = db.Column('SALARY', db.INTEGER)
    worktime = db.Column('WORKTIME', db.INTEGER)
    username = db.Column('USERNAME', db.String(50), nullable=False)
    role = db.Column('ROLE_NAME', db.String(15), nullable=False )

    def __init__(self, login, password, username, role):
        if not User.query.filter_by(login=login).first():
            self.login = login
            self.password = password
            self.username = username
            self.role = role
            self.worktime = 0
            self.salary = 0
            db.session.add(self)
            db.session.commit()

    def start_day(self, activity):
        if not Workday.query.filter_by(user=self.login, date=datetime.date.today().toordinal()).first():
            if Activity.query.filter_by(name=activity).first():
                newDay = Workday(self.login, datetime.date.today().toordinal(), activity)
            else:
                newDay = Workday(self.login, datetime.date.today().toordinal(), "Standart")
            db.session.add(newDay)
            db.session.commit()
            return newDay
        else:
            Workday.query.filter_by(user=self.login, date=datetime.date.today().toordinal()).first().start()

    def end_day(self):
        workday = Workday.query.filter_by(user=self.login, date=datetime.date.today().toordinal()).first()
        if workday:
            workday.stop()
            #print('Workday ' + workday.date + ' for ' + workday.user + ' is ' + str(workday.ended) + '. Time: ' + str(workday.time))

    def fix_time(self, ctime):
        unfixed = Workday.query.filter(Workday.user == self.login, Workday.date < datetime.date.today().toordinal(), Workday.ended == 0)
        workday = Workday.query.filter_by(user=self.login, date=datetime.date.today().toordinal()).first()
        if workday and workday.ended == 0:
            workday.time += ctime
            self.worktime += ctime
            db.session.commit()
            print('Workday ' + str(workday.date) + ' for ' + workday.user + ' is fixed. Time: ' + str(workday.time))
        if unfixed:
            for item in unfixed:
                item.stop()
        #now = datetime.datetime.today().time()
        #if now.hour == 23 and now.minute == 59 and now.second == 59:




    def choose_activity(self, activity):
        workday = Workday.query.filter_by(user=self.login, date=datetime.date.today().toordinal()).first()
        if workday:
            workday.activity = activity
        db.session.commit()

    def order_overtime(self, date, actvity):
        newDay = Workday.query.filter_by(user=self.login, date=date).first()
        if newDay:
            newDay.activity = actvity
        else:
            newDay = Workday(self.login, date, actvity)
        newDay.time = 0
        newDay.ended = 1
        db.session.add(newDay)
        db.session.commit()
        return newDay

    def replace_worktime(self, date):
        newDay = Workday.query.filter_by(user=self.login, date=date).first()
        if newDay:
            newDay.activity = 'Vacation'
        else:
            newDay = Workday(self.login, date, 'Vacation')
        #newDay.time = Normative/7 * 3600
        newDay.time = 0
        newDay.ended = 1
        db.session.add(newDay)
        db.session.commit()
        return newDay

    def take_sick(self, date):
        newDay = Workday.query.filter_by(user=self.login, date=date).first()
        if newDay:
            newDay.activity = 'Sick'

        else:
            newDay = Workday(self.login, date, 'Sick')
        #newDay.time = Normative/7 * 3600
        newDay.time = 0
        newDay.ended = 1
        db.session.add(newDay)
        db.session.commit()
        return newDay


class Developer(User):
    def ohhh(self, date, activity):
        newDay = Workday(self.login, date, activity)
        db.session.add(newDay)
        db.session.commit()
        return newDay


class Manager(User):
    def start_dev_day(self, user, activity):
        target = User.query.filter_by(login=user).first()
        target.start_day(activity)
        db.session.commit()

    def end_dev_day(self, user):
        target = User.query.filter_by(login=user).first()
        target.end_day()
        db.session.commit()

    def choose_dev_activity(self, user, activity):
        target = User.query.filter_by(login=user).first()
        target.choose_activity(activity)
        db.session.commit()

    def register_new_user(self, login, password, username, role):
        user = User(login, password, username, role)
        db.session.add(user)
        db.session.commit()

    def delete_user(self, user):
        target = User.query.filter_by(login=user).first()
        if target:
            db.session.delete(target)
            db.session.commit()

def fix_all_func(Quant):
    users = User.query.all()
    for user in users:
        user.fix_time(Quant)
    print('tick-tack')

    #time.sleep(Quant)
    #fix_all_func()
def calculate():
    users = User.query.all()
    today = datetime.date.today()
    #firstday = datetime.date(today.year, today.month, 1)
    for user in users:
        days = Workday.query.filter(Workday.user == user.login,
                                    Workday.calculated == 0,
                                    Workday.date != today.toordinal())
        for day in days:
            if Activity.query.filter_by(name=day.activity).first():
                act_coeff = Activity.query.filter_by(name=day.activity).first().coeff
                if day.activity != 'Sick' and day.activity != 'Vacancy':
                    user.salary += act_coeff * day.time/3600 * RubsPerHour
                else:
                    user.salary += act_coeff * 6 * RubsPerHour

                day.calculated = 1
        #user.worktime = 0
    db.session.commit()

