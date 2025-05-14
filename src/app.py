"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from sqlalchemy import select
from models import db, Users, Vehicles, Planets, Characters, Favourites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_users():
    stmt = select(Users)
    users = db.session.execute(stmt).scalars().all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data or "username" not in data:
        return jsonify({"error": "Missing Data"}), 404
    

    new_user = Users(
        email = data["email"],
        password = data["password"],
        username = data["username"],
        firstname = data.get("firstname", None) ,
        lastname = data.get("lastname", None)
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()

    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)
    user.username = data.get("username", user.username)
    db.session.commit()

    return jsonify(user.serialize()), 200


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):

    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()

    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User delete"}), 200


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    stmt = select(Vehicles)
    vehicles = db.session.execute(stmt).scalars().all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200


@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle(id):
    stmt = select(Vehicles).where(Vehicles.id == id)
    vehicle = db.session.execute(stmt).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200


@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing Data"}), 404
    
    new_vehicle = Vehicles(
        name = data["name"],
        model = data.get("model", None),
        cost_credits = data.get("cost_credits", None),
        max_speed = data.get("max_speed", None),
        crew = data.get("crew", None)
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.serialize()), 201


@app.route('/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    data = request.get_json()
    stmt = select(Vehicles).where(Vehicles.id == id)
    vehicle = db.session.execute(stmt).scalar_one_or_none()

    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    
    vehicle.name = data.get("name", vehicle.name)
    db.session.commit()

    return jsonify(vehicle.serialize()), 200


@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):

    stmt = select(Vehicles).where(Vehicles.id == id)
    vehicle = db.session.execute(stmt).scalar_one_or_none()

    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    
    db.session.delete(vehicle)
    db.session.commit()

    return jsonify({"message": "Vehicle delete"}), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    stmt = select(Planets)
    planets = db.session.execute(stmt).scalars().all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    stmt = select(Planets).where(Planets.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing Data"}), 404
    
    new_planet = Planets(
        name = data["name"],
        climate = data.get("climate", None),
        population = data.get("population", None),
        terrain = data.get("terrain", None)
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201


@app.route('/planets/<int:id>', methods=['PUT'])
def update_planet(id):
    data = request.get_json()
    stmt = select(Planets).where(Planets.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    planet.name = data.get("name", planet.name)
    db.session.commit()

    return jsonify(planet.serialize()), 200


@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):

    stmt = select(Planets).where(Planets.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": "Planet delete"}), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    stmt = select(Characters)
    characters = db.session.execute(stmt).scalars().all()
    return jsonify([character.serialize() for character in characters]), 200


@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    stmt = select(Characters).where(Characters.id == id)
    character = db.session.execute(stmt).scalar_one_or_none()
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200


@app.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing Data"}), 404
    
    new_character = Characters(
        name = data["name"],
        gender = data.get("gender", None),
        height = data.get("height"),
        birth_year = data.get("birth_year"),
        skin_color = data.get("skin_color"),
        eyes_color = data.get("eyes_color")
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201


@app.route('/characters/<int:id>', methods=['PUT'])
def update_character(id):
    data = request.get_json()
    stmt = select(Characters).where(Characters.id == id)
    character = db.session.execute(stmt).scalar_one_or_none()

    if character is None:
        return jsonify({"error": "Character not found"}), 404
    
    character.name = data.get("name", character.name)
    db.session.commit()

    return jsonify(character.serialize()), 200


@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):

    stmt = select(Characters).where(Characters.id == id)
    character = db.session.execute(stmt).scalar_one_or_none()

    if character is None:
        return jsonify({"error": "Character not found"}), 404
    
    db.session.delete(character)
    db.session.commit()

    return jsonify({"message": "Character delete"}), 200


@app.route('/users/favourites', methods=['GET'])
def get_favourites():
    stmt = select(Favourites)
    favourites = db.session.execute(stmt).scalars().all()
    if favourites is None:
        return jsonify({"error": "Favourites not found"}), 404
    return jsonify([fav.serialize() for fav in favourites]), 200


@app.route('/favourites/vehicles/<int:vehiclesFav_id>', methods=['POST'])
def new_vehicle_fav(vehiclesFav_id):
    data = request.get_json()
    # stmt = select(Vehicles).where(Vehicles.id == vehiclesFav_id)
    # favourite = db.session.execute(stmt).scalar_one_or_none()
    users_id = data.get('user_id')
    
    if not users_id:
        return jsonify({"error": "User ID is required"}), 400
    
    vehicle = db.session.get(Vehicles, vehiclesFav_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    
    user = db.session.get(Users, users_id)
    if not user:
        return jsonify({"error": "User not found"}), 400

    new_fav = Favourites(
        usersFav_id=users_id,
        vehiclesFav_id=vehiclesFav_id,
        # planetsFav_id=None,
        # charactersFav_id=None,
    )

    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201


@app.route('/favourites/planets/<int:planetsFav_id>', methods=['POST'])
def new_planet_fav(planetsFav_id):
    data = request.get_json()
    # stmt = select(Vehicles).where(Vehicles.id == vehiclesFav_id)
    # favourite = db.session.execute(stmt).scalar_one_or_none()
    users_id = data.get('user_id')

    if not users_id:
        return jsonify({"error": "User ID is required"}), 400
    

    planet = db.session.get(Planets, planetsFav_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    
    user = db.session.get(Users, users_id)
    if not user:
        return jsonify({"error": "User not found"}), 400

    new_fav = Favourites(
        usersFav_id=users_id,
        # vehiclesFav_id=None,
        planetsFav_id=planetsFav_id,
        # charactersFav_id=None
    )

    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201


@app.route('/favourites/characters/<int:charactersFav_id>', methods=['POST'])
def new_character_fav(charactersFav_id):
    data = request.get_json()
    # stmt = select(Vehicles).where(Vehicles.id == vehiclesFav_id)
    # favourite = db.session.execute(stmt).scalar_one_or_none()
    users_id = data.get('user_id')

    if not users_id:
        return jsonify({"error": "User not found"}), 400
    

    character = db.session.get(Characters, charactersFav_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    

    user = db.session.get(Users, users_id)
    if not user:
        return jsonify({"error": "User not found"}), 400
    
    

    new_fav = Favourites(
        usersFav_id=users_id,
        # vehiclesFav_id=None,
        # planetsFav_id=None,
        charactersFav_id=charactersFav_id
    )

    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

@app.route('/favourites/vehicles/<int:vehiclesFav_id>', methods=['DELETE'])
def delete_vehicle_fav(vehiclesFav_id):

    data = request.get_json()
    # stmt = select(Vehicles).where(Vehicles.id == vehiclesFav_id)
    # favourite = db.session.execute(stmt).scalar_one_or_none()
    users_id = data.get('user_id')

    if not users_id:
        return jsonify({"error": "User not found"}), 400
    
    stmt = select(Favourites).where(
        Favourites.usersFav_id == users_id,
        Favourites.vehiclesFav_id == vehiclesFav_id
    )
    vehicle = db.session.execute(stmt).scalars().first()
    
    db.session.delete(vehicle)
    db.session.commit()

    return jsonify({"message": "Vehicle Fav delete"}), 200

@app.route('/favourites/planets/<int:planetsFav_id>', methods=['DELETE'])
def delete_planet_fav(planetsFav_id):

    data = request.get_json()
    # stmt = select(Vehicles).where(Vehicles.id == vehiclesFav_id)
    # favourite = db.session.execute(stmt).scalar_one_or_none()
    users_id = data.get('user_id')

    if not users_id:
        return jsonify({"error": "User not found"}), 400
    
    stmt = select(Favourites).where(
        Favourites.usersFav_id == users_id,
        Favourites.planetsFav_id == planetsFav_id
    )
    planet = db.session.execute(stmt).scalars().first()
    
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": "Planet Fav delete"}), 200


@app.route('/favourites/characters/<int:charactersFav_id>', methods=['DELETE'])
def delete_character_fav(charactersFav_id):

    data = request.get_json()
    # stmt = select(Vehicles).where(Vehicles.id == vehiclesFav_id)
    # favourite = db.session.execute(stmt).scalar_one_or_none()
    users_id = data.get('user_id')

    if not users_id:
        return jsonify({"error": "User not found"}), 400
    
    stmt = select(Favourites).where(
        Favourites.usersFav_id == users_id,
        Favourites.charactersFav_id == charactersFav_id
    )
    character = db.session.execute(stmt).scalars().first()
    
    db.session.delete(character)
    db.session.commit()

    return jsonify({"message": "Character Fav delete"}), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
