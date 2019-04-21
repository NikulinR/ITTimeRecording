from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
import wtforms.validators as valid


class LoginForm(FlaskForm):
  login = StringField('Login', [valid.DataRequired() ])
  password = PasswordField('Password', [valid.DataRequired()])
