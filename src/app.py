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
from models import db, User, States

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
    all_users = User.query.all() ## tengo una lista 
    all_users = list(map(lambda x: x.serialize(), all_users))

    print((all_users))
    return jsonify(all_users), 200

@app.route('/states', methods=['GET'])
def get_states():
    all_states = States.query.all()
    all_states = list(map(lambda x: x.serialize(), all_states))

    print(all_states)

    return jsonify(all_states), 200

@app.route('/user', methods=['POST'])
def add_user():
    body = request.get_json()
    user = User(username = body['username'], postal_code = body['postal_code'])
    try: 
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 200
    except: 
        return jsonify({ 'err_msg': 'can`t add user'}), 400
    
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({}), 204

# @app.route('/users', methods=['GET'])
# def get_users():
#     all_users = User.query.all()
#     all_users = list(map(lambda x: x.serialize(), all_users))

#     return jsonify(all_users), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
