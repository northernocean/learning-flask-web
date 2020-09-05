import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = "jump-card-blue"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

Migrate(app, db)

# these imports require the db to be created before they are processed
from project.puppies.views import puppies_blueprint
from project.owners.views import owners_blueprint

app.register_blueprint(owners_blueprint, url_prefix="/owners")
app.register_blueprint(puppies_blueprint, url_prefix="/puppies")
