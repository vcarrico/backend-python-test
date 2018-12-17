from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from alayatodo import app, db

from alayatodo.forms import TodoForm, LoginForm
from alayatodo.models import Todo
from alayatodo.helpers import (
    login_user, login_redirect, login_required,
    get_previous_page, get_next_page, get_page_max, get_last_page_uncompleted,
    ITEMS_PER_PAGE)


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET', 'POST'])
@login_redirect('/todos')
def login():
    error = ''
    username = request.form.get('username')
    password = request.form.get('password')
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        logged_in = login_user(username=username, password=password)
        if logged_in:
            return redirect('/todos')
        error = "Invalid username or password!"
    return render_template('login.html', error=error, form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<int:id>', methods=['GET'], defaults={'response_format': None})
@app.route('/todo/<int:id>/<response_format>', methods=['GET'])
@login_required
def todo(id, response_format):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if response_format == 'json':
        return todo.to_json()
    return render_template('todo.html', todo=todo)


@app.route('/todos/', defaults={'page': 1})
@app.route('/todos/<int:page>', methods=['GET'], strict_slashes=False)
@login_required
def todos_list(page):
    user_todos_query = Todo.query.filter_by(
        user_id=session['user']['id']).order_by(Todo.completed)

    todos = user_todos_query.all()
    todos_current_page = user_todos_query.paginate(
        page, ITEMS_PER_PAGE, True).items

    context = {
        'todos': todos_current_page,
        'current_page': page,
        'previous_page': get_previous_page(page),
        'next_page': get_next_page(page, len(todos)),
        'max_page': get_page_max(len(todos))
    }
    return render_template('todos.html', **context)


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
        flash("ToDo added successfuly!")
    else:
        flash("ToDo description is required!")
    return redirect(
        url_for(
            'todos_list',
            page=get_last_page_uncompleted(session['user']['id'])))


@app.route('/todo/<id>/delete', methods=['POST', ])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash("ToDo deleted successfuly!")
    return redirect('/todos')


@app.route('/todo/<id>/complete', methods=['POST'])
@login_required
def todo_complete(id):
    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if todo:
        todo.completed = not todo.completed
        db.session.commit()
    return redirect('/todos')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
app.register_error_handler(404, page_not_found)
