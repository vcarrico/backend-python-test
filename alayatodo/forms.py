from flask_wtf import FlaskForm
from wtforms import validators, fields


class TodoForm(FlaskForm):
    description = fields.StringField(u'description', [validators.DataRequired(), ])


class LoginForm(FlaskForm):
    username = fields.StringField(u'username', [validators.DataRequired(), ])
    password = fields.PasswordField(u'password', [validators.DataRequired(), ])
