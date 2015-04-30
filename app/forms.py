from flask.ext.wtf import Form
from wtforms.ext.dateutil.fields import DateField, DateTimeField
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, optional

WEIGHT_UNITS = [('lbs', 'lbs'), ('kg', 'kg'), ('g', 'g')]
PERIOD_UNITS = [(None, None), ('days', 'days'), ('weeks', 'weeks'), ('months', 'months')]

class UserEditForm(Form):
	about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])

class AddAnimalForm(Form):
	name = StringField('Name', validators=[DataRequired(), Length(min=0, max=64)])
	species_common = StringField('Species (Common)', validators=[DataRequired(), Length(min=1, max=100)])
	species = StringField('Species', validators=[Length(max=100)])
	dob = DateField('Date of Birth', display_format='%m/%d/%Y')
	weight_units = SelectField('Weight Units', choices=WEIGHT_UNITS)
	avatar = FileField('Photo', validators=[FileAllowed(['jpg',], 'Images Only')])

class AddWeightForm(Form):
	weight = DecimalField('Weight', validators=[DataRequired()])
	date = DateField('Date', display_format='%m/%d/%Y')

class WeightGraphForm(Form):
	start_date = DateField('Start Date', display_format='%m/%d/%Y')
	end_date = DateField('End Date', display_format='%m/%d/%Y')

	def __init__(self, start_date, end_date, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.start_date.default = start_date
		self.end_date.default = end_date

class AddAlertForm(Form):
	name = StringField('Name', validators=[DataRequired()])
	start = DateTimeField('Start Datetime', validators=[DataRequired()])
	end = DateTimeField('End Datetime', validators=[optional()])
	message = StringField('Message', validators=[DataRequired()])
	repeat_period = SelectField('Repeat Period', choices=PERIOD_UNITS)
	repeat_number = IntegerField('Repeat Number', validators=[optional()])
	animal = SelectField('Animal', coerce=int)

	def __init__(self, animals, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		animal_ids = [x.id for x in animals]
		animal_names = [x.name for x in animals]
		self.animal.choices = zip(animal_ids, animal_names)

