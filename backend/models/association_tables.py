from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

event_administrators_table = Table(
    'event_administrators',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True)
)