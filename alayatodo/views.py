from flask import (
    redirect,
    render_template,
    request,
    session
)

from alayatodo import app, db

from alayatodo.forms import TodoForm, LoginForm
from alayatodo.models import Todo
from alayatodo.helpers import (
    login_user, login_redirect, login_required)


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET', 'POST'])
@login_redirect('/todo')
def login():
    error = ''
    username = request.form.get('username')
    password = request.form.get('password')
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        logged_in = login_user(username=username, password=password)
        if logged_in:
            return redirect('/todo')
        error = "Invalid username or password!"
    return render_template('login.html', error=error, form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'], strict_slashes=False)
@login_required
def todos_list():
    todos = Todo.query.filter_by(user_id=session['user']['id']).all()
    return render_template('todos.html', todos=todos, add_todo_form=TodoForm())


@app.route('/todo', methods=['POST'], strict_slashes=False)
@login_required
def todo_insert():
    form = TodoForm(request.form)
    if form.validate():
        todo = Todo(
            description=form.data['description'],
            user_id=session['user']['id'])
        db.session.add(todo)
        db.session.commit()
        return redirect('/todo')

    todos = Todo.query.filter_by(user_id=session['user']['id']).all()
    return render_template('todos.html', todos=todos, add_todo_form=form)


@app.route('/todo/<id>/delete', methods=['POST', ])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>/complete', methods=['POST'])
@login_required
def todo_complete(id):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if todo:
        todo.completed = not todo.completed
        db.session.commit()
    return redirect('/todo')
