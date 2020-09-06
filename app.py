from project import app, db
from flask import (render_template, redirect, request, url_for, flash)
from flask_login import login_user, login_required, logout_user
from project.models import User
from project.forms import LoginForm, RegistrationForm


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/welcome")
@login_required
def welcome_user():
    return render_template("welcome_user.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("Login Successful")

            next = request.args.get(
                "next")  # the page the user wanted, but needed to login first
            if next is None or (not next[0] == "/"):  # not next[0] means we are in this domain, not some other website
                return redirect(url_for("welcome_user"))

            return redirect(next)

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering")

    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
