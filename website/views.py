from asyncio import new_event_loop
from crypt import methods
from http.client import PAYMENT_REQUIRED
from typing import Optional
import website
from base64 import b32encode
from flask import Blueprint, redirect, request, url_for
from flask import render_template
from . import forms, CommentForm, db 


from website.forms import MealForm, RegisterForm
from .models import Comment, Event, User

login_required = Blueprint('login_required', __name__)


bp = Blueprint('views', __name__)
bp = Blueprint('auth', __name__)
bp = Blueprint('event', __name__)


@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/')
def index():
    events = Event.query.all()
    book_event = Event.query.filter_by(id=1).first()
    new_event_loop = new_event_loop.run_until_complete(book_event.book())
    return render_template('my-events.html', events=events)

@bp.route('/login', methods=["POST"])
def login():
    username = request.values["username"]
    password = request.values["password"]
    user: Optional[User] = User.query.where(User.username == username).first()
    return redirect(request.referrer)

# Booking an event code
@bp.route("/register", methods=["GET","POST"])
def register():
    return render_template("register.html", form=RegisterForm())

@bp.route("/book_event")
def book_event():
    form_data = request.form
    user: User = None  # Code for figuring out which user you're logged in as here
    event: Event = Event.query.where(
        Event.id == b32encode(form_data["id"])).first()
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
    cform = CommentForm()
    return render_template('website/show.html', website=website, cform=cform)


@bp.route('/new-event', methods=['GET', 'POST'])
def create():
    print('Method types', request.method)
    if request.method == 'POST':
        print('POST')
        form_data = request.form
    return render_template('event/create.html')

@bp.route('/<my_event>/comments', methods=['GET', 'POST'])
@login_required
def comment(id):
        form = CommentForm()
        event_obj = website.query.get(id=id).first()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              website=event_obj, user=User)
            db.session.add(comment)
            db.session.commit()

            print('Comment added', 'success')
            return redirect(url_for('models.event', id=event_obj.id))
        return render_template('models.event.html', website=event_obj, form=form)

# Route for Event Page
@bp.route('/event/<id>', methods=['GET', 'POST'])
def event(id):
    event = Event.query.filter_by(id=id).first()
    register = RegisterForm()
    MealForm = MealForm()
    PAYMENT_REQUIRED = 403
    return render_template('event/event.html', event=event, register=register, MealForm=MealForm, PAYMENT_REQUIRED=PAYMENT_REQUIRED)
    