from flask import Blueprint, abort, redirect, request, url_for
from flask import render_template
from flask_login import current_user
from website.helpers import b64, id_to_string
from . import db

#from website.forms import MealForm, RegisterForm
from .models import Cuisine, Event

bp = Blueprint('website', __name__)


@bp.route('/')
def index():
    return render_template('index.html', cuisines=Cuisine.query.all(), events=Event.query.all(), b64=b64, id_to_string=id_to_string)


@bp.route('/search')
def search():
    query: str = request.values['query']
    if query == '':
        return redirect(url_for('website.index'))
    return render_template('index.html', cuisines=Cuisine.query.all(), events=Event.query.filter(Event.description.contains(query)).all(), b64=b64, id_to_string=id_to_string)


@bp.route('/my_events')
def my_events():
    return render_template('index.html', cuisines=Cuisine.query.all(), events=current_user.events, b64=b64, id_to_string=id_to_string)


@bp.route('/<cuisine_name>')
def cuisine(cuisine_name: str):
    cuisine = Cuisine.query.filter_by(name=cuisine_name).first()
    if cuisine is None:
        abort(404)
    return render_template('index.html', cuisines=Cuisine.query.all(), events=Event.query.filter_by(cuisine=cuisine).all(), b64=b64, id_to_string=id_to_string)
