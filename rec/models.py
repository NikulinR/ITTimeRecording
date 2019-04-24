from rec import db


class Role(db.Model):
    __tablename__ = 'ROLE'
    name = db.Column('NAME', db.String(15), primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Activity(db.Model):
    __tablename__ = 'ACTIVITY'
    name = db.Column('NAME',db.String(15), primary_key=True)
    coeff = db.Column('COEFF', db.REAL, nullable=False)

    def __init__(self, name, coeff):
        self.name = name
        self.coeff = coeff

    def __repr__(self):
        return '<Coeff of %r is %r>' % (self.name, self.coeff)


class Project(db.Model):
    __tablename__='PROJECTS'
    id = db.Column('ID', db.INTEGER, primary_key=True, autoincrement=True)
    coeff = db.Column('COEFF', db.REAL, nullable=False)
    name = db.Column('NAME', db.String(15), nullable=False)


class Normative(db.Model):
    __tablename__='NORMATIVES'
    workday = db.Column('WORKDAYS', db.INTEGER, primary_key=True)


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
    #activity = db.relationship('ACTIVITY')
    #user = db.relationship('USER')


class User(db.Model):
    __tablename__ = 'USER'
    login = db.Column('LOGIN', db.String(20), primary_key=True)
    password = db.Column('PASSWORD', db.String(20), nullable=False)
    salary = db.Column('SALARY', db.INTEGER)
    worktime = db.Column('WORKTIME', db.INTEGER)
    username = db.Column('USERNAME', db.String(50), nullable=False)
    role = db.Column('ROLE_NAME', db.String(15), db.ForeignKey('ROLE.NAME'), nullable=False )
    project = db.Column('PROJECT_ID', db.String(15), db.ForeignKey('PROJECTS.ID'))

    def EndDay(self, time):
        self.worktime += time
        db.session.commit()
    #role = db.relationship('ROLE')
    #project = db.relationship('PROJECTS')