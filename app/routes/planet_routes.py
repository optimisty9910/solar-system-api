from flask import Blueprint, request
from app.models.planet import Planet
from app.db import db
from app.route_utilities import validate_model_id


planet_routes = Blueprint(
    "planet_routes",
    __name__,
    url_prefix="/planets"
)


@planet_routes.post("")
def create_planet():
    request_body = request.get_json()

    new_planet = Planet.from_dict(request_body)

    db.session.add(new_planet)
    db.session.commit()

    return new_planet.to_dict(), 201


@planet_routes.get("")
def get_all_planets():
    query = db.select(Planet)

    name = request.args.get("name")
    if name:
        query = query.filter(
            Planet.name.ilike(f"%{name}%")
        )

    description = request.args.get("description")
    if description:
        query = query.filter(
            Planet.description.ilike(f"%{description}%")
        )

    distance_from_sun = request.args.get("distance_from_sun")
    if distance_from_sun:
        query = query.filter(
            Planet.distance_from_sun >= distance_from_sun
        )

    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(planet.to_dict())

    return planets_response


@planet_routes.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model_id(Planet, planet_id)

    return planet.to_dict()


@planet_routes.patch("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model_id(Planet, planet_id)

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

    return planet.to_dict(), 200


@planet_routes.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model_id(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()

    response = {
        "message": f"Planet {planet_id} deleted successfully"
    }

    return response, 200