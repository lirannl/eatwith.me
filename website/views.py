#from asyncio import new_event_loop
#from crypt import methods
#from http.client import PAYMENT_REQUIRED
from typing import Optional
import website
from base64 import b32encode
from flask import Blueprint, Response, abort, redirect, request, url_for
from flask import render_template
from flask_login import login_required, current_user

from website.helpers import id_to_string, string_to_id
from . import db

from website.forms import MealForm, RegisterForm
from .models import Comment, Event, User

#login_required = Blueprint('login_required', __name__)

bp = Blueprint('website', __name__)
#bp = Blueprint('views', __name__)
#bp = Blueprint('auth', __name__)
#bp = Blueprint('event', __name__)


@bp.route('/')
def index():
    return render_template('base.html')

# @bp.route('/')
# def index():
    #events = Event.query.all()
    #book_event = Event.query.filter_by(id=1).first()
    #new_event_loop = new_event_loop.run_until_complete(book_event.book())
    # return render_template('my-events.html', events=events)


@bp.route("/book_event")
@login_required
def book_event():
    form_data = request.form
    user: User = current_user  # Example - how to figure out the user
    event: Event = Event.query.where(
        Event.id == b32encode(form_data["id"].encode())).first()
    if (event.hostId == user.id):
        # However you return a 403 response because you can't book your own event
        return abort(403)
    event.attendees.append([user] * form_data.count)
    return render_template

# Connecting create event


#   user: User = None


@bp.route('/event/<id>')
def show(id: str):
    event: Optional[Event] = Event.query.get(id=string_to_id(id))
    if (event is None):
        return abort(404)
    # create the comment form
    # cform = CommentForm()
    return render_template('event/index.html', event=event)


@bp.route('/new-event', methods=['GET', 'POST'])
def create():
    print('Method types', request.method)
    return redirect(url_for('models.create'))
    return render_template('models/create.html')


#@bp.route('/event/<id>/comments', methods=['GET', 'POST'])
#@login_required
#def comment(id: str):
#    form = CommentForm()
#    event_obj: Optional[Event] = Event.query.get(string_to_id(id))
#    if form.validate_on_submit():
#        comment = Comment(body=form.body.data,
#                          website=event_obj, user=User)
#        db.session.add(comment)
#        db.session.commit()

#        print('Comment added', 'success')

#        return redirect(url_for('models.event', id=id_to_string(event_obj.id)))

#    return render_template('models.event.html', website=event_obj, form=form)

# Route for Event Page


@bp.route('/event/<id>', methods=['GET', 'POST'])
def event(id: str):
    event: Event = Event.query.get(string_to_id(id))
    register = RegisterForm()
    MealForm = MealForm()
    PAYMENT_REQUIRED = 403
    return render_template('event/event.html', event=event, register=register, MealForm=MealForm, PAYMENT_REQUIRED=PAYMENT_REQUIRED)
