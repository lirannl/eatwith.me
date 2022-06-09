
from flask import Blueprint, render_template, request, redirect, url_for
from .models import User, Comment
from .forms import UserForm, CommentForm
from crypt import methods
from urllib import request
from xml.etree.ElementTree import Comment

bp = Blueprint('website', __name__, url_perfix='/website')

@bp.route('/<id>')
def show(id):
    #website = ()
    # create the comment form
    cform = CommentForm()
    #return render_template('website/my-event.html', website=, form=cform )


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
  #  @bp.route('/<id>/comment, method = ['Get', 'POST'])
 #   def comment (id):
        #here the form is created form = CommentForm()
#        form = CommentForm()
    #if form.validate_on_submit(): #this is true only in case of POST method
        #print("The following comment has been posted", form.text.data)
        # notice the signature of url_for
        #return redirect(url_for('website.show', id=1))
        

    def get_website():
        # a comment
        #comment = Comment()
        #User.set_comments(comment)
        #comment = Comment()
        #User.set_comments(comment)
        #return User
