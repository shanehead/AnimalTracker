from flask.ext.wtf import Form
from wtforms.ext.dateutil.fields import DateField
from wtforms import StringField, TextAreaField, DecimalField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length

WEIGHT_UNITS = [('lbs', 'lbs'), ('kg', 'kg'), ('g', 'g')]

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
