from app import db

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	animals = db.relationship("Animal", backref='user_id', lazy='dynamic')
	avatar = db.Column(db.String)

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname=nickname).first() is None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname=new_nickname).first() is None:
				return new_nickname
			version += 1
		return new_nickname

	def get_avatar(self):
		return self.avatar or ''

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

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
