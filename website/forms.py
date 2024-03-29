
from datetime import datetime
from typing import cast
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, FileField
from wtforms.fields.html5 import DateTimeLocalField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed


# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")


# this is the registration form
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    username = StringField("Email Address (username)", validators=[
                           Email("Please enter a valid email")])
    contact_number = StringField("Phone number", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(
        6, -1, "Password must not be shorter than 6 characters")])
    confirm = PasswordField("Confirm Password", validators=[
                            EqualTo('password', message="Passwords should match")])
    submit = SubmitField("Register")

# Create/Update new meal


class MealForm(FlaskForm):
    description = TextAreaField('Description',
                                validators=[InputRequired()])
    image = FileField('Meal image',
                      validators=[FileAllowed({'PNG', 'JPG', 'png', 'jpg'},
                                              message='Only supports png,jpg,JPG,PNG')
                                  ])
    address = StringField('Address', validators=[InputRequired()])
    time = DateTimeLocalField('Time')
    coarse_location = StringField(
        'Coarse location', validators=[InputRequired()])
    capacity = IntegerField('Capacity', validators=[InputRequired(
    ), NumberRange(min=1, message="Must have some capacity")])
    cuisine = StringField('Cuisine', validators=[InputRequired()])
    ticket_price = DecimalField('Ticket Price', validators=[InputRequired()])
    submit = SubmitField("Submit")

    def populate_obj(self, obj):
        self.description.data = obj.description
        self.address.data = obj.address
        self.capacity.data = obj.capacity
        self.cuisine.data = obj.cuisine.name
        self.time.data = cast(datetime, obj.time)
        self.coarse_location.data = obj.coarse_location
        self.ticket_price.data = obj.ticket_price


class DelForm(FlaskForm):
    # within the validator make sure the amount is > 0
    name = StringField('Description of event', validators=[InputRequired()])
    submit = SubmitField("Submit")

    # Comment form


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField("Submit")
