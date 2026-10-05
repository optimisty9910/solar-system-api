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

def validate_planet_id(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        response = {"message": f"planet {planet_id} invalid"}
        abort(make_response(response, 400))

    for planet in planets:
        if planet.id == planet_id:
            return planet

    response = {"message": f"planet {planet_id} not found"}
    abort(make_response(response, 404))
        

@planet_routes.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet_id(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance from sun": planet.distance_from_sun
    }