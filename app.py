from flask import Flask
from flask_restful import Resource, Api
from users import authenticate, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.config["SECRET_KEY"] = 'dove-drop-forward-kettle'
api = Api(app)
jwt = JWT(app, authenticate, identity)

# In-Memory "Database": list of puppy key/value pairs: [{'name':'rufus'},{'name':'ollie'}, ...]
puppies = []


class PuppyNames(Resource):

    @jwt_required()
    def get(self, name):
        for pup in puppies:
            if pup["name"] == name:
                return pup
        return {}, 404

    def post(self, name):
        pup = {"name": name}
        puppies.append(pup)
        return pup

    def delete(self, name):
        for num, pup in enumerate(puppies):
            if pup["name"] == name:
                deleted = puppies.pop(num)
                return deleted


class AllNames(Resource):
    def get(self):
        return {"puppies": puppies}


api.add_resource(PuppyNames, "/puppy/<string:name>")
api.add_resource(AllNames, "/puppy/all")
# api.add_resource(HelloWorld, "/")

if(__name__ == "__main__"):
    app.run(debug=True)
