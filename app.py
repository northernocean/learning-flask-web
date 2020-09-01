import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

Migrate(app, db)


class Puppy(db.Model):

    # Override default table name
    # __tablename__ = "puppies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    age = db.Column(db.Integer)
    breed = db.Column(db.Text)
    toys = db.relationship('Toy', backref='puppy', lazy='dynamic')    # one to many 
                                                                      # backref is the name of a virtual field in the other table referring to this table 
                                                                      #   i.e. toy.puppy = 1. Maybe can use real column name too not sure!
    owner = db.relationship('Owner', backref='puppy', uselist=False)  # one to one

    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed

    def __str__(self):
        return f"{self.id}/{self.name},{self.age},{self.breed},{self.owner.name if self.owner else ''}"
    
    def __repr__(self):
        return f'{{"id":"{self.id}", "name":"{self.name}", "age":"{self.age}", "breed":"{self.breed}", "owner":"{self.owner.name if self.owner else None}"}}'

    def report_toys(self):
        print("Here are my toys!")
        for toy in self.toys:
            print(toy.item_name)
        

class Toy(db.Model):

    id = db.Column(db.Integer,primary_key = True)
    item_name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppy.id'))

    def __init__(self,item_name,puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id


class Owner(db.Model):

    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppy.id'))

    def __init__(self,name,puppy_id):
        self.name = name
        self.puppy_id = puppy_id