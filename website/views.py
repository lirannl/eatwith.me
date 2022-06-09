from flask import Blueprint
from flask import render_template
from .models import db
from .models import Cuisine
import datetime as DT

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    cuisines    = Cuisine.query.all()
    cs          = list()
    for cuisine in cuisines:
        if DT.datetime.now() < cuisine.date_from:
            cuisine.status = 'Upcoming'
        elif DT.datetime.now() > cuisine.date_from and DT.datetime.now() < cuisine.date_to:
            cuisine.status = 'Active'
        else:
            cuisine.status = 'Inactive'
        cs.append(cuisine)
    return render_template('index.html', cuisines=cs)
