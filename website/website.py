
from asyncio import events
from csv import unregister_dialect
from flask import Blueprint, render_template, request, redirect, url_for
from .models import User, Comment, website
from .forms import UserForm, CommentForm
from crypt import methods
from urllib import request
from xml.etree.ElementTree import Comment
from auth import login_required
from flask_sqlalchemy import SQLAlchemy
from . import db


bp = Blueprint('website', __name__, url_perfix='/website')

@bp.route('/<id>')
def show(id):
    website = website.query.get(id=id).first()
    # create the comment form
    cform = CommentForm()
    return render_template('website/show.html', website=website, cform=cform)


@bp.route('/new-event', methods = ['GET', 'POST'])
def create():
    print('Method types', request.method)
    return redirect(url_for('website.new-event'))
    return render_template('website/new-event', form=form)    
        

class User:
    # this is the function used to create the user
    def __init__(self):
        self.user_type='guest'
        self.uname=None
        self.pwd=None
        self.emailID=None

    def register(self,name,pwd,emailID):
        self.uname=name
        self.pwd=pwd
        self.emailID=emailID

    def __repr__(self):
        s= "Name: {0}, Email: {1}, type: {2}\n"
        s=s.format(self.uname, self.emailID, self.user_type)
        return s
    @bp.route('/<my_event>/comments', methods = ['GET', 'POST'])
    @login_required
    def comment (id):
        form = CommentForm()
        website_obj = website.query.get(id=id).first()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data, website=website_obj,user=User)
            db.session.add(comment)
            db.session.commit()

            print('Comment added','success')
            
            return redirect(url_for('website.show', id=website_obj.id))
            
  
