from base64 import b32encode
from flask import Blueprint, redirect, request
from flask import render_template
from sqlalchemy.orm import Session
from .models import Event, User
from . import bp


@bp.route('/')
def index():
    return render_template('base.html')

# Booking an event code


@bp.route("/book_event")
def book_event():
    form_data = request.form
    user: User = None  # Code for figuring out which user you're logged in as here
    event: Event = Event.query.where(
        Event.id == b32encode(form_data["id"])).first()
    if (event.hostId == user.id):
        return 403  # However you return a 403 response because you can't book your own event
    event.attendees.append([user] * form_data.count)
    return redirect("Where?")

# Connecting create event


@bp.route("/create_event")
def create_event():
    form_data = request.form
#     user: User = None
