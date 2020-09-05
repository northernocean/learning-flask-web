from flask import Blueprint, render_template, redirect, url_for
from project import db
from project.models import Owner
from project.owners.forms import AddForm

owners_blueprint = Blueprint("owners", __name__,
                                template_folder="templates/owners")


@owners_blueprint.route("/add", methods=["GET","POST"])
def add():
    
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data
        pup_id = form.puppy_id.data
        new_owner = Owner(name, pup_id)
        db.session.add(new_owner)
        db.session.commit()

        return redirect(url_for("puppies.list"))

    return render_template("add_owner.html", form=form)
