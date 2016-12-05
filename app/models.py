from app import db

class User(db.Model):
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
        return '<User %r>' % self.id

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
    group_id = db.Column(db.Integer, db.ForeignKey('animal_group.id'))
    weights = db.relationship("AnimalWeight", backref='animal', lazy='dynamic')
    notes = db.relationship("AnimalNote", backref='animal', lazy='dynamic')
    alerts = db.relationship("Alert", backref='animal', lazy='dynamic')

    def get_avatar(self):
        return self.avatar or ''

class AnimalWeight(db.Model):
    __tablename__ = 'weights'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))

class AnimalGroup(db.Model):
    __tablename__ = 'animal_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class AnimalNote(db.Model):
    __tablename__ = 'animal_notes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, server_default=db.text('now()'))
    note = db.Column(db.String, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    message = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    repeat_period = db.Column(db.String(10))
    repeat_number = db.Column(db.Integer)

    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# models we want to create API endpoints for
api_models = {'user': User, 'animal': Animal, 'animal_weight': AnimalWeight,
              'animal_group': AnimalGroup, 'animal_note': AnimalNote, 'alert': Alert}

# models we want CRUD-style endpoints and pass the routing to the Angular app
crud_models = {'user': User, 'animal': Animal, 'animal_weight': AnimalWeight,
               'animal_group': AnimalGroup, 'animal_note': AnimalNote, 'alert': Alert}
