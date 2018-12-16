from flask_wtf import FlaskForm
from wtforms import validators, fields


class TodoForm(FlaskForm):
    description = fields.StringField(u'description', [validators.required(), ])


class LoginForm(FlaskForm):
    username = fields.StringField(u'username', [validators.required(), ])
    password = fields.PasswordField(u'password', [validators.required(), ])
