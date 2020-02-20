"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Jobs, Users, Achievements
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/register', methods=['POST'])
def handle_login():

    json = request.get_json()

    db.session.add(Users(
        first_name = json['first_name'],
        last_name = json['last_name'],
        username = json['username'],
        date_of_birth = json['date_of_birth'],
        email = json['email']
    ))
    db.session.commit()
    return jsonify(json)

@app.route('/users')
def get_user():

    return jsonify( Users.query.get(7).serialize() )

@app.route('/delete')
def delete():

    db.session.delete(Achievements.query.get())
    db.session.commit()
    return 'done'
    
    
@app.route('/achievements', methods=['POST'])
def achievements():

    json = request.get_json()

    db.session.add(Achievements(
        user_id = json['user_id'],
        achievement = json['achievement'],
        reward = json['reward']
    ))
    db.session.commit()
    return jsonify(json)

@app.route('/change', methods=['POST'])
def handle_change():

    json = request.get_json()
    member = Users.query.filter_by(json["first_name"]).first()
    member_dict = member.serialize()
    if member is None:
        return 'User Not Found: 404'
    
    return jsonify(member_dict)

@app.route('/ex_1', methods=['POST'])
def handle_ex_1():

    json = request.get_json()

    db.session.add(Jobs(
        job_name = json['name'],
        job_place = json['place'],
        job_pay = json['pay']
    ))
    db.session.commit()
    return jsonify(json)

@app.route('/ex_2', methods=['GET'])
def handle_ex_2():

    employ = Jobs.query.get(5)
    employ_dict = employ.serialize()
    
    return jsonify(employ_dict)



@app.route('/got_it', methods=['POST', 'GET'])
def handle_got_it():

    return 'got it'

@app.route('/all_odd', methods=['POST', 'GET'])
def handle_all_odd():
    i = 0
    all_odds = []
    while i < 20:
        i += 1
        if i %2 != 0:
            all_odds.append(i)
    return jsonify(all_odds)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
