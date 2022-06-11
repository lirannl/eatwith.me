from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .forms import MealForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required

bp = Blueprint('meal', __name__, url_prefix='/meal')

@bp.route('/<id>')
def show(id):
    destination = Event.query.filter_by(id=id).first()

bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = MealForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path=check_upload_file(form)
    meal=Event(name=form.name.data,description=form.description.data, 
    image=db_file_path)
    # add the object to the db session
    db.session.add(meal)
    # commit to the database
    db.session.commit()
    print('Successfully created new meal')
    #Always end with redirect when form is valid
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)

#adding the check upload file form
def check_upload_file(form):
  #get file data from form  
  fp=form.image.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path