from rec import db
import datetime

Normative = 40
RubsPerHour = 250


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
    desc = db.Column('DESCRIPTION', db.String(40))


class Workday(db.Model):
    __tablename__='WORKDAY'
    id = db.Column('ID', db.INTEGER, primary_key=True, autoincrement= True)
    time = db.Column('TIME', db.INTEGER)
    date = db.Column('DATE', db.INTEGER)
    activity = db.Column('ACTIVITY_NAME', db.String(15), db.ForeignKey('ACTIVITY.NAME'), nullable=False)
    user = db.Column('USER_LOGIN',db.String(20), db.ForeignKey('USER.LOGIN'), nullable=False)

    def __init__(self, user, date, activity):
        self.user = user
        self.date = date
        self.time = 0
        self.activity = activity
        db.session.add(self)
        db.session.commit()

    def calculate(self):
        user = User.query.filter_by(login=self.user).first()
        if user:
            act_coeff = Activity.query.filter_by(name=self.activity).first().coeff
            user.salary += act_coeff * self.time/3600 * RubsPerHour
        db.session.commit()
        return act_coeff * self.time/3600 * RubsPerHour


class User(db.Model):
    __tablename__ = 'USER'
    login = db.Column('LOGIN', db.String(20), primary_key=True)
    password = db.Column('PASSWORD', db.String(20), nullable=False)
    salary = db.Column('SALARY', db.INTEGER)
    worktime = db.Column('WORKTIME', db.INTEGER)
    username = db.Column('USERNAME', db.String(50), nullable=False)
    role = db.Column('ROLE_NAME', db.String(15), nullable=False )

    def __init__(self, login, password, username, role):
        if User.query.filter_by(login=login).first():
            return False
        else:
            self.login = login
            self.password = password
            self.username = username
            self.role = role
            db.session.add(self)
            db.session.commit()

    def start_day(self, activity):
        if Activity.query.filter_by(name=activity).first():
            newDay = Workday(self.login, datetime.date.today().toordinal(), activity)
        else:
            newDay = Workday(self.login, datetime.date.today().toordinal(), "Standart")
        db.session.add(newDay)
        db.session.commit()
        return newDay

    def end_day(self):
        workday = Workday.query.filter_by(user=self.login, date=datetime.date.today().toordinal()).first()
        if workday:
            self.worktime += workday.time
        db.session.commit()

    def fix_time(self, time):
        workday = Workday.query.filter_by(user=self.login, date=datetime.date.today().toordinal()).first()
        if workday:
            workday.time += time
        db.session.commit()

    def choose_activity(self, activity):
        workday = Workday.query.filter_by(user=self.login, date=datetime.date.today().toordinal()).first()
        if workday:
            workday.activity = activity
        db.session.commit()


class Developer(User):
    def order_overtime(self, date, activity):
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
            target.delete()
