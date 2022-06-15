
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, FileField, IntegerField, DateTimeField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}


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
    image = FileField('Meal image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')
    ])
    address = StringField('Address', validators=[InputRequired()])
    time = StringField('Time', validators=[InputRequired()])
    coarse_location = StringField(
        'Coarse location', validators=[InputRequired()])
    capacity = IntegerField('Capacity', validators=[InputRequired()])
    cuisine = StringField('Cuisine', validators=[InputRequired()])
    ticket_price = FloatField('Ticket Price', validators=[InputRequired()])
    submit = SubmitField("Create")


    # Book form
class BookForm(FlaskForm):
        # within the validator make sure the amount is > 0
    name = StringField('Description of event', validators=[InputRequired()])
    ticket = IntegerField('Amount of tickets', validators=[InputRequired()])
    submit = SubmitField("Submit")

class DelForm(FlaskForm):
        # within the validator make sure the amount is > 0
    name = StringField('Description of event', validators=[InputRequired()])
    submit = SubmitField("Submit")

    
    # Comment form
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField("Submit")

