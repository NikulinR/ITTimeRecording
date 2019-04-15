from flask_wtf import Form
from wtforms import StringField, PasswordField
import wtforms.validators as valid


class LoginForm(Form):
  login = StringField('Login', [valid.DataRequired() ])
  password = PasswordField('Password', [valid.DataRequired()])
