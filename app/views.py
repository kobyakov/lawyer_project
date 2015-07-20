# -*- coding: utf-8 -*-

from app import app, db
from models import Category, Type, Contract, User
from forms import AddCategory, AddType, AddContract, SignupForm, SigninForm

from flask import render_template, url_for, flash, redirect, request, session

from webhelpers.text import urlify
from transliterate import translit

@app.route('/')
@app.route('/index')
def index():
	return render_template(
		'index.html',
		title = u'Конструктор договоров онлайн',
		active = 'index')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			user = User(form.username.data, form.password.data, form.email.data)
			db.session.add(user)
			db.session.commit()
			session['email'] = user.email
			return redirect(url_for('profile'))
	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
	form = SigninForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))
                 
	elif request.method == 'GET':
		return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
 	if 'email' not in session:
		return redirect(url_for('signin'))
     
	session.pop('email', None)
	return redirect(url_for('index'))

@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))
	user = User.query.filter_by(email = session['email']).first()
	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')

@app.route('/about')
def about():
	return render_template(
		'about.html',
		title = u'О сервисе',
		active = 'about')

@app.route('/contracts')
def contracts():
	categories = Category.query.all()
	types = Type.query.all()
	contracts = Contract.query.all()
	return render_template(
		'contracts.html',
		title = u'Создать документ',
		active = 'contracts',
		categories = Category.query.all(),
		types = Type.query.all(),
		contracts = Contract.query.all())

@app.route('/addcategory', methods = ['GET', 'POST'])
def addcategory():
	addform = AddCategory()
	if addform.validate_on_submit():
		name = addform.name.data
		slug = urlify(translit(name, 'ru', reversed = True))
		is_contract = addform.is_contract.data
		new_category = Category(
			name=name,
			slug = slug,
			is_contract = is_contract)
		db.session.add(new_category)
		db.session.commit()
		flash('OK')
		return redirect('/index')
	return render_template('addcategory.html',
		title=u'Добавить категорию',
		form = addform)

@app.route('/addtype', methods = ['GET', 'POST'])
def addtype():
	addform = AddType()
	addform.category.choices = [(c.id, c.name) for c in Category.query.all()]
	if addform.validate_on_submit():
		name = addform.name.data
		slug = urlify(translit(name, 'ru', reversed = True))
		is_contract = addform.is_contract.data
		category_id = addform.category.data
		#return '%s %d %d' % (slug, is_contract, category)
		new_type = Type(
			name=name,
			slug = slug,
			category_id = category_id,
			is_contract = is_contract)
		db.session.add(new_type)
		db.session.commit()
		flash('OK')
		return redirect('/index')
	return render_template('addtype.html',
		title = u'Добавить тип',
		form = addform) 

@app.route('/addcontract', methods = ['GET', 'POST'])
def addcontract():
	addform = AddContract()
	addform.type_.choices = [(t.id, t.name) for t in Type.query.all()]
	if addform.validate_on_submit():
		name = addform.name.data
		slug = urlify(translit(name, 'ru', reversed = True))
		is_contract = addform.is_contract.data
		type_id = addform.type_.data
		new_contract = Contract(
			name = name,
			slug = slug,
			type_id = type_id,
			is_contract = is_contract)
		db.session.add(new_contract)
		db.session.commit()
		flash('OK')
		return redirect('/index')
	return render_template('addcontract.html',
		title = u'Добавить документ',
		form = addform) 

@app.route('/kobyakov')
def kobyakov():
	return render_template('kobyakov.html',
		title='kobyakov')