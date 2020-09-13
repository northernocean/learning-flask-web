from flask import render_template, url_for, flash, redirect, request, Blueprint
from puppycompanyblog.models import User, BlogPost
from flask_login import login_user, logout_user, login_required, current_user
from puppycompanyblog import db
from puppycompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from puppycompanyblog.users.picture_handler import add_profile_image

users = Blueprint("users", __name__)

# account
# list of posts


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.image.data:
            username = current_user.username
            new_image_path = add_profile_image(form.image.data, username)
            current_user.profile_image = new_image_path

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash("User Account Updated.")
        return redirect(url_for("core.index"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for("static", filename="profile_images/" + current_user.profile_image)
    return render_template("account.html", profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):

    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query
        .filter_by(author=user)
        .order_by(BlogPost.date.desc())
        .paginate(page=page, per_page=5)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@users.route("/register", methods=["GET", "POST"])
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


@users.route("/login", methods=["GET", "POST"])
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
