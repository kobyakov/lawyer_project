from app import db
from webhelpers.text import urlify
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(128), index=True, unique=True)
	slug = db.Column(db.String(128),index=True, unique=True)
	is_contract = db.Column(db.Boolean, default = False)
	types = db.relationship('Type', backref = 'category', lazy = 'dynamic')
	def __repr__(self):
		return '<category %r>' %(self.name)

class Type(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	name = db.Column(db.String(128), index=True, unique=True)
	slug = db.Column(db.String(128),index=True, unique=True)
	is_contract = db.Column(db.Boolean, default = False)
	contracts = db.relationship('Contract', backref = 'type', lazy = 'dynamic')
	
	def __repr__(self):
		return '<type %r>' %(self.name)

class Contract(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
	name = db.Column(db.String(128), index=True, unique=True)
	slug = db.Column(db.String(128),index=True, unique=True)
	is_contract = db.Column(db.Boolean, default = True)
	contract_template = db.Column(db.String(128),index=True, unique=True)
	
	def __repr__(self):
		return '<contract %r>' %(self.name)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(40), unique = True, index = True)
	password_hash = db.Column(db.String(40))
	email = db.Column(db.String(60), unique = True, index = True)
	registered_on = db.Column(db.DateTime)

	def __init__(self, username, password, email):
		self.username = username
		self.email = email.lower()
		self.registered_on = datetime.utcnow()
		self.set_password(password)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % (self.username)	

