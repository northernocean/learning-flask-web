import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from users import authenticate, identity
from flask_jwt import JWT, jwt_required
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
jwt = JWT(app, authenticate, identity)
api = Api(app)


class Puppy(db.Model):

    name = db.Column(db.String(80), primary_key=True)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name}

    def __str__(self):
        return f"{self.name}"


class PuppyResource(Resource):

    def get(self, name):
        pup = Puppy.query.filter_by(name=name).first()
        if pup:
            return pup.json()
        return {}, 404

    @jwt_required()
    def post(self, name):
        pup = Puppy(name=name)
        db.session.add(pup)
        db.session.commit()
        return pup.json()

    def delete(self, name):
        pup = Puppy.query.filter_by(name=name).first()
        if pup:
            db.session.delete(pup)
            db.session.commit()
            return {}, 400
        return {}, 404


class AllPuppies(Resource):

    @jwt_required()
    def get(self):
        puppies = Puppy.query.all()
        return [pup.json() for pup in puppies]


api.add_resource(PuppyResource, '/puppy/<string:name>')
api.add_resource(AllPuppies, '/puppies')

if __name__ == '__main__':
    app.run(debug=True)
