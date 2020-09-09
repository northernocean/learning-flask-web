from flask import render_template, url_for, flash, redirect, request, Blueprint
from puppycompanyblog.models import User
from flask_login import login_user, logout_user
from puppycompanyblog import db
from puppycompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from puppycompanyblog.users.picture_handler import add_profile_image

users = Blueprint("users", __name__)

# account
# list of posts

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@users.route("/register", methods=["GET","POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.data.password)

        db.session.add(user)
        db.session.commit()

        flash("Thanks for registering.")

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


@users.route("/login", methods=["GET","POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            if (next is None) or (not next[0] == "/"):
                next = url_for("core.index")
            return redirect(next)

    return render_template("login.html", form=form)
