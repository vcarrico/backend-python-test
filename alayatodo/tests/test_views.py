from flask import url_for


def test_get_home_returns_http_200(app):
    client = app.test_client()

    resp = client.get(url_for('home'))
    assert resp.status_code == 200


def test_get_login_returns_http_200(app):
    client = app.test_client()

    resp = client.get(url_for('login'))
    assert resp.status_code == 200


def test_get_todo_returns_http_302_if_not_logged(app):
    client = app.test_client()

    resp = client.get(url_for('todo', id=1), follow_redirects=False)
    assert resp.status_code == 302


def test_get_todos_list_returns_http_302_if_not_logged(app):
    client = app.test_client()

    resp = client.get(url_for('todos_list'), follow_redirects=False)
    assert resp.status_code == 302


def test_get_todo_insert_returns_http_405(app):
    client = app.test_client()

    resp = client.get(url_for('todo_insert'))
    assert resp.status_code == 405
