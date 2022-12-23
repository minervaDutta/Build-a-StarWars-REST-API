"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
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

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    response_API = requests.get('https://swapi.dev/api/people')
    print(response_API)

    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return response_API.json()["results"], 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    response_API = requests.get('https://swapi.dev/api/planets')
    print(response_API)

    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return response_API.json()["results"], 200


@app.route('/people/<people_id>', methods=['GET'])
def get_all_people_id(people_id):
    response_API = requests.get('https://swapi.dev/api/people/'+people_id)
    print(response_API)

    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return response_API.json(), 200

@app.route('/planets/<planet_id>', methods=['GET'])
def get_all_planet_id(planet_id):
    response_API = requests.get('https://swapi.dev/api/planets/'+planet_id)
    print(response_API)

    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return response_API.json(), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    # query = db.select([User])
    # result = connection.execute(query).fetchall()
    users_query=User.query.all()
    all_users=list(map(lambda x:x.serialize(),users_query))
    print(all_users)
    return all_users, 200

@app.route('/favourite/planet/<planet_id>/<user_id>', methods=['GET'])
def get_all_users_planets(planet_id, user_id):
    user1 = User.query.get(user_id)
    if user1 is None:
        user1 = User(id=user_id, favourite_planets=json.dumps([planet_id]), favourite_people=json.dumps([]))
        db.session.add(user1)
        db.session.commit()
        return "OK", 200
    fav_planets = json.loads(user1.favourite_planets) #changes str to list
    fav_planets.append(planet_id) #adds to list
    user1.favourite_planets = json.dumps(fav_planets) #list to str

    db.session.commit()
    return "New planet added", 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

# [GET] /people