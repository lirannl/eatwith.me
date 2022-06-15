# import flask - from the package import class
from flask import Blueprint, Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from base64 import b32encode

from website.forms import LoginForm

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application


def create_app():
    # this is the name of the module/package that is calling this app
    app = Flask(__name__)
    app.debug = True
    # set the app configuration data
    app.config['SECRET_KEY'] = "סודכמוסבהחלט"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)

    # initialize the login manager
    login_manager = LoginManager()

    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(eval(user_id))

    # importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    #create meal import
    from . import meal
    app.register_blueprint(meal.bp)

    # Error handling general error messages
    @app.errorhandler(404)  # not found
    def not_found(e):
        return render_template("error.html", errortype="404")

    @app.errorhandler(403)  # if you dont have access
    def not_found(e):
        return render_template("error.html", errortype="403")

    @app.errorhandler(401)  # if you havent logged in
    def not_found(e):
        return render_template("error.html", errortype="401")

    @app.errorhandler(500)  # server error
    def not_found(e):
        return render_template("error.html", errortype="500")

    @app.before_first_request
    def create_tables():
        db.metadata.create_all(db.engine)

    return app