from app import app
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
	return render_template(
		'contracts.html',
		title = 'Contracts',)