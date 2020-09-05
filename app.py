import os
from forms import AddForm, DelForm, AddOwnerForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SECRET_KEY"] = "jump-card-mask"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

Migrate(app, db)


class Puppy(db.Model):

    # __tablename__ = "puppy"
    # default name will be puppy

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # first argument: Class Name
    # backref: Indicates the string name of a property to be placed on
    #          the related mapper's class that will handle this relationship 
    #          in the other direction. I.e., owner.puppy where owner is an instance of Owner
    owner = db.relationship("Owner", backref="puppy", uselist=False)

    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"{self.name} (id: {str(self.id)}, owner: {self.owner} )"

    def __repr__(self):
        return f'{{"id":"{self.id}", "name":"{self.name}", "owner":"{self.owner}"}}'


class Owner(db.Model):

    # __tablename__ = "owner"
    # default name will be owner
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # foreign key argument: "table.column_name". This will set up the physical column to hold the foreign key.
    puppy_id = db.Column(db.Integer, db.ForeignKey("puppy.id"))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f'{{"name":"{self.name}"}}'


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/add_owner", methods=["GET","POST"])
def add_owner():
    
    form = AddOwnerForm()

    if form.validate_on_submit():
        name = form.name.data
        pup_id = form.puppy_id.data
        new_owner = Owner(name, pup_id)
        print(new_owner.name)
        print(new_owner.puppy_id)
        db.session.add(new_owner)
        db.session.commit()

        return redirect(url_for("list_pup"))

    return render_template("add_owner.html", form=form)


@app.route("/add", methods=["GET","POST"])
def add_pup():
    
    form = AddForm()
    
    if form.validate_on_submit():
        name = form.name.data
        newpuppy = Puppy(name)
        db.session.add(newpuppy)
        db.session.commit()

        return redirect(url_for("list_pup"))

    return render_template("add.html", form=form)


@app.route("/list")
def list_pup():

    puppies = Puppy.query.all()
    return render_template("list.html", puppies=puppies)


@app.route("/delete", methods=["GET","POST"])
def del_pup():

    form = DelForm()

    if form.validate_on_submit():

        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for("list_pup"))
    
    return render_template("delete.html", form=form)

if(__name__ == "__main__"):
    app.run(debug=True)
