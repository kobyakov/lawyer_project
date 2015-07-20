# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, PasswordField, SubmitField
from wtforms.validators import Required, Email
from models import db, User

class SignupForm(Form):
	username = TextField("Username",  [Required("Please enter your username.")])
	email = TextField("Email",  [Required("Please enter your email address."), Email("Please enter your email address.")])
	password = PasswordField('Password', [Required("Please enter a password.")])
	submit = SubmitField("Create account")	
	
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)	
	
	def validate(self):
		if not Form.validate(self):
			return False
	   	user = User.query.filter_by(email = self.email.data.lower()).first()
	 	if user:
			self.email.errors.append("That email is already taken")
			return False
		else:
			return True

class SigninForm(Form):
	email = TextField("Email",  [Required("Please enter your email address."), Email("Please enter your email address.")])
	password = PasswordField('Password', [Required("Please enter a password.")])
	submit = SubmitField("Sign In")
	 
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)	
	def validate(self):
		if not Form.validate(self):
			return False
	   
		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid e-mail or password")
			return False

class AddCategory(Form):
	name = TextField('name', validators = [Required()])
	is_contract = BooleanField('is_contract', default = False)

class AddType(Form):
	name = TextField('name', validators = [Required()])
	is_contract = BooleanField('is_contract', default = False)
	category = SelectField('category', coerce = int, validators = [Required()])

class AddContract(Form):
	name = TextField('name', validators = [Required()])
	is_contract = BooleanField('is_contract', default = True)
	type_ = SelectField('type', coerce = int, validators = [Required()])

