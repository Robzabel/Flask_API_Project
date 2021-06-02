from flask import Flask
from flask_restful import Api, Resource, reqparse


#Create the FlasK App
app = Flask(__name__)
#Create the API wrapper and pass the app to it    
api = Api(app)                
#Create the Request Parser object
film_put_args = reqparse.RequestParser()


#Define the paramaters to parse requests for, extracted data will be stored in parse_args()
film_put_args.add_argument("title", type=str, help='You must specify the Title of the film!')
film_put_args.add_argument("director", type=str, help='You must specify the Director of the film!')
film_put_args.add_argument("rating", type=int, help='You must specify the Rating of the film, 1 - 10!')


films = {}


class Film(Resource):
    """
    The Film Resource that the API will refer to 
    """

    def get(self, film_id):
        return films[film_id]


    def put(self, film_id):
        args = film_put_args.parse_args() #the parse_args() method searches the request for the criteria in the add_argument statements above
        return{film_id : args} #Return the data that has been added to the user


#link the resource with the URL string and the dynamin value
api.add_resource(Film, "/film/<int:film_id>")


#If this file is executed, not imported, run the application
if __name__ == "__main__":
    app.run(debug=True)
