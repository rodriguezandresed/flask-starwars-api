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
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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



@app.route('/user', methods=['GET'])
@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id = None):
	if request.method == 'GET':
		if user_id  is None:
			users = User.query.all()
			users = list(map(lambda user: user.serialize(), users))
			return jsonify(users),200
		else:
			user = User.query.filter_by(id=user_id).first()
			if user is not None:
				return jsonify(user.serialize()),200
			else:
				return jsonify({
					"msg": "user not found"
				}), 404
	if request.method == 'PUT':
		body = request.json
		if not body.get("email"):
			return jsonify({
				"msg": "something happened, try again"				
			}), 400
			
		user_update = User.query.filter_by(id=user_id).first()
		
		if user_update is None:
			return jsonify({
				"msg": "User not found"
			}), 404
			
		try:
		
			user_update.email = body.get("email")
			db.session.commit()
			return jsonify(user.serialize()), 201
		except Exception as error:
			db.session.rollback()
			return jsonify(error.args)
		
		
	if request.method == 'DELETE':		
		user_delete = User.query.filter_by(id=user_id).first()
		if user_delete is None:
			return jsonify({
				"msg": "User not found"
			}), 404
			
		db.session.delete(user_delete)
		
		try: 
			db.session.commit()
			return jsonify([]), 204
		except Exception as error:
			db.session.rollback()
			return jsonify(error.args)			

@app.route('/user', methods=['POST'])
def handle_other_user():
	body = request.json
	
	if not body.get("email"):
		return jsonify({
			"msg": "something happened, try again"
		}), 400
		
	user = User(email=body["email"])
	try:
		db.session.add(user)
		db.session.commit()
		return jsonify(user.serialize()), 201
	
	except Exception as error:
		db.session.rollback()
		return jsonify(error.args), 500
		

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
