from flask import Blueprint
from flask import render_template
from .models import db
from .models import Cuisine
import datetime as DT

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html', cuisines=cs)
