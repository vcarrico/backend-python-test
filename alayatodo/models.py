from sqlalchemy_utils.types.password import PasswordType

from alayatodo import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(PasswordType(
        schemes=['pbkdf2_sha512', ]), nullable=False)
    todos = db.relationship('Todo', backref='person', lazy=True)

    def __repr__(self):
        return "User: {}".format(self.username)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "To-Do <User.id {}>: {}".format(self.user_id, self.description)
