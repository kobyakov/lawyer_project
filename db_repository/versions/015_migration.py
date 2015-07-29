from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
categories = Table('categories', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=128)),
    Column('slug', VARCHAR(length=128)),
    Column('is_contract', BOOLEAN),
)

contracts = Table('contracts', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('type_id', INTEGER),
    Column('name', VARCHAR(length=128)),
    Column('slug', VARCHAR(length=128)),
    Column('is_contract', BOOLEAN),
    Column('contract_template', VARCHAR(length=128)),
)

types = Table('types', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('category_id', INTEGER),
    Column('name', VARCHAR(length=128)),
    Column('slug', VARCHAR(length=128)),
    Column('is_contract', BOOLEAN),
)

users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=60)),
    Column('password', VARCHAR(length=40)),
    Column('authenticated', BOOLEAN),
)

category = Table('category', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('slug', String(length=128)),
    Column('is_contract', Boolean, default=ColumnDefault(False)),
)

contract = Table('contract', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type_id', Integer),
    Column('name', String(length=128)),
    Column('slug', String(length=128)),
    Column('is_contract', Boolean, default=ColumnDefault(True)),
    Column('contract_template', String(length=128)),
)

type = Table('type', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('category_id', Integer),
    Column('name', String(length=128)),
    Column('slug', String(length=128)),
    Column('is_contract', Boolean, default=ColumnDefault(False)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=60)),
    Column('password', String(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['categories'].drop()
    pre_meta.tables['contracts'].drop()
    pre_meta.tables['types'].drop()
    pre_meta.tables['users'].drop()
    post_meta.tables['category'].create()
    post_meta.tables['contract'].create()
    post_meta.tables['type'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['categories'].create()
    pre_meta.tables['contracts'].create()
    pre_meta.tables['types'].create()
    pre_meta.tables['users'].create()
    post_meta.tables['category'].drop()
    post_meta.tables['contract'].drop()
    post_meta.tables['type'].drop()
    post_meta.tables['user'].drop()
