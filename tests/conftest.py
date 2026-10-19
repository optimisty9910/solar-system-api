import pytest
from app import create_app
from app.db import db
from app.models.planet import Planet
from flask.signals import request_finished
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_saved_planet(app):
    # Arrange
    earth = Planet(
        name="Earth", 
        description="The third planet from the Sun", 
        distance_from_sun=149.6)
    db.session.add(earth)
    db.session.commit()
    
    