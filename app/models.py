from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	about_me = db.Column(db.String(140))
	avatar = db.Column(db.String)

	animals = db.relationship("Animal", backref='owner', lazy='dynamic')
	alerts = db.relationship("Alert", backref='user', lazy='dynamic')

	def get_avatar(self):
		return self.avatar or ''

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.id)

class Animal(db.Model):
	__tablename__ = 'animals'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	species = db.Column(db.String(100))
	species_common = db.Column(db.String(100))
	dob = db.Column(db.Date)
	avatar = db.Column(db.String)
	weight_units = db.Column(db.String)

	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	weights = db.relationship("AnimalWeight", backref='animal', lazy='dynamic')
	alerts = db.relationship("Alert", backref='animal', lazy='dynamic')

	def get_avatar(self):
		return self.avatar or ''

class AnimalWeight(db.Model):
	__tablename__ = 'weights'

	id = db.Column(db.Integer, primary_key=True)
	weight = db.Column(db.Float, nullable=False)
	date = db.Column(db.Date, nullable=False)

	animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))

class Alert(db.Model):
	__tablename__ = 'alerts'

	id = db.Column(db.Integer, primary_key=True)
	start = db.Column(db.DateTime, nullable=False)
	end = db.Column(db.DateTime)
	message = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)
	repeat_period = db.Column(db.String(10))
	repeat_number = db.Column(db.Integer)

	animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
