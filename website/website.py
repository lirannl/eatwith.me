from crypt import methods
from urllib import request
from xml.etree.ElementTree import Comment

from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint('website', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')

@bp.route('/new-event', methods = ['GET', 'POST'])
def create():
    print('Method types', request.method)
    return redirect(url_for('website.new-event'))
# return render_template('website/new-event', form=form)    

