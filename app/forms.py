from flask.ext.wtf import Form
from wtforms.ext.dateutil.fields import DateField
from wtforms import StringField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length

class UserEditForm(Form):
	about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])

class AddAnimalForm(Form):
	name = StringField('Name', validators=[DataRequired(), Length(min=0, max=64)])
	species_common = StringField('Species (Common)', validators=[DataRequired(), Length(min=1, max=100)])
	species = StringField('Species', validators=[Length(max=100)])
	dob = DateField('Date of Birth', display_format='%m/%d/%Y')
	avatar = FileField('Photo', validators=[FileAllowed(['jpg',], 'Images Only'),])
