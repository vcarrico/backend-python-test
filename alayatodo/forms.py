from wtforms import validators, fields, Form


class TodoForm(Form):
    description = fields.StringField(u'description', [validators.required(), ])


class LoginForm(Form):
    username = fields.StringField(u'username', [validators.required(), ])
    password = fields.PasswordField(u'password', [validators.required(), ])
