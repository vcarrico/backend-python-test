from decouple import config


DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = config('SECRET_KEY', default='dev_secret_key')
USERNAME = 'admin'
PASSWORD = 'default'

SQLALCHEMY_DATABASE_URI = config(
    'SQLALCHEMY_DATABASE_URI', default='sqlite:///{}'.format(DATABASE))
