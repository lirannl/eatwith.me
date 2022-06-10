from typing import Optional
import website
from base64 import b32encode
from flask import Blueprint, Response, abort, redirect, request, url_for
from flask import render_template
from flask_login import login_required, login_user, logout_user, current_user
from . import db

from website.forms import MealForm, RegisterForm
from .models import Event, User


bp = Blueprint('website', __name__)


@bp.route('/')
def index():
    return render_template('base.html')


@bp.route("/book_event")
@login_required
def book_event():
    form_data = request.form
    user: User = None  # Code for figuring out which user you're logged in as here
    event: Event = Event.query.where(
        Event.id == b32encode(form_data["id"].encode())).first()
    if (event.hostId == user.id):
        return 403  # However you return a 403 response because you can't book your own event
    event.attendees.append([user] * form_data.count)
    return render_template

# Connecting create event
@bp.route("/create_event", methods = ['GET', 'POST'])
def create_event():
    form_data = request.form
    form = MealForm()
    #if form.validatae_on_submit():
        #print('Successfully created new meal')
    return render_template('event/create.html', form=MealForm())

#   user: User = None
@bp.route('/<id>')
def show(id):
    website = website.query.get(id=id).first()
    # create the comment form
    # cform = CommentForm()
    return render_template('event/index.html', event=event)


@bp.route('/new-event', methods=['GET', 'POST'])
def create():
    print('Method types', request.method)
    return redirect(url_for('models.create'))
    return render_template('models/create.html')


@bp.route('/<my_event>/comments', methods=['GET', 'POST'])
def comment(id):
    form = CommentForm()
    event_obj = website.query.get(id=id).first()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          website=event_obj, user=User)
        db.session.add(comment)
        db.session.commit()

        print('Comment added', 'success')

        return redirect(url_for('models.show', id=event_obj.id))
    return render_template('website/show.html', website=event_obj, form=form)
