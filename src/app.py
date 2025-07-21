import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_current_user_favorites():
    user_id = request.args.get("user_id")
    if not user_id:
        raise APIException("You must provide a user_id", 400)
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([fav.serialize() for fav in favorites]), 200

@app.route('/people', methods=['GET'])
def get_people():
    characters = Character.query.all()
    return jsonify([char.serialize() for char in characters]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    character = Character.query.get(people_id)
    if not character:
        raise APIException("Character not found", 404)
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        raise APIException("Planet not found", 404)
    return jsonify(planet.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    user_id = request.json.get("user_id")
    if not user_id:
        raise APIException("user_id is required", 400)
    fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    user_id = request.json.get("user_id")
    if not user_id:
        raise APIException("user_id is required", 400)
    fav = Favorite(user_id=user_id, character_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify(fav.serialize()), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    user_id = request.args.get("user_id")
    if not user_id:
        raise APIException("user_id is required", 400)
    fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        raise APIException("Favorite not found", 404)
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    user_id = request.args.get("user_id")
    if not user_id:
        raise APIException("user_id is required", 400)
    fav = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not fav:
        raise APIException("Favorite not found", 404)
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite character deleted"}), 200

@app.route('/user', methods=['GET'])
def handle_hello():
    return jsonify({"msg": "Hello, this is your GET /user response"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)