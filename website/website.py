
#from flask import Blueprint, render_template, request, redirect, url_for
#from .models import User, Comment
#from .forms import UserForm, CommentForm

#bp = Blueprint('website', __name__, url_perfix='/website')

#@bp.route('/<id>')
#def show(id):
#    wesbite = get_website()
    # create the comment form
#    cform = CommentForm()
#    return render_template('website/event.html', website=website, form=form )
from crypt import methods
from urllib import request
from xml.etree.ElementTree import Comment

from flask import redirect, url_for

@bp.route('/new-event', methods = ['GET', 'POST'])
def create():
    print('Method types', request.method)
    return redirect(url_for('website.new-event'))
# return render_template('website/new-event', form=form)    

