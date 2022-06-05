
from tkinter.tix import InputOnly
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo


# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")



# this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    contact_number = StringField(
        "Contact Number", validators=[InputRequired()])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired()])
    confirm = PasswordField("Confirm Password", validators=[
                            InputRequired(), EqualTo('password', message="Please confirm password")])

    # submit button
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
    text: TextAreaField('Comment', [InputRequired])
    sumbit: SubmitField('Create')