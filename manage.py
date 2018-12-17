import subprocess
import os
import pytest

from flask_migrate import MigrateCommand
from flask_script import Manager

from resources import fixtures

from alayatodo import app, db
from alayatodo.models import User, Todo

manager = Manager(app)


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output
        os._exit(1)


@manager.command
def initdb():
    _run_sql('resources/database.sql')
    print "AlayaTodo: Database initialized."


@manager.command
def load_fixtures():
    for user in fixtures.USERS:
        db.session.add(User(**user))
        db.session.commit()
    for todo in fixtures.TODOS:
        db.session.add(Todo(**todo))
        db.session.commit()
    print "AlayaTodo: Fixtures loaded."


@manager.command
def test():
    pytest.main(["-s", "alayatodo/tests"])

manager.add_command('db', MigrateCommand)
