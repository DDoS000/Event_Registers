from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Sequence

metadata = MetaData()

users = Table(
    'my_users', metadata,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('email', String(100)),
    Column('password', String(100)),
    Column('fullname', String(50)),
    Column('created_on', DateTime),
    Column('status', String(1)),
)

codes = Table(
    'my_codes', metadata,
    Column('id', Integer, Sequence('code_id_seq'), primary_key=True),
    Column('email', String(100)),
    Column('reset_code', String(50)),
    Column('status', String(1)),
    Column('exprired_in', DateTime)
)

blacklists = Table(
    'my_blacklists', metadata,
    Column('token', String(250), unique=True),
    Column('email', String(100)),
)

events = Table(
    'my_events', metadata,
    Column('id', Integer, Sequence('event_id_seq'), primary_key=True),
    Column('name', String(100)),
    Column('description', String(250)),
    Column('location', String(100)),
    Column('start_date', DateTime),
    Column('end_date', DateTime),
    Column('created_by', Integer),
    Column('created_on', DateTime),
    Column('status', String(1)),
    Column('image', String(250)),
)

events_register = Table(
    'my_events_register', metadata,
    Column('id', Integer, Sequence('events_register_id_seq'), primary_key=True),
    Column('events_id', Integer),
    Column('code', String(150)),
    Column('token', String(150)),
    Column('status', String(1)),
)


