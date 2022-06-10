from base64 import b32encode
from flask import Blueprint, redirect, request, url_for
from flask import render_template
from sqlalchemy.orm import Session
from .models import Comment, Event, User
from . import bp, db
#from .forms import LoginForm, RegisterForm, CommentForm, MealForm, BookForm
#from auth import login_required

import website

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

@bp.route('/<id>')
def show(id):
    website = website.query.get(id=id).first()
    # create the comment form
    cform = CommentForm()
    return render_template('website/show.html', website=website, cform=cform)


@bp.route('/new-event', methods = ['GET', 'POST'])
def create():
        print('Method types', request.method)
        return redirect(url_for('models.create'))
        return render_template('models/create.html')

        @bp.route('/<my_event>/comments', methods = ['GET', 'POST'])
        @login_required
        def comment (id):
            form = CommentForm()
            event_obj = website.query.get(id=id).first()
            if form.validate_on_submit():
                comment = Comment(body=form.body.data, website=event_obj,user=User)
                db.session.add(comment)
                db.session.commit()
            
                print('Comment added','success')

                return redirect(url_for('models.show', id=event_obj.id))
            return render_template('website/show.html', website=event_obj, form=form)