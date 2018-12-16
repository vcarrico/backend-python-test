from wtforms import validators, Form, StringField


class TodoForm(Form):
    description = StringField(u'description', [validators.required(), ])
