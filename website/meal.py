from flask import Blueprint, render_template, request, redirect, url_for
from .models import Comment, Cuisine, Event, User
from .forms import MealForm, RegisterForm #, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from website.helpers import id_to_string, string_to_id
from typing import Optional

bp = Blueprint('meal', __name__, url_prefix='/meal', template_folder = '/meal')

# @bp.route('/<id>')
# def show(id: str):
#     destination = Event.query.get(id)
#     return render_template('event/index.html', destination=destination)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = MealForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        cuisine = Cuisine.query.where(Cuisine.name.lower() ==
                                      request.form.cuisine.lower().trim()).first()
        if cuisine is None:
            db.session.add(Cuisine(name=(request.form.cuisine.lower()).trim()))
            # Get the newly created cuisine
            cuisine = Cuisine.query.where(Cuisine.name.lower() ==
                                          request.form.cuisine.lower().trim()).first()
        meal = Event(name=form.name.data, cuisine=cuisine, host=current_user, description=form.description.data,
                     image=db_file_path)
        # add the object to the db session
        db.session.add(meal)
        # commit to the database
        db.session.commit()
        print('Successfully created new meal')
        # Always end with redirect when form is valid
        return redirect(url_for('meal.create'))
    return render_template('event/create.html', form=form)

# adding the check upload file form


def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static/image', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/image/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

# adding the Comment Form
@bp.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id: str):
    form = CommentForm()
    event_obj: Optional[Event] = Event.query.get(string_to_id(id))
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          website=event_obj, user=User)
        db.session.add(comment)
        db.session.commit()

        print('Comment added', 'success')

        return redirect(url_for('meal.event', id=id_to_string(event_obj.id)))

    return render_template('event/event.html', website=event_obj, form=form)
   
