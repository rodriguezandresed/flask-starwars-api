from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)

	def __repr__(self):
		return '<User %r>' % self.id

	def serialize(self):
		return {
			"id": self.id,
			"email": self.email,
			#do not serialize the password, it's a security breach
		}


class Nature(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nature_name = db.Column(db.String(250))
    nature_person = db.relationship('Person', backref="nature", uselist=True)
    nature_planet = db.relationship('Planet', backref="nature", uselist=True)
    nature_favorite = db.relationship('Favorite', backref="nature", uselist=True)

    def __repr__(self):
        return f'<Nature > f{self.nature_name}'

    def serialize(self):
        return {
			"natureName": self.natureName,
			#do not serialize the password, it's a security breach
		}


class Favorite(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_name = db.Column(db.String(250), nullable=False)
    favorite_uid = db.Column(db.Integer, nullable=False)
    favorite_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))
    __table_args__ = (db.UniqueConstraint(
	"user_id","favorite_name","favorite_nature", "favorite_uid",
	name="debe_tener_una_sola_coincidencia"
    ),)


    def __repr__(self):
        return f'<Favorite> f{self.id}'

    def serialize(self):
        return {
			"favorite_name": self.favorite_name,
			"favorite_nature":self.favorite_nature,
            "favorite_uid":self.favorite_uid,
            "user_id":self.user_id
			#do not serialize the password, it's a security breach
		}


class Person(db.Model):

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    uid = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(250))
    person_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))
    

    def __repr__(self):
        return f'<Person> f{self.uid}'

    def serialize(self):
        return {
			"person_name": self.person_name,
			"person_nature":self.person_nature,
            "person_uid":self.uid
			#do not serialize the password, it's a security breach
		}


class Planet(db.Model):

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    uid = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(250))
    planet_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))

    def __repr__(self):
        return f'<Planet> f{self.uid}'

    def serialize(self):
        return {
			"planet_name": self.planet_name,
			"planet_nature":self.planet_nature,
            "planet_uid":self.uid
			#do not serialize the password, it's a security breach
		}


