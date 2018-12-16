from alayatodo import app, db
from flask import (
    g,
    redirect,
    render_template,
    request,
    session
)

from alayatodo.forms import TodoForm
from alayatodo.models import Todo


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['POST', 'GET'])
@app.route('/todo/', methods=['POST', 'GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')

    form = TodoForm(request.form)
    if request.method == 'POST' and form.validate():
        todo = Todo(
            description=form.data['description'],
            user_id=session['user']['id'])
        db.session.add(todo)
        db.session.commit()
        return redirect('/todo')

    todos = Todo.query.filter_by(user_id=session['user']['id']).all()
    return render_template('todos.html', todos=todos, add_todo_form=form)


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')
