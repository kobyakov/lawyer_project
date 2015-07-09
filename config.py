import os
basedir = os.path.abspath(os.path.dirname(__file__))

# forms parameters
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess' 

# database parameters
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')