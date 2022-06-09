
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, FileField, IntegerField, DateTimeField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field


    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #User comment 
    class CommentForm(FlaskForm):
        text: TextAreaField('Comment', [InputRequired])
        sumbit: SubmitField('Create')

    #submit button
    submit = SubmitField("Register")

#Create/Update new meal
class MealForm(FlaskForm):
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  image = FileField('Meal image', validators=[
    # FileRequired(message='Image cannot be empty'),
    # FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')
    ])
  Price = StringField('Price', validators=[InputRequired()])
  address = StringField('Address', validators=[InputRequired()])
  time = DateTimeField('Time', validators=[InputRequired()])
  coarse_location = StringField('Coarse location', validators=[InputRequired()])
  capacity = IntegerField('Capacity', validators=[InputRequired()])
  cuisine = StringField('Cuisine', validators=[InputRequired()])
  ticket_price = FloatField('Ticket Price', validators=[InputRequired()])
  submit = SubmitField("Create")
  
  #Book form
  class BookForm(FlaskForm):
    count = IntegerField('Amount of tickets', validators=[InputRequired(), ])#within the validator make sure the amount is > 0