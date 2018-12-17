import pytest

from alayatodo import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/alayatodo_test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    db.init_app(app)

    with app.app_context():
        from alayatodo.views import *  # noqa
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
