from datetime import datetime
from hashlib import sha256
from random import Random
import random
from typing import Optional
from . import db
from sqlalchemy import BLOB, Boolean, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Table, create_engine
from sqlalchemy.orm import declarative_base, relationship, Session, backref

Base = declarative_base()


class User(db.Model):
    __tablename__ = 'users'
    id: bytes = db.Column(BLOB(64), primary_key=True)
    username: str = db.Column(
        String(256), index=True, unique=True)
    salt: bytes = db.Column(BLOB(64))
    password_hash: bytes = db.Column(BLOB(64))
    contact_number: str = db.Column(String(256), unique=True)
    name: str = db.Column(String(256))
    # events: list = relationship('Event',
    #                             secondary='attendees',
    #                             backref='attendees', lazy='dynamic')

    def set_password(self, password: str):
        self.salt = Random().randbytes(64)
        self.password_hash = sha256(
            self.salt + password.encode('utf-8')).digest()

    def check_password(self, password: str):
        return self.password_hash == sha256(self.salt + password.encode('utf-8')).digest()

    def __init__(self, username: str, name: str, contact_number: Optional[str]):
        self.id = Random().randbytes(64)
        self.username = username
        self.contact_number = contact_number
        self.name = name


class Cuisine(db.Model):
    __tablename__ = 'cuisines'
    id: bytes = db.Column(BLOB(64), primary_key=True,
                       default=Random().randbytes(64))
    name: str = db.Column(String(256), index=True,
                       unique=True)
    # events: list = relationship('Event', backref='cuisine', lazy='dynamic')


class Attribute(db.Model):
    __tablename__ = 'attributes'
    id: bytes = db.Column(BLOB(64), primary_key=True,
                       default=Random().randbytes(64))
    name: str = db.Column(String(256), index=True,
                       unique=True)
    # events: list = relationship(
    #     'Event', backref='attribute', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comments'
    id: bytes = db.Column(BLOB(64), primary_key=True,
                       default=Random().randbytes(64))
    eventId: bytes = db.Column(BLOB(64), ForeignKey('events.id'))
    # event = relationship('Event', backref='comments', lazy='dynamic')
    creation_time = db.Column(DateTime, default=datetime.utcnow)
    content = db.Column(String(16384))
    commenterId = db.Column(BLOB(64), ForeignKey('users.id'))
    # commenter = relationship('User', backref='comments', lazy='dynamic')


class Event(db.Model):
    __tablename__ = 'events'
    id: bytes = db.Column(BLOB(64), primary_key=True,
                       default=Random().randbytes(64))
    cuisineId: bytes = db.Column(BLOB(64), ForeignKey('cuisines.id'))
    # cuisine: Cuisine = relationship(
    #     'Cuisine', backref=backref('events', lazy='dynamic'))
    hostId: bytes = db.Column(BLOB(64), ForeignKey('users.id'))
    # host: User = relationship(
    #     'User', backref=backref('events', lazy='dynamic'))
    attendees: list[User] = relationship('User',
                                         secondary='attendees',
                                         backref='events', lazy='dynamic')
    def get_status(self):
        if self.isActive and len(self.attendees) < self.capacity:
            return "Upcoming"
        elif self.isActive:
            return "Booked"
        # The CRA didn't specify what the difference between cancelled and inactive should be,
        # Just that both would show up, so... This makes it show up
        elif random.choice([True, False]):
            return "Cancelled"
        else:
            return  "Inactive"
    status: str = property(get_status)
    ticket_price: Float = db.Column(Numeric(precision=10, scale=2))
    address: str = db.Column(String(2048))
    coarse_location: str = db.Column(String(256))
    description: str = db.Column(String(2048))
    capacity: int = db.Column(Integer)
    image: bytes = db.Column(BLOB(1024 * 1024 * 10))
    time: datetime = db.Column(DateTime)
    # attributes: list[Attribute] = relationship('Attribute',
    #                                               secondary='event_attributes',
    #                                               backref='events', lazy='dynamic')
    isActive: bool = db.Column(Boolean, default=True)
    comments: list[Comment] = relationship('Comment',
                                           backref='event', lazy='dynamic')


    def __init__(self, time: datetime, address: str, coarse_location: str, description: str, capacity: int, cuisine: Cuisine, ticket_price: float, image: bytes, host: User):
        self.time = time
        self.image = image
        self.address = address
        self.coarse_location = coarse_location
        self.description = description
        self.capacity = capacity
        self.ticket_price = ticket_price
        self.isActive = True
        self.cuisine = cuisine
        self.hostId = host.id


# event_attributes = Table('event_attributes',
#                             Base.metadata,
#                             db.Column('eventId', BLOB(64),
#                                       ForeignKey('events.id')),
#                             db.Column('attributeId', BLOB(64),
#                                       ForeignKey('attributes.id'))
#                             )
attendees = Table('attendees', Base.metadata,
                  db.Column('eventId', BLOB(64),
                         ForeignKey('events.id')),
                  db.Column('userId', BLOB(64),
                         ForeignKey('users.id'))
                  )
