from flask import session, redirect
from functools import wraps

from alayatodo.models import User


def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['user'] = user.to_dict()
        session['logged_in'] = True
        return True


def login_redirect(url_redirect):
    def decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if session.get('logged_in'):
                return redirect(url_redirect)
            return func(*args, **kwargs)
        return func_wrapper
    return decorator


def login_required(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return func(*args, **kwargs)
    return func_wrapper
