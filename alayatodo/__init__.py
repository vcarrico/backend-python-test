import sqlite3

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from alayatodo import settings


app = Flask(__name__)
app.config.from_object(settings)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
csrf.init_app(app)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


import alayatodo.views
