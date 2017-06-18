# -*- coding: utf-8 -*-

from app import app, db, login_manager, principals, admin_permission, be_admin
from models import Category, Type, Contract, User, ROLE_ADMIN, ROLE_USER
from forms import AddCategory, AddType, AddContract, RegisterForm, LoginForm

from flask import render_template,  render_template_string, send_from_directory, make_response, url_for, flash, redirect, request, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_loaded, identity_changed

from webhelpers.text import urlify
from transliterate import translit
from bs4 import BeautifulSoup

import os
import re
import html2text

@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(user_id)

@app.before_request
def before_request():
    g.user = current_user

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
	needs = []
	if identity.id in ('admin'):
		needs.append(be_admin)
	for n in needs:
		identity.provides.add(n)

@app.errorhandler(403)
def authorisation_failed(e):
    return ('Authorisation_failed')

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
				if user.role == ROLE_ADMIN:
					identity = Identity(ROLE_ADMIN)
					identity_changed.send(app, identity=identity)
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
	for key in ['identity.id', 'identity.auth_type']:
		session.pop(key, None)
	#identity_changed.send(app, identity=AnonymousIdentity())
	return redirect(url_for('index'))
 	#if 'email' not in session:
	#	return redirect(url_for('signin'))
    # 
	#session.pop('email', None)
	#return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
	user = User.query.filter_by(email = g.user.email).first()
	if user is None:
		return redirect(url_for('login'))
	else:
		return render_template('profile.html', user=user)

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
		contract = Contract.query.filter(Contract.slug==_contract).first()
		return render_template(
			'editor.html',
			title = u'Редактировать документ',
			active = 'contracts',
			contract_template = contract.contract_template,)

@app.route('/editor')
def editor():
	return render_template(
		'editor.html',
		title = u'Редактировать документ',
		active = 'contracts',)

@app.route('/save', methods = ['GET', 'POST'])
def saver():
	document = request.form['body']
	html = render_template('pdf.html', document=document)



	upload_dir = app.config['UPLOAD_FOLDER']
	filename = "doc.txt"

	result_html = html2text.html2text(html)
	doc = open(os.path.join(upload_dir, filename), 'w')
	doc.write(result_html.encode('utf-8'))
	doc.close()

	doc = open(os.path.join(upload_dir, filename), 'r')
	html = doc.read()
	doc.close()

	result_html = html2text.html2text(html.decode('utf-8'))
	doc = open(os.path.join(upload_dir, filename), 'w')
	doc.write(result_html.encode('utf-8'))
	doc.close()


	return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)	


@app.route('/download', methods = ['GET', 'POST'])
def download():
	response = make_response("test")
	response.headers["Content-Disposition"] = "attachment; filename=books.csv"
	response.headers["Content-Type"] = "text/html; charset=utf-8"
	return response


@app.route('/manage')
@login_required
@admin_permission.require(http_exception=403)
def manage():
	return render_template('manage.html')


@app.route('/manage/addcategory', methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
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
		active='addcat',
		form = addform)

@app.route('/addtype', methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
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
		active = 'addtyp',
		form = addform) 

@app.route('/addcontract', methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
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
		active = 'addcon',
		form = addform) 

@app.route('/save_contract')
def save_contract():
	filename = 'test.txt'
	return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)	

@app.route('/kobyakov')
def kobyakov():
	return render_template('kobyakov.html',
		title='kobyakov')