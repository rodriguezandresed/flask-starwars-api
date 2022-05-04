"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Person, Favorite, Nature
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"]=os.environ.get("FLASK_APP_KEY")
jwt = JWTManager(app)
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

		if not body.get("password"):
			return jsonify({
				"msg": "something happened, try again"				
			}), 400
			
		user_update = User.query.filter_by(id=user_id).first()
		
		if user_update is None:
			return jsonify({
				"msg": "User not found"
			}), 404

		user = User(email=body["email"], password=body["password"])	
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
		
	user = User(email=body["email"], password=body["password"])
	try:
		db.session.add(user)
		db.session.commit()
		return jsonify(user.serialize()), 201
	
	except Exception as error:
		db.session.rollback()
		return jsonify(error.args), 500
		
@app.route('/login', methods=['POST'])
def handle_login():
	email=request.json.get("email", None)
	password=request.json.get("password", None)

	if email is not  None and password is not None:
		user = User.query.filter_by(email=email, password=password).one_or_none()
		if user is not None:
			print(user.id)
			create_token=create_access_token(identity=user.id)
			return jsonify(
				{
					"token":create_token,
					"user_id":user.id,
					"email":user.email

				}
			)
		else:
			return jsonify({
			"msg": "Not Found"
		}), 404

	else:
		return jsonify({
			"msg": "something happened, try again"
		}), 400

@app.route('/planets', methods=['GET'])
@app.route('/planets/<int:planet_uid>', methods=['GET'])
def handle_planet(planet_uid= None):
	if request.method == 'GET':
		if planet_uid  is None:
			planets = Planet.query.all()
			planets = list(map(lambda planet: planet.serialize(), planets))
			return jsonify(planets),200
		else:
			planet = Planet.query.filter_by(uid=planet_uid).first()
			if planet is not None:
				return jsonify(planet.serialize()),200
			else:
				return jsonify({
					"msg": "Planet not found"
				}), 404

@app.route('/person', methods=['GET'])
@app.route('/person/<int:person_uid>', methods=['GET'])
def handle_person(person_uid= None):
	if request.method == 'GET':
		if person_uid is None:
			people = Person.query.all()
			people = list(map(lambda person: person.serialize(), people))
			return jsonify(people),200
		else:
			person = Person.query.filter_by(uid=person_uid).first()
			if person is not None:
				return jsonify(person.serialize()),200
			else:
				return jsonify({
					"msg": "Person not found"
				}), 404
	

@app.route('/favorites', methods=['GET'])
@app.route('/favorites/<string:nature>/<int:name_uid>', methods=['GET', 'DELETE'])
@jwt_required()
def handle_favorite(nature=None, name_uid=None, favorite_id= None):
	user = get_jwt_identity()
	if request.method == 'GET':
		if favorite_id  is None and name_uid is None and nature is None:
			favorites = Favorite.query.filter_by(user_id=user)
			favorites = list(map(lambda favorite: favorite.serialize(), favorites))
			return jsonify(favorites),200
		else:
			favorite = Favorite.query.filter_by(user_id=user).first()
			if favorite is not None:
				return jsonify(favorite.serialize()),200
			else:
				return jsonify({
					"msg": "user not found"
				}), 404
	
	if request.method == 'DELETE':
		print(nature)
		if nature == "planet":	
			favorite_delete = Favorite.query.filter_by(favorite_nature=1,favorite_uid=name_uid,user_id=user ).first()
		if nature == "person":
			favorite_delete = Favorite.query.filter_by(favorite_nature=2,favorite_uid=name_uid, user_id=user).first()
		else:
			pass
		if favorite_delete is None:
			return jsonify({
				"msg": "Favorite not found"
			}), 404
			
		db.session.delete(favorite_delete)
		
		try: 
			db.session.commit()
			return jsonify([]), 204
		except Exception as error:
			db.session.rollback()
			return jsonify(error.args)	

@app.route('/favorites/<string:nature>/<int:name_uid>', methods=['POST'])
@jwt_required()
def handle_add_favorite(nature, name_uid):
	body=request.json
	body_name=body.get("favorite_name", None)
# creo que no hace falta, [update] lo que no es *****
#	body_nature=body.get("favorite_nature", None)

	if body_name is not  None:
		user = get_jwt_identity()
		if user is not None:
			nature_id = Nature.query.filter_by(nature_name = nature.lower()).first()
			if nature == "planet":
				wildcard=1
				name = Planet.query.filter_by(planet_name = body_name).first()
				if name is not None:
					favorite= Favorite.query.filter_by(favorite_name=body_name, user_id=user).first()
					if favorite is not None:
							return jsonify({
								"msg":"Favorited item already exists!"
							})
					else:
						favorite = Favorite(favorite_name=body["favorite_name"], favorite_nature=wildcard,favorite_uid=name_uid, user_id=user )	
						try:
							db.session.add(favorite)
							db.session.commit()
							return jsonify(favorite.serialize()), 201
						except Exception as error:
							db.session.rollback()
							return jsonify(error.args), 500
				else: 
					return jsonify({
									"msg": "Planet does not exist!"
									}), 400
			elif nature == "person":
				wildcard=2
				name = Person.query.filter_by(person_name = body_name).first()
				if name is not None:
					## para sqlflask el comparativo AND es una , 
					favorite= Favorite.query.filter_by( favorite_name=body_name, user_id=user ).first()
					if favorite is not None:
							return jsonify({
								"msg":"Favorited item already exists!"
							})
					else:
						favorite = Favorite(favorite_name=body["favorite_name"], favorite_nature=wildcard,favorite_uid=name_uid,  user_id=user )	
						try:
							db.session.add(favorite)
							db.session.commit()
							return jsonify(favorite.serialize()), 201
						except Exception as error:
							db.session.rollback()
							return jsonify(error.args), 500
				else: 
					return jsonify({
									"msg": "Person does not exist!"
									}), 400
			else:
				return jsonify({
								"msg": "Not a Planet or a Person!"
								}), 400
		else:
				return jsonify({
								"msg": "Please log in!"
								}), 400
	else:
		return jsonify({
						"msg": "something happened, try again [bad body format]"
						}), 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
