
from flask import Blueprint, render_template, redirect, url_for
from project import db
from project.models import Puppy 
from project.puppies.forms import AddForm, DelForm

puppies_blueprint = Blueprint("puppies", __name__,
                                template_folder="templates/puppies")


@puppies_blueprint.route("/add", methods=["GET","POST"])
def add():
    
    form = AddForm()
    
    if form.validate_on_submit():
        name = form.name.data
        newpuppy = Puppy(name)
        db.session.add(newpuppy)
        db.session.commit()

        return redirect(url_for("puppies.list"))

    return render_template("add.html", form=form)


@puppies_blueprint.route("/list")  # no form on this page so don't require methods...
def list():

    puppies = Puppy.query.all()
    return render_template("list.html", puppies=puppies)


@puppies_blueprint.route("/delete", methods=["GET","POST"])
def delete():

    form = DelForm()

    if form.validate_on_submit():

        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for("puppies.list"))
    
    return render_template("delete.html", form=form)


if(__name__ == "__main__"):
    app.run(debug=True)