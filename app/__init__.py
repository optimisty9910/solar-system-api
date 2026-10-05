from flask import Flask
from app.routes.planet_routes import planet_routes

def create_app(test_config=None):
    app = Flask(__name__)
    app.register_blueprint(planet_routes)

    return app