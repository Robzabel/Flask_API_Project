from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy


#Create the FlasK App
app = Flask(__name__)
#Create the API wrapper and pass the app to it    
api = Api(app)                
#Create the Request Parser object
film_put_args = reqparse.RequestParser()
#Create the Database object and initialise it with app
db = SQLAlchemy(app)


#Define the app configs for SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///film_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

#Create the database Model
class Film(db.Model):
    """
    The database to store the films
    """
    __tablename__ = "films"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<film: name = {self.title}, director = {self.director}, rating out of 10 = {self.rating}>"

#Configure the Database, comment as necessary
#db.drop_all()
#db.create_all()


#Define the paramaters to parse requests for, extracted data will be stored in parse_args()
film_put_args.add_argument("title", type=str, help='You must specify the Title of the film!', required =True)
film_put_args.add_argument("director", type=str, help='You must specify the Director of the film!', required=True)
film_put_args.add_argument("rating", type=int, help='You must specify the Rating of the film, 1 - 10!', required = True)


#Create a resource for the API
class Film_db(Resource):
    """
    The Film Resource for the API 
    """

    def get(self, film_id):
        output = Film.query.get(id = film_id)
        return output


    def put(self, film_id):
        
        args = film_put_args.parse_args() #the parse_args() method searches the request for the criteria in the add_argument statements above
        films[film_id] = args #stores the put data in the films dict with the film_id as the main key
        return {"message":"Your film has been added!"}, 201 #Return a success message and an HTTP code


    def delete(self, film_id):

        del films[film_id]#remove the film from the db
        return {"message":"Your film has been deleted!"}, 200#return a success message and an HTTP code

#link the resource with the URL string and the dynamin value
api.add_resource(Film, "/film/<int:film_id>")


#If this file is executed, not imported, run the application
if __name__ == "__main__":
    app.run(debug=True)
