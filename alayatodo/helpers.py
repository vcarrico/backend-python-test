from math import ceil

from flask import session, redirect
from functools import wraps

from alayatodo.models import User, Todo

ITEMS_PER_PAGE = 5


# Login Helpers
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


# Pagination Helpers
def get_page_max(items_count):
    return int(ceil(items_count / float(ITEMS_PER_PAGE)))


def get_next_page(page, items_count):
    return min(page + 1, get_page_max(items_count))


def get_previous_page(page):
    return max(page - 1, 1)


def get_last_page_uncompleted(user_id):
    """It gets the last page of uncompleted `todos` from an user."""
    user_todos = Todo.query.filter_by(user_id=user_id, completed=False).all()
    return get_page_max(len(user_todos))
