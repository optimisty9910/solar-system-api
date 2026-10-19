def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get('/planets')

    # Assert
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_one_planet(client, one_saved_planet):
    # Act
    response = client.get("/planets/1")

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "name": "Earth",
        "description": "The third planet from the Sun",
        "distance_from_sun": 149.6
    }

def test_get_one_planet_with_nonexistent_id(client):
    # Act
    response = client.get("/planets/999")

    # Assert
    assert response.status_code == 404
    assert response.get_json() == {"message": "Planet 999 not found"}

def test_get_all_planets_with_records(client, one_saved_planet):
    # Act
    response = client.get('/planets')

    # Assert
    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "name": "Earth",
            "description": "The third planet from the Sun",
            "distance_from_sun": 149.6
        }
    ]

def test_create_planet(client):
    # Arrange
    new_planet = {
        "name": "Mars",
        "description": "The fourth planet from the Sun",
        "distance_from_sun": 227.9
    }

    # Act
    response = client.post('/planets', json=new_planet)

    # Assert
    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Mars",
        "description": "The fourth planet from the Sun",
        "distance_from_sun": 227.9
    }
