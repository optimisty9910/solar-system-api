from flask import abort, Blueprint, make_response, request
from app.models.planet import Planet
from ..db import db

planet_routes = Blueprint('planet_routes', __name__, url_prefix='/planets')

@planet_routes.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    distance_from_sun = request_body["distance_from_sun"]

    new_planet = Planet(name=name, description=description, distance_from_sun=distance_from_sun)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "distance_from_sun": new_planet.distance_from_sun,
    }

    return response, 201


@planet_routes.get("")
def get_all_planets():
    query = db.select(Planet)

    name = request.args.get("name")
    if name:
        query = query.filter(Planet.name.ilike(f"%{name}%"))

    description = request.args.get("description")
    if description:
        query = query.filter(Planet.description.ilike(f"%{description}%"))
    
    distance_from_sun = request.args.get("distance_from_sun")
    if distance_from_sun:
        query = query.filter(Planet.distance_from_sun >= (distance_from_sun))

    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "distance_from_sun": planet.distance_from_sun
            }
        )
    return planets_response

def validate_planet_id(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        response = {"message": f"Planet {planet_id} invalid"}
        abort(make_response(response, 400))

    planet = db.session.get(Planet, planet_id)
    if planet:
        return planet

    response = {"message": f"Planet {planet_id} not found"}
    abort(make_response(response, 404))
        

@planet_routes.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet_id(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance_from_sun": planet.distance_from_sun
    }

@planet_routes.patch("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet_id(planet_id)

    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict):
        return {"message": "Invalid planet data"}, 400

    if "name" in request_body:
        planet.name = request_body["name"]

    if "description" in request_body:
        planet.description = request_body["description"]

    if "distance_from_sun" in request_body:
        planet.distance_from_sun = request_body["distance_from_sun"]

    db.session.commit()

    response = {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance_from_sun": planet.distance_from_sun
    }

    return response, 200


@planet_routes.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet_id(planet_id)

    db.session.delete(planet)
    db.session.commit()

    response = {
        "message": f"Planet {planet_id} deleted successfully"
    }

    return response, 200