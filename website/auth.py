from typing import Optional
from flask import (
    Blueprint, Response, abort, flash, render_template, request, redirect
)
from urllib.parse import urlparse, unquote
from website.models import User
#from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_required, login_user, logout_user
from . import db


# create a blueprint
bp = Blueprint('auth', __name__)


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method != "POST":
        return render_template("base.html")
    username = request.form["username"]
    password = request.form["password"]
    user: Optional[User] = User.query.where(User.username == username).first()
    if user is not None and user.check_password(password):
        if not login_user(user):
            return abort(Response("Not authorised to log in", 403))
        # Was this request sent from a page that has a "next" parameter?
        next = unquote(urlparse(request.referrer).query).replace("next=", "")
        if next != "":
            return redirect(next)
        return redirect(request.origin)
    flash("Invalid username or password", "login_error")
    return redirect(request.origin)

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect("/")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db.session.add(User(
            request.form["username"], request.form["name"], request.form["contact_number"]))
        newUser: User = User.query.where(
            User.username == request.form["username"]).first()
        newUser.set_password(request.form["password"])
        try:
            db.session.commit()
        except Exception as e:
            print(e.with_traceback())
        return redirect("/")
    return render_template("register.html", form=RegisterForm())
