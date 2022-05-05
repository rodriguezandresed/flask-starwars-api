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


# class Nature(db.Model):
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = db.Column(db.Integer, primary_key=True)
#     nature_name = db.Column(db.String(250))
#     nature_person = db.relationship('Person', backref="nature", uselist=True)
#     nature_planet = db.relationship('Planet', backref="nature", uselist=True)
#     nature_favorite = db.relationship('Favorite', backref="nature", uselist=True)

#     def __repr__(self):
#         return f'<Nature > f{self.nature_name}'

#     def serialize(self):
#         return {
# 			"natureName": self.natureName,
# 			#do not serialize the password, it's a security breach
# 		}


class Favorite(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_name = db.Column(db.String(250), nullable=False)
    favorite_id = db.Column(db.Integer, nullable=False)
    favorite_nature = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint(
	"user_id","favorite_name","favorite_nature", "favorite_id",
	name="debe_tener_una_sola_coincidencia"
    ),)


    def __repr__(self):
        return f'<Favorite> f{self.id}'

    def serialize(self):
        return {
			"favorite_name": self.favorite_name,
			"favorite_nature":self.favorite_nature,
            "favorite_id":self.favorite_id,
            "user_id":self.user_id
			#do not serialize the password, it's a security breach
		}


class People(db.Model):

    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(250))
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(100))
    mass = db.Column(db.String(100))
    hair_color = db.Column(db.String(100))
    skin_color = db.Column(db.String(100))
    eye_color = db.Column(db.String(100))
    birth_year = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    homeworld = db.Column(db.String(100))

    def __repr__(self):
        return f'<Person> f{self.id}'

    def serialize(self):
        return{
            "id":self.id,
            "image":self.image,
            "height":self.height,
            "mass":self.mass,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color,
            "eye_color":self.eye_color,
            "birth_year":self.birth_year,
            "gender":self.gender,
            "name":self.name,
            "homeworld":self.homeworld,
        }

    def __init__(self, *args, **kwargs):
        """
            "name":"andres",
            "lastname":"rodriguez"


        """
      

        for (key, value) in kwargs.items():
            if hasattr(self, key):
                attr_type = getattr(self.__class__, key).type

                try:
                    attr_type.python_type(value)
                    setattr(self, key, value)
                except Exception as error:
                    print(f"ignota los demas valores: {error.args}")

    @classmethod
    def create(cls, data):
        # creamos instancia
        instance = cls(**data)
        if (not isinstance(instance, cls)):
            print("fallamos")
            return None
        db.session.add(instance)
        try:
            db.session.commit()
            print(f"creado: {instance.name}")
            return instance
        except Exception as error:
            db.session.rollback()
            print(error.args)



class Planets(db.Model):

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(250))
    climate = db.Column(db.String(100))
    diameter = db.Column(db.String(100))
    gravity = db.Column(db.String(100))
    orbital_period = db.Column(db.String(100))
    population = db.Column(db.String(100))
    rotation_period = db.Column(db.String(100))
    surface_water = db.Column(db.String(100))
    terrain = db.Column(db.String(100))

    def __repr__(self):
        return f'<Planets> f{self.uid}'

    def serialize(self):
        return{
            "id":self.id,
            "image":self.image,
            "climate":self.climate,
            "diameter":self.diameter,
            "gravity":self.gravity,
            "name":self.name,
            "orbital_period":self.orbital_period,
            "population":self.population,
            "rotation_period":self.rotation_period,
            "surface_water":self.surface_water,
            "terrain":self.terrain,
        }

    def __init__(self, *args, **kwargs):
        """
            "name":"andres",
            "lastname":"rodriguez"


        """
      

        for (key, value) in kwargs.items():
            if hasattr(self, key):
                attr_type = getattr(self.__class__, key).type

                try:
                    attr_type.python_type(value)
                    setattr(self, key, value)
                except Exception as error:
                    print(f"Ignore the rest: {error.args}")

    @classmethod
    def create(cls, data):
        # creamos instancia
        instance = cls(**data)
        if (not isinstance(instance, cls)):
            print("We failed")
            return None
        db.session.add(instance)
        try:
            db.session.commit()
            print(f"Created: {instance.name}")
            return instance
        except Exception as error:
            db.session.rollback()
            print(error.args)