# -*- coding: utf-8 -*-

import os
import config

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, Permission, RoleNeed

from werkzeug.debug import DebuggedApplication
	
app = Flask(__name__)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.config.from_object('config')


######## DB PARAMS ###################
db = SQLAlchemy(app)

######## LOGIN MANAGER ###############
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

######## PRINCIPAL ############
principals = Principal(app)
be_admin = RoleNeed('admin')
admin_permission = Permission(be_admin)


from app import views, models