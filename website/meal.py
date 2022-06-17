import base64
from crypt import methods
from datetime import datetime
from random import Random
from re import T
from flask import Blueprint, abort, render_template, request, redirect, url_for
from .models import Comment, Cuisine, Event, User
from .forms import MealForm, RegisterForm, CommentForm, DelForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from website.helpers import b64, get_cuisine, id_to_string, string_to_id
from typing import Optional
from wtforms.validators import InputRequired
from flask_wtf.file import FileRequired

bp = Blueprint('meal', __name__, url_prefix='/meal', template_folder='/meal')

# Stroing the db information once user creates a meal


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if (request.method != 'POST'):
        form = MealForm()
        form.time.validators.extend([InputRequired()])
        form.image.validators.extend([
            FileRequired(message='Image cannot be empty')])
        return render_template('event/create.html', form=form, cuisines=Cuisine.query.all())
    time: datetime = datetime.fromisoformat(request.form["time"])
    address: str = request.form["address"]
    coarse_location: str = request.form["coarse_location"]
    description: str = request.form["description"]
    capacity = int(request.form["capacity"])
    cuisine = get_cuisine(request.form["cuisine"])
    ticket_price = float(request.form["ticket_price"])
    image = request.files["image"]
    host: User = current_user
    event = Event(
        time, address, coarse_location,
        description, capacity, cuisine,
        ticket_price, image.stream.read(), host
    )
    db.session.add(event)
    db.session.commit()
    return redirect(f"/meal/{id_to_string(event.id)}")


@bp.route('<id>/update', methods=['GET', 'POST'])
@login_required
def update(id: str):
    if (request.method != 'POST'):
        event: Event = Event.query.get(string_to_id(id))
        form = MealForm()
        form.populate_obj(event)
        return render_template('event/create.html', form=form, event=event, cuisines=Cuisine.query.all())
    try:
        time: Optional[datetime] = datetime.fromisoformat(request.form["time"])
    except ValueError:
        time = None
    address: str = request.form["address"]
    coarse_location: str = request.form["coarse_location"]
    description: str = request.form["description"]
    capacity = int(request.form["capacity"])
    cuisine = get_cuisine(request.form["cuisine"])
    ticket_price = float(request.form["ticket_price"])
    image = request.files["image"]
    host: User = current_user
    event = Event.query.get(string_to_id(id))
    if time is not None:
        event.time = time
    event.address = address
    event.coarse_location = coarse_location
    event.description = description
    event.capacity = capacity
    event.cuisine = cuisine
    event.ticket_price = ticket_price
    if image.filename != '' :
        event.image = image.stream.read()
    event.host = host
    db.session.commit()
    return redirect(f"/meal/{id}")


@bp.route('/delmeal', methods=['GET', 'POST'])
@login_required
def delmeal():
    print('Method type: ', request.method)
    form = DelForm()
    if form.validate_on_submit():

        delevent = Event.query.where(Event.description ==
                                     request.form['name'].lower()).first()
        if delevent is not None:
            pass
           # drop the row
           # db.session.add(eal)

        # add the object to the db session

        # commit to the database
        # db.session.commit()
        print('Successfully deleted meal')
        # Always end with redirect when form is valid
        return redirect(url_for('meal.delet'))
    return render_template('event/delmeal.html', form=form)
# 1. There should be a page showing all the event and for each 'view detail' it redirect to a page with the end point of event id /<event_id>
# 2. When user click on update button the event id should be passed into the 'update' end point where we just have to find the event with the matching eventid that we passeed in, and update it using mealform


def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static\\img', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '\\static\\img\\' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

# adding the Comment Form


# @bp.route('<id>/comment', methods=['GET', 'POST'])
# @login_required
# def comment(id: str):
#     form = CommentForm()
#     event_obj: Optional[Event] = Event.query.get(string_to_id(id))
#     if form.validate_on_submit():
#         comment = Comment(website=event_obj, user=User)
#         db.session.add(comment)
#         db.session.commit()

#         print('Comment added', 'success')

#         return redirect(url_for('meal.event', id=id_to_string(event_obj.id)))
#     return render_template('event/event.html', website=event_obj, form=form)

@bp.route('/<id>/book', methods=["POST"])
def book(id: str):
    event: Event = Event.query.get(string_to_id(id))
    amount: int = int(request.form["amount"])
    if event is None:
        return abort(404)
    if (event.capacity - event.attendees.count()) < amount:
        return abort(400)
    for i in range(amount):
        event.attendees.extend([current_user])
        db.session.commit()
    return redirect(request.referrer)


@bp.route('<id>/cancel', methods=["POST"])
def cancel(id: str):
    event: Event = Event.query.get(string_to_id(id))
    if event is None:
        return abort(404)
    event.isActive = False
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/<id>', methods=["GET", "POST"])
def show(id: str):
    event: Event = Event.query.get(string_to_id(id))
    if event is None:
        return abort(404)
    if (request.method == "POST"):
        comment = Comment(request.form["comment"],
                          current_user, event)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('meal.show', id=id))
    return render_template("event/index.html", event=event, form=CommentForm(), b64=b64, id_to_string=id_to_string)
