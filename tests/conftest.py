import pytest
from app import app, db
import os

@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        if os.path.exists('test.db'):
            os.remove('test.db')

@pytest.fixture
def client(test_app):
    return test_app.test_client() 