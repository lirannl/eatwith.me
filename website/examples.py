from datetime import datetime
from typing import Optional

from website.helpers import string_to_id
from .models import Event, User, Cuisine
from . import db

# These are simply examples and should not be imported


def get_cuisine(name: str):
    cuisine = Cuisine.query.filter_by(name=name).first()
    if cuisine is None:
        db.session.add(Cuisine(name=name))
        db.session.commit()
        cuisine = Cuisine.query.filter_by(name=name).first()
    return cuisine


def create_event():
    new_event = Event(description='Homemade prosciutto and red wine',
                      ticket_price=16.0,
                      capacity=8,
                      time=datetime.now(),
                      address='69 Funny st, Fairield',
                      coarse_location='Fairfield',
                      image=bytes(),
                      host=User.query.filter_by(name="Chris").first(),
                      cuisine=get_cuisine("Italian"))


def get_event(id: str):
    event: Optional[Event] = Event.query.get(string_to_id(id))
    return event
