from flask import abort, Blueprint, make_response
from app.models.planet import planets

planet_routes = Blueprint('planet_routes', __name__, url_prefix='/planets')

@planet_routes.route('/', methods=['GET'])
def get_planets():
    planets_response = []

    for planet in planets:
        planets_response.append({
            'id': planet.id,
            'name': planet.name,
            'description': planet.description,
            'distance_from_sun': planet.distance_from_sun
        })

    return make_response(planets_response, 200)