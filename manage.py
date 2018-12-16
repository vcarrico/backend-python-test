import subprocess
import os

from flask_migrate import MigrateCommand
from flask_script import Manager

from alayatodo import app

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
    _run_sql('resources/fixtures.sql')
    print "AlayaTodo: Database initialized."

manager.add_command('db', MigrateCommand)
