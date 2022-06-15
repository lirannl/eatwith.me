from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Comment, Cuisine, Event, User
from .forms import MealForm, RegisterForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from website.helpers import get_cuisine, id_to_string, string_to_id
from typing import Optional

bp = Blueprint('meal', __name__, url_prefix='/meal', template_folder='/meal')

# Stroing the db information once user creates a meal


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if (request.method != 'POST'):
        return render_template('event/create.html', form=MealForm())
    time: datetime = datetime.fromisoformat(request.form["time"])
    address: str = request.form["address"]
    coarse_location: str = request.form["coarse_location"]
    description: str = request.form["description"]
    capacity = int(request.form["capacity"])
    cuisine = get_cuisine(request.form["cuisine"])
    ticket_price = int(request.form["ticket_price"])
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


# 1. There should be a page showing all the event and for each 'view detail' it redirect to a page with the end point of event id /<event_id>
# 2. When user click on update button the event id should be passed into the 'update' end point where we just have to find the event with the matching eventid that we passeed in, and update it using mealform

# @bp.route('/detail/<id>', methods=['GET', 'POST'])
# @login_required
# def create():
#   print('Method type: ', request.method)
#   form = MealForm()
#   if form.validate_on_submit():
#     print('place holder')
#       # get event id from detail endpoint
#       #need to find the match inside of the database inorder to update

#   return render_template('event/detail.html', form=form)

# #adding update login
# @bp.route('/update', methods=['GET', 'POST'])
# @login_required
# def create():
#   print('Method type: ', request.method)
#   form = MealForm()
#   if form.validate_on_submit():
#     print('place holder')
#       # get event id from detail endpoint
#       #need to find the match inside of the database inorder to update

#   return render_template('event/update.html', form=form)

# adding the check upload file form


def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static\\image', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '\\static\\image\\' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

# adding the Comment Form


@bp.route('<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id: str):
    form = CommentForm()
    event_obj: Optional[Event] = Event.query.get(string_to_id(id))
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          website=event_obj, user=User)
        db.session.add(comment)
        db.session.commit()

        print('Comment added', 'success')

        return redirect(url_for('meal.event', id=id_to_string(event_obj.id)))
    return render_template('event/event.html', website=event_obj, form=form)


@bp.route('/<id>')
def show(id: str):
    event = Event.query.get(string_to_id(id))
    comments = Comment.query.all()
    return render_template("event/index.html", event=event, comments=comments)
