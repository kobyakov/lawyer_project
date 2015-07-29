from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
category = Table('category', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=128)),
    Column('slug', VARCHAR(length=128)),
    Column('is_contract', BOOLEAN),
)

contract = Table('contract', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('type_id', INTEGER),
    Column('name', VARCHAR(length=128)),
    Column('slug', VARCHAR(length=128)),
    Column('is_contract', BOOLEAN),
    Column('contract_template', VARCHAR(length=128)),
)

type = Table('type', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('category_id', INTEGER),
    Column('name', VARCHAR(length=128)),
    Column('slug', VARCHAR(length=128)),
    Column('is_contract', BOOLEAN),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=40)),
    Column('password_hash', VARCHAR(length=40)),
    Column('email', VARCHAR(length=60)),
    Column('registered_on', DATETIME),
)

categories = Table('categories', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('slug', String(length=128)),
    Column('is_contract', Boolean, default=ColumnDefault(False)),
)

contracts = Table('contracts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type_id', Integer),
    Column('name', String(length=128)),
    Column('slug', String(length=128)),
    Column('is_contract', Boolean, default=ColumnDefault(True)),
    Column('contract_template', String(length=128)),
)

types = Table('types', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('category_id', Integer),
    Column('name', String(length=128)),
    Column('slug', String(length=128)),
    Column('is_contract', Boolean, default=ColumnDefault(False)),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=60)),
    Column('password', String(length=40)),
    Column('authenticated', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['category'].drop()
    pre_meta.tables['contract'].drop()
    pre_meta.tables['type'].drop()
    pre_meta.tables['user'].drop()
    post_meta.tables['categories'].create()
    post_meta.tables['contracts'].create()
    post_meta.tables['types'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['category'].create()
    pre_meta.tables['contract'].create()
    pre_meta.tables['type'].create()
    pre_meta.tables['user'].create()
    post_meta.tables['categories'].drop()
    post_meta.tables['contracts'].drop()
    post_meta.tables['types'].drop()
    post_meta.tables['users'].drop()
