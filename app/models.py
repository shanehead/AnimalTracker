from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	about_me = db.Column(db.String(140))
	animals = db.relationship("Animal", backref='user_id', lazy='dynamic')
	avatar = db.Column(db.String)

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
	owner = db.Column(db.Integer, db.ForeignKey('users.id'))
	avatar = db.Column(db.String)

	def get_avatar(self):
		return self.avatar or ''

class AnimalWeight(db.Model):
	__tablename__ = 'weights'

	id = db.Column(db.Integer, primary_key=True)
	# @todo - Pounds? Kilograms? Grams?
	weight = db.Column(db.Float, nullable=False)
	date = db.Column(db.Date, nullable=False)
	animal = db.Column(db.Integer, db.ForeignKey('animals.id'))
