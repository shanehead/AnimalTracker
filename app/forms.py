from flask.ext.wtf import Form
from wtforms.ext.dateutil.fields import DateField
from wtforms import StringField, BooleanField, TextAreaField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
	openid = StringField('Open ID', validators=[DataRequired()])
	remember_me = BooleanField('Remember me', default=False)

class EditForm(Form):
	avatar = FileField('Photo')
	nickname = StringField('Nickname', validators=[DataRequired()])
	about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])

	def __init__(self, original_nickname, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_nickname = original_nickname

	def validate(self):
		if not Form.validate(self):
			return False
		if self.nickname.data == self.original_nickname:
			return True
		user = User.query.filter_by(nickname=self.nickname.data).first()
		if user != None:
			self.nickname.errors.append('This nickname is already in use. Please choose another one.')
			return False
		return True

class AddAnimalForm(Form):
	name = StringField('Name', validators=[DataRequired(), Length(min=0, max=64)])
	species_common = StringField('Species (Common)', validators=[DataRequired(), Length(min=1, max=100)])
	species = StringField('Species', validators=[Length(max=100)])
	dob = DateField('Date of Birth', display_format='%m/%d/%Y')
	avatar = FileField('Photo')
