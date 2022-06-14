from datetime import datetime
from hashlib import sha256
from random import Random
import random
from flask_login import UserMixin
from typing import Optional
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: bytes = db.Column(db.BLOB(16), primary_key=True,
                          default=Random().randbytes(16))
    username: str = db.Column(
        db.String(256), index=True, unique=True)
    salt: bytes = db.Column(db.BLOB(16))
    password_hash: bytes = db.Column(db.BLOB(16))
    contact_number: str = db.Column(db.String(256), unique=True)
    name: str = db.Column(db.String(256))
    # events: list = db.relationship('Event',
    #                             secondary='attendees',
    #                             backref='attendees', lazy='dynamic')

    def set_password(self, password: str):
        self.salt = Random().randbytes(64)
        self.password_hash = sha256(
            self.salt + password.encode('utf-8')).digest()

    def check_password(self, password: str):
        return self.password_hash == sha256(self.salt + password.encode('utf-8')).digest()

    def __init__(self, username: str, name: str, contact_number: Optional[str]):
        self.username = username
        self.contact_number = contact_number
        self.name = name


class Cuisine(db.Model):
    __tablename__ = 'cuisines'
    id: bytes = db.Column(db.BLOB(16), primary_key=True,
                          default=Random().randbytes(16))
    name: str = db.Column(db.String(256), index=True,
                          unique=True)
    # events: list = db.relationship('Event', backref='cuisine', lazy='dynamic')

#Book class
class Book(db.Model):
    __tablename__ = 'book'
    id: bytes = db.Column(db.BLOB(16), primary_key=True,
                          default=Random().randbytes(16))
    name: str = db.Column(db.String(256), index=True,
                          unique=True)
    ticket: int = db.Column(db.Integer)                      

class Attribute(db.Model):
    __tablename__ = 'attributes'
    id: bytes = db.Column(db.BLOB(16), primary_key=True,
                          default=Random().randbytes(16))
    name: str = db.Column(db.String(256), index=True,
                          unique=True)
    # events: list = db.relationship(
    #     'Event', backref='attribute', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comments'
    id: bytes = db.Column(db.BLOB(16), primary_key=True,
                          default=Random().randbytes(16))
    eventId: bytes = db.Column(db.BLOB(16), db.ForeignKey('events.id'))
    # event = db.relationship('Event', backref='comments', lazy='dynamic')
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String(16384))
    commenterId = db.Column(db.BLOB(16), db.ForeignKey('users.id'))
    # commenter = db.relationship('User', backref='comments', lazy='dynamic')


class Event(db.Model):
    __tablename__ = 'events'
    id: bytes = db.Column(db.BLOB(16), primary_key=True,
                          default=Random().randbytes(16))
    cuisineId: bytes = db.Column(db.BLOB(16), db.ForeignKey('cuisines.id'))
    cuisine: Cuisine = db.relationship(
        'Cuisine', backref='events')
    hostId: bytes = db.Column(db.BLOB(16), db.ForeignKey('users.id'))
    # host: User = db.relationship(
    #     'User', backref=backref('events', lazy='dynamic'))
    attendees: list[User] = db.relationship('User',
                                            secondary='attendees',
                                            backref='events', lazy='dynamic')
    #book: Book = db.relationship('Book', backref='events') this line is messing up the code
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
            return "Inactive"
    status: str = property(get_status)
    ticket_price: float = db.Column(db.Numeric(precision=10, scale=2))
    address: str = db.Column(db.String(2048))
    coarse_location: str = db.Column(db.String(256))
    description: str = db.Column(db.String(2048))
    capacity: int = db.Column(db.Integer)
    image: bytes = db.Column(db.BLOB(1024 * 1024 * 10))
    time: datetime = db.Column(db.DateTime)
    avaliable_tickets: int = db.Column(db.Integer)
    # attributes: list[Attribute] = db.relationship('Attribute',
    #                                               secondary='event_attributes',
    #                                               backref='events', lazy='dynamic')
    isActive: bool = db.Column(db.Boolean, default=True)
    comments: list[Comment] = db.relationship('Comment',
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
#                             db.metadata,
#                             db.Column('eventId', db.BLOB(16),
#                                       db.ForeignKey('events.id')),
#                             db.Column('attributeId', db.BLOB(16),
#                                       db.ForeignKey('attributes.id'))
#                             )
attendees = db.Table('attendees', db.metadata,
                     db.Column('id', db.BLOB(16), primary_key=True,
                               default=Random().randbytes(16)),
                     db.Column('eventId', db.BLOB(16),
                               db.ForeignKey('events.id')),
                     db.Column('userId', db.BLOB(16),
                               db.ForeignKey('users.id'))
                     )
