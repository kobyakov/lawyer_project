# -*- coding: utf-8 -*-

from app import app, db, login_manager
from models import Category, Type, Contract, User
from forms import AddCategory, AddType, AddContract, RegisterForm, LoginForm

from flask import render_template, url_for, flash, redirect, request, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from webhelpers.text import urlify
from transliterate import translit

@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(user_id)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
	return render_template(
		'index.html',
		title = u'Конструктор договоров онлайн',
		active = 'index')

@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		#if User.query.filter_by(email = self.email.data.lower()).first():
		#	form.email.errors.append("That email is already taken")
		#	return False
		user = User(form.email.data, form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('User successfully registered')
		return redirect(url_for('index'))
	else:
		return render_template('register.html', form=form)
		
	#if request.method == 'POST':
	#	if form.validate() == False:
	#		return render_template('signup.html', form=form)
	#	else:
	#		user = User(form.username.data, form.password.data, form.email.data)
	#		db.session.add(user)
	#		db.session.commit()
	#		session['email'] = user.email
	#		return redirect(url_for('profile'))
	#elif request.method == 'GET':
	#	return render_template('signup.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data.lower()).first()
		if user:
			if user.check_password(form.password.data):
				login_user(user, remember = True)
				return redirect(url_for("index"))
			else:
				form.email.password.append("Password is not valid")
		else:
			form.email.errors.append("This user is not exists")
		return render_template('login.html', form=form)
	else:
		return render_template('login.html', form=form)
	#if request.method == 'POST':
	#	if form.validate() == False:
	#		return render_template('signin.html', form=form)
	#	else:
	#		session['email'] = form.email.data
	#		return redirect(url_for('profile'))
    #             
	#elif request.method == 'GET':
	#	return render_template('signin.html', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))
 	#if 'email' not in session:
	#	return redirect(url_for('signin'))
    # 
	#session.pop('email', None)
	#return redirect(url_for('index'))

#@app.route('/profile')
#@login_required
#def profile():
#	if '' not in session:
#		return redirect(url_for('signin'))
#	user = User.query.filter_by(email = session['email']).first()
#	if user is None:
#		return redirect(url_for('signin'))
#	else:
#		return render_template('profile.html')

@app.route('/about')
def about():
	return render_template(
		'about.html',
		title = u'О сервисе',
		active = 'about')

@app.route('/contracts')
@app.route('/contracts/<_category>')
@app.route('/contracts/<_category>/<_type>')
@app.route('/contracts/<_category>/<_type>/<_contract>')
def contracts(_category=None, _type=None, _contract=None):
	if not _category and not _type and not _contract:
		categories = Category.query.all()	
		return render_template(
			'contracts.html',
			title = u'Создать документ',
			active = 'contracts',
			categories = Category.query.all())
	if _category and not _type and not _contract:
		types = Type.query.\
			filter(Type.category_id==Category.id).\
			filter(Category.slug==_category)
		return render_template(
			'contracts.html',
			title = u'Создать документ',
			active = 'contracts',
			_category = _category,
			types = types)
	if _category and _type and not _contract:
		contracts = Contract.query.\
			filter(Contract.type_id==Type.id).\
			filter(Type.slug==_type)
		return render_template(
			'contracts.html',
			title = u'Создать документ',
			active = 'contracts',
			_category = _category,
			_type = _type,
			contracts = contracts)
	if _category and _type and _contract:
		return('OK')

@app.route('/addcategory', methods = ['GET', 'POST'])
@login_required
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
		return redirect('/addcategory')
	return render_template('addcategory.html',
		title=u'Добавить категорию',
		form = addform)

@app.route('/addtype', methods = ['GET', 'POST'])
@login_required
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
		return redirect('/addtype')
	return render_template('addtype.html',
		title = u'Добавить тип',
		form = addform) 

@app.route('/addcontract', methods = ['GET', 'POST'])
@login_required
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
		return redirect('/addcontract')
	return render_template('addcontract.html',
		title = u'Добавить документ',
		form = addform) 

@app.route('/kobyakov')
def kobyakov():
	return render_template('kobyakov.html',
		title='kobyakov')