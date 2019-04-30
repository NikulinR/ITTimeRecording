from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
import wtforms.validators as valid


class LoginForm(FlaskForm):
    login = StringField('Login', [valid.DataRequired()])
    password = PasswordField('Password', [valid.DataRequired()])


class OvertimeForm(FlaskForm):
    date = DateField('Date', [valid.DataRequired()], format='%Y-%m-%d')


class RegisterForm(FlaskForm):
    login = StringField('Login', [valid.DataRequired()])
    password = StringField('Password', [valid.DataRequired()])
    role = StringField('Role', [valid.DataRequired()])
    username = PasswordField('Username', [valid.DataRequired()])