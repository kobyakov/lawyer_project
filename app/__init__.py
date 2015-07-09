# -*- coding: utf-8 -*-

import os
import config

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from werkzeug.debug import DebuggedApplication
	
app = Flask(__name__)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import views, models