from app import app, db
from models import Category
from flask import render_template, url_for
@app.route('/')
@app.route('/index')
def index():
	return render_template(
		'index.html',
		title = 'Main',)

@app.route('/about')
def about():
	return render_template(
		'about.html',
		title = 'About',)

@app.route('/contracts')
def contracts():
	categories = Category.query.all()
	return render_template(
		'contracts.html',
		title = 'Contracts',
		categories = categories)