from app import app, db, api_manager
from auth import OAuthSignIn
from flask import render_template, url_for, flash, redirect, request, g, make_response, abort, Response
from sqlalchemy.sql import exists
#from forms import UserEditForm, AddAnimalForm, AddWeightForm, WeightGraphForm, AddAlertForm, AddAnimalNoteForm
from models import User, Animal, AnimalWeight, Alert, AnimalNote, api_models, crud_models
from datetime import date
from dateutil.relativedelta import relativedelta
from graphs import plot_weight
from tools import s3_upload
from pprint import pprint
import json

# Create API endpoints
for model_name in api_models:
    model_class = api_models[model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'], allow_patch_many=True)

@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')

@app.route('/add_animal', methods=['POST'])
def add_animal():
    pprint(vars(request))
    print "request.files = '%s" % request.files
    # for attr in dir(request):
    #     print "request.%s" % attr
    #     pprint(getattr(request, attr))
    file = request.files['file']
    print "method=add_animal file='%s'" % str(file)
    if file:
        photo_uri = s3_upload(file)
        data = {'photo_uri': photo_uri}
        resp = Response(json.dumps(data), status=200, mimetype='application/json')
        print resp
        return resp
    #     animal = Animal(name=form.name.data, species=form.species.data,
    #                     species_common=form.species_common.data, dob=form.dob.data,
    #                     owner_id=g.user.id, weight_units=form.weight_units.data)
    #     animal.avatar = photo_path
    #     db.session.add(animal)
    #     db.session.commit()
    #     flash('%s has been added' % form.name.data)
    #     return redirect(url_for('user', id=g.user.id))
    # return render_template('add_animal.html', title='Add an animal', form=form)
#
# @lm.user_loader
# def load_user(id):
# 	return User.query.filter_by(id=id).first()
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	# Send them to their home page if they are logged in
# 	if g.user is not None and g.user.is_authenticated:
# 		return redirect(url_for('user', id=g.user.id))
# 	return render_template('login.html', title='Sign In')
#
# @app.route('/authorize/<provider>')
# def oauth_authorize(provider):
# 	if not current_user.is_anonymous:
# 		return redirect(url_for('index'))
# 	oauth = OAuthSignIn.get_provider(provider)
# 	return oauth.authorize()
#
# @app.route('/callback/<provider>')
# def oauth_callback(provider):
# 	if not current_user.is_anonymous:
# 		return redirect(url_for('user', id=g.user.id))
# 	oauth = OAuthSignIn.get_provider(provider)
# 	username, email, picture = oauth.callback()
# 	if email is None:
# 		flash('Authentication failed')
# 		return redirect(url_for('index'))
# 	this_user = User.query.filter_by(email=email).first()
# 	if this_user is None:
# 		name = username
# 		if name is None or name == "":
# 			name = email.split('@')[0]
# 		this_user = User(email=email, name=name, avatar=picture)
# 		db.session.add(this_user)
# 		db.session.commit()
# 	# Check if their avatar has changed
# 	if this_user.avatar != picture:
# 		this_user.avatar = picture
# 		db.session.add(this_user)
# 		db.session.commit()
# 	login_user(this_user, remember=True)
# 	g.user = this_user
# 	return redirect(url_for('user', id=g.user.id))
#
# @app.route('/logout')
# def logout():
# 	logout_user()
# 	g.user = None
# 	return redirect(url_for('index'))
#
# @app.route('/user/<id>')
# @login_required
# def user(id):
# 	if id == g.user.id:
# 		this_user = g.user
# 	else:
# 		this_user = User.query.filter_by(id=id).first()
# 	if this_user == None:
# 		flash('User %s not found.' % id)
# 		return redirect(url_for('index'))
# 	animals = this_user.animals.all()
# 	return render_template('user.html', user=this_user, animals=animals)
#
# @app.route('/edit_user', methods=['GET', 'POST'])
# @login_required
# def edit_user():
# 	form = UserEditForm()
# 	if request.method == 'POST' and form.validate_on_submit():
# 		g.user.about_me = form.about_me.data
# 		db.session.add(g.user)
# 		db.session.commit()
# 		flash('Your changes have been saved')
# 		return redirect(url_for('user', id=g.user.id))
# 	else:
# 		form.about_me.data = g.user.about_me
# 	return render_template('edit_user.html', form=form, user=g.user)
#
# @app.route('/edit_animal/<id>', methods=['GET', 'POST'])
# @login_required
# def edit_animal(id):
# 	animal = Animal.query.filter_by(id=id).first()
# 	form = AddAnimalForm()
# 	if request.method == 'POST' and form.validate_on_submit():
# 		animal.name = form.name.data
# 		animal.species = form.species.data
# 		animal.species_common = form.species_common.data
# 		animal.weight_units = form.weight_units.data
# 		animal.dob = form.dob.data
# 		if form.avatar.data:
# 			photo_path = s3_upload(form.avatar)
# 			animal.avatar = photo_path
# 		db.session.add(animal)
# 		db.session.commit()
# 		flash('Your changes have been saved')
# 		return redirect(url_for('animal', id=animal.id))
# 	else:
# 		form.name.data = animal.name
# 		form.species.data = animal.species
# 		form.species_common.data = animal.species_common
# 		form.weight_units.data = animal.weight_units
# 		form.dob.data = animal.dob
# 	return render_template('edit_animal.html', form=form, animal=animal)
#
# @app.route('/add_animal', methods=['GET', 'POST'])
# @login_required
# def add_animal():
# 	form = AddAnimalForm()
# 	if request.method == 'POST' and form.validate_on_submit():
# 		photo_path = s3_upload(form.avatar)
# 		animal = Animal(name=form.name.data, species=form.species.data,
# 						species_common=form.species_common.data, dob=form.dob.data,
# 						owner_id=g.user.id, weight_units=form.weight_units.data)
# 		animal.avatar = photo_path
# 		db.session.add(animal)
# 		db.session.commit()
# 		flash('%s has been added' % form.name.data)
# 		return redirect(url_for('user', id=g.user.id))
# 	return render_template('add_animal.html', title='Add an animal', form=form)
#
# @app.route('/animal/<id>')
# def animal(id):
# 	animal = Animal.query.filter_by(id=id).first()
# 	if animal == None:
# 		flash('Animal with ID %d not found.' % id)
# 		return redirect(url_for('index'))
# 	# Calculate the age here
# 	delta = relativedelta(date.today(), animal.dob)
# 	if delta.years != 0:
# 		if delta.months != 0:
# 			animal.age = '%d years, %d months' % (delta.years, delta.months)
# 		else:
# 			animal.age = '%d years' % (delta.years, delta.months)
# 	else:
# 		if delta.months != 0:
# 			if delta.days != 0:
# 				animal.age = '%d months, %d days' % (delta.months, delta.years)
# 			else:
# 				animal.age = '%d months' % (delta.months, delta.years)
# 		else:
# 			animal.age = '%d days' % delta.days
# 	return render_template('animal.html', animal=animal)
#
# @app.route('/weights/<id>', methods=['GET', 'POST'])
# def weights(id):
# 	animal = Animal.query.filter_by(id=id).first()
# 	if animal == None:
# 		flash('Animal with ID %d not found.' % id)
# 		return redirect(url_for('index'))
# 	graph = None
# 	form = None
# 	weights = animal.weights.all()
# 	if weights is not None and len(weights) != 0:
# 		dates = [x.date for x in weights]
# 		first_date = min(dates)
# 		last_date = max(dates)
# 		form = WeightGraphForm(start_date=first_date, end_date=last_date)
# 		if request.method == 'POST' and form.validate_on_submit():
# 			graph = plot_weight(animal, weights, form.start_date.data, form.end_date.data)
# 			return render_template('weights.html', form=form, animal=animal, graph=graph)
# 		else:
# 			graph = plot_weight(animal, weights, first_date, last_date)
# 	return render_template('weights.html', title="Weights", form=form, animal=animal, graph=graph)
#
# @app.route('/add_weight/<animal_id>', methods=['GET', 'POST'])
# @login_required
# def add_weight(animal_id):
# 	animal = Animal.query.filter_by(id=animal_id).first()
# 	form = AddWeightForm()
# 	if request.method == 'POST' and form.validate_on_submit():
# 		weight = AnimalWeight(animal_id=animal_id, weight=form.weight.data, date=form.date.data)
# 		db.session.add(weight)
# 		db.session.commit()
# 		flash("Weight for %s has been added" % animal.name)
# 		return redirect(url_for('weights', id=animal_id))
# 	return render_template("add_weight.html", title="Add Weight", form=form, animal_id=animal)
#
# @app.route('/add_animal_note/<animal_id>', methods=['GET', 'POST'])
# @login_required
# def add_animal_note(animal_id):
# 	animal = Animal.query.filter_by(id=animal_id).first()
# 	form = AddAnimalNoteForm()
# 	if request.method == 'POST' and form.validate_on_submit():
# 		note = AnimalNote(animal_id=animal_id, note=form.note.data)
# 		db.session.add(note)
# 		db.session.commit()
# 		flash("Note for %s has been added" % animal.name)
# 		return redirect(url_for('animal', id=animal_id))
#
# 	return render_template("add_animal_note.html", title="Add Note", form=form, animal_id=animal)
# @app.route('/alerts')
# @login_required
# def alerts():
# 	alerts = g.user.alerts.all()
# 	return render_template("alerts.html", title="Alerts", user=g.user, alerts=alerts)
#
# @app.route('/add_alert', methods=['GET', 'POST'])
# @login_required
# def add_alert():
# 	animals = Animal.query.filter_by(owner_id=g.user.id).all()
# 	form = AddAlertForm(animals=animals)
# 	if request.method == 'POST' and form.validate_on_submit():
# 		alert = Alert(start_date=form.start.data, end_date=form.end.data, message=form.message.data,
# 					  name=form.name.data, repeat_period=form.repeat_period.data,
# 					  repeat_number=form.repeat_number.data, user_id=g.user.id,
# 					  animal_id=form.animal.data)
# 		db.session.add(alert)
# 		db.session.commit()
# 		flash("Alert '%s' has been added" % alert.name)
# 		return redirect(url_for('alerts'))
# 	return render_template("add_alert.html", title="Add Alert", user=g.user, form=form)
#
# @app.route('/edit_alert/<alert_id>', methods=['GET', 'POST'])
# @login_required
# def edit_alert(alert_id):
# 	alert = Alert.query.filter_by(id=alert_id).first()
# 	animals = Animal.query.filter_by(owner_id=g.user.id).all()
# 	form = AddAlertForm(animals=animals)
# 	if request.method == 'POST' and form.validate_on_submit():
# 		alert.start_date = form.start.data
# 		alert.end_date = form.end.data
# 		alert.message = form.message.data
# 		alert.name = form.name.data
# 		alert.repeat_number = form.repeat_number.data
# 		alert.repeat_period = form.repeat_period.data
# 		alert.animal_id = form.animal.data
# 		db.session.add(alert)
# 		db.session.commit()
# 		flash("Your changes have been saved")
# 		return redirect(url_for('alerts'))
# 	else:
# 		form.start.data = alert.start_date
# 		form.end.data = alert.end_date
# 		form.message.data = alert.message
# 		form.name.data = alert.name
# 		form.repeat_number.data = alert.repeat_number
# 		form.repeat_period.data = alert.repeat_period
# 		form.animal.data = alert.animal_id
# 	return render_template("edit_alert.html", title="Edit Alert", user=g.user, form=form)
#
# @app.route('/qrcode/<id>')
# def qrcode(id):
# 	return render_template('qrcode.html', id=id)
#
# @app.before_request
# def before_request():
# 	g.user = current_user
#
# @app.errorhandler(404)
# def not_found_error(error):
# 	return render_template('404.html'), 404
#
# @app.errorhandler(500)
# def internal_error(error):
# 	db.session.rollback()
# 	return render_template('500.html'), 500

