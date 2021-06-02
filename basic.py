from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

names = {'john':{'age': 32, 'gender': 'male'},
        'steff': {'age': 26, 'gender': 'female'}}

class HelloWorld(Resource):
    def get(self, name):
        return names[name]

api.add_resource(HelloWorld, '/<string:name>')

if __name__ == "__main__":
    app.run(debug = True)