from app import app, db
from models import Category
from forms import AddForm

from flask import render_template, url_for, flash, redirect

from webhelpers.text import urlify
from transliterate import translit

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

@app.route('/add', methods = ['GET', 'POST'])
def add():
	addform = AddForm()
	if addform.validate_on_submit():
		name = addform.name.data
		slug = urlify(translit(name, 'ru', reversed = True))
		new_category = Category(
			name=name,
			slug = slug)
		db.session.add(new_category)
		db.session.commit()
		flash('OK')
		return redirect('/index')
	return render_template('add.html',
		title='Add',
		form = addform)

@app.route('/kobyakov')
	return render_template('kobyakov.html')