from decouple import config


DEBUG = True
SECRET_KEY = config('SECRET_KEY', default='dev_secret_key')


# DB Settings
DATABASE = '/tmp/alayatodo.db'
SQLALCHEMY_DATABASE_URI = config(
    'SQLALCHEMY_DATABASE_URI', default='sqlite:///{}'.format(DATABASE))
SQLALCHEMY_TRACK_MODIFICATIONS = True
MIGRATIONS_DIRECTORY = 'resources/migrations'
