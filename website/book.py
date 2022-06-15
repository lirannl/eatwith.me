from itertools import count
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Cuisine, Event, User, Book
from .forms import MealForm, RegisterForm, BookForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from website.helpers import id_to_string, string_to_id
from typing import Optional

bp = Blueprint('book', __name__, url_prefix='/book', template_folder = '/book')

#Stroing the db information once user creates a meal
@bp.route('/<id>')
def show(id):
     event = Event.query.filter_by(id=id).first
     return render_template('event/index.html', event=event)#Look at this and change it


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = BookForm() 
    if form.validate_on_submit():
        # call the function that checks and returns image
        try:
            selected_event = Event.query.where(Event.description.lower() == 
                                        request.form.name.lower().trim()).first()
            if selected_event is not None:
                if selected_event.capacity >=request.form.ticket:
                    print('Booked out')
                    #Make a booking table where you store the ticket amount,event id,cost in total,booking_id
                
                elif selected_event.capacity<= request.form.ticket:
                    print('Commiting all changes')
                    #reutrn to user say order being place and return order if for reference
        except:
            print('cant find the matching database')
        
        # if book is None:
        #     db.session.add(Book(name=(request.form.book.lower()).trim()))
        #     # Get the newly created cuisine
        #     book = Book.query.where(Book.name.lower() ==
        #                                   request.form.book.lower().trim()).first()
        # ticket = Book(name=form.name.data, book=book, host=current_user, description=form.description.data)
        # #num_tickets
        
        # # add the object to the db session
        # db.session.add(ticket)
        # # commit to the database
        # db.session.commit()
        # print('Successfully created new ticket')
        # # Always end with redirect when form is valid
        return redirect(url_for('meal.create'))
    return render_template('event/create.html', form=form)
