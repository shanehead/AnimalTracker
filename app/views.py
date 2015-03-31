from app import app, db, lm, oid
from flask import render_template, url_for, flash, redirect, session, request, g, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, UserEditForm, AddAnimalForm
from models import User, Animal, AnimalWeight
from datetime import datetime, date
from uuid import uuid4
from werkzeug import secure_filename
from dateutil.relativedelta import relativedelta

@app.route('/')
@app.route('/index')
@login_required
def index():
	# Send them to their home page if they are logged in
	# login_required decorator will send them to the login page if they aren't
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('user', nickname=g.user.nickname))

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
	# Send them to their home page if they are logged in
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('user', nickname=g.user.nickname))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
	return render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
	logout_user()
	g.user = None
	return redirect(url_for('index'))

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash("Invalid login. PLease try again")
		return redirect(url_for('login'))
	user = User.query.filter_by(email=resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		nickname = User.make_unique_nickname(nickname)
		user = User(nickname=nickname, email=resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User %s not found.' % nickname)
		return redirect(url_for('index'))
	animals = user.animals.all()
	return render_template('user.html', user=user, animals=animals)

@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
	form = UserEditForm(g.user.nickname)
	if request.method == 'POST' and form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		if form.avatar.data:
			g.user.avatar = "%s_%s" % (uuid4(), secure_filename(form.avatar.data.filename))
			photo_path = app.config['MEDIA_FOLDER'] + '/' + g.user.avatar
			form.avatar.data.save(photo_path)
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved')
		return redirect(url_for('user', nickname=g.user.nickname))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit_user.html', form=form, user=g.user)

@app.route('/edit_animal/<id>', methods=['GET', 'POST'])
@login_required
def edit_animal(id):
	animal = Animal.query.filter_by(id=id).first()
	form = AddAnimalForm()
	if request.method == 'POST' and form.validate_on_submit():
		animal.name = form.name.data
		animal.species = form.species.data
		animal.species_common = form.species_common.data
		animal.dob = form.dob.data
		if form.avatar.data:
			animal.avatar = "%s_%s" % (uuid4(), secure_filename(form.avatar.data.filename))
			photo_path = app.config['MEDIA_FOLDER'] + '/' + animal.avatar
			form.avatar.data.save(photo_path)
		db.session.add(animal)
		db.session.commit()
		flash('Your changes have been saved')
		return redirect(url_for('animal', id=animal.id))
	else:
		form.name.data = animal.name
		form.species.data = animal.species
		form.species_common.data = animal.species_common
		form.dob.data = animal.dob
	return render_template('edit_animal.html', form=form, animal=animal)

@app.route('/add_animal', methods=['GET', 'POST'])
@login_required
def add_animal():
	form = AddAnimalForm()
	if request.method == 'POST' and form.validate_on_submit():
		photo_filename = "%s_%s" % (uuid4(), secure_filename(form.avatar.data.filename))
		photo_path = app.config['MEDIA_FOLDER'] + '/' + photo_filename
		animal = Animal(name=form.name.data, species=form.species.data,
						species_common=form.species_common.data, dob=form.dob.data, owner=g.user.id)
		animal.avatar = photo_filename
		form.avatar.data.save(photo_path)
		db.session.add(animal)
		db.session.commit()
		flash('%s has been added' % form.name.data)
		return redirect(url_for('user', nickname=g.user.nickname))
	return render_template('add_animal.html', title='Add an animal', form=form)

@app.route('/animal/<id>')
def animal(id):
	animal = Animal.query.filter_by(id=id).first()
	if animal == None:
		flash('Animal with ID %d not found.' % id)
		return redirect(url_for('index'))
	# Calculate the age here
	delta = relativedelta(date.today(), animal.dob)
	if delta.years != 0:
		if delta.months != 0:
			animal.age = '%d years, %d months' % (delta.years, delta.months)
		else:
			animal.age = '%d years' % (delta.years, delta.months)
	else:
		if delta.months != 0:
			if delta.days != 0:
				animal.age = '%d months, %d days' % (delta.months, delta.years)
			else:
				animal.age = '%d months' % (delta.months, delta.years)
		else:
			animal.age = '%d days' % delta.days
	return render_template('animal.html', animal=animal)

@app.route('/uploads/<img_name>')
def uploads(img_name):
	return send_from_directory(app.config['MEDIA_FOLDER'], img_name)

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

