from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	task = db.relationship('Task',backref="user", uselist=True)
	
	def __repr__(self):
		return '<User %r>' % self.id
		
	def serialize(self):
		return {
			"id": self.id,
			"email": self.email,
			#do not serialize the password, it's a security breach
		}
		
class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	label = db.Column(db.String(250), nullable=False)
	done = db.Column(db.Boolean(), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	__table_args__=(db.UniqueConstraint(
	"user_id",
	"label",
	name="debe_tener_una_sola_coincidencia"
	),)
	
	def __repr__(self):
		return f'<Task object> f{self.id}'
		
	def serialize(self):
		return {
			"id": self.id,
			"email": self.email,
			#do not serialize the password, it's a security breach
		}