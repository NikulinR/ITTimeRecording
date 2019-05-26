from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField
import wtforms.validators as valid


class LoginForm(FlaskForm):
    login = StringField('Login',  [valid.DataRequired(), valid.Length(min=4, max=20)])
    password = PasswordField('Password', [valid.DataRequired(), valid.Length(min=2, max=20)])


class OvertimeForm(FlaskForm):
    date = DateField('Date', [valid.DataRequired()], format='%Y-%m-%d')


class RegisterForm(FlaskForm):
    login = StringField('Login', [valid.DataRequired(), valid.Length(min=4, max=20)])
    password = PasswordField('Password', [valid.DataRequired(), valid.Length(min=2, max=20)])
    role = SelectField('Role', choices=[('Manager', 'Manager'), ('Developer', 'Developer')], default='Developer')
    username = StringField('Username', [valid.DataRequired()])
