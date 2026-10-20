from flask import abort, make_response
from .db import db


def validate_model_id(model, model_id):
    model_name = model.__name__

    try:
        model_id = int(model_id)
    except (TypeError, ValueError):
        response = {
            "message": f"{model_name} {model_id} invalid"
        }
        abort(make_response(response, 400))

    instance = db.session.get(model, model_id)

    if instance:
        return instance

    response = {
        "message": f"{model_name} {model_id} not found"
    }
    abort(make_response(response, 404))
