# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class AddForm(Form):
	name = TextField('name', validators = [Required()])

