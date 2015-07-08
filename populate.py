#!flask/bin/python
# -*- coding: utf-8 -*-

from app import db, models
c = models.Category(name="Купли-продажи".decode('utf8'))
db.session.add(c)
db.session.commit()