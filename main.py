from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc



#Create the FlasK App
app = Flask(__name__)
#Create the API wrapper and pass the app to it    
api = Api(app)                
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

#Create the PUT Request Parser object
film_put_args = reqparse.RequestParser()
#Define the paramaters to parse requests for, extracted data will be stored in parse_args()
film_put_args.add_argument("title", type=str, help='You must specify the Title of the film!', required =True)
film_put_args.add_argument("director", type=str, help='You must specify the Director of the film!', required=True)
film_put_args.add_argument("rating", type=int, help='You must specify the Rating of the film, 1 - 10!', required = True)

#Create the UPDATE Request Parser object
film_update_args = reqparse.RequestParser()
#Define the paramaters to parse requests for, extracted data will be stored in parse_args(). Do not make all required
film_update_args.add_argument("title", type=str, help='You must specify the Title of the film!')
film_update_args.add_argument("director", type=str, help='You must specify the Director of the film!')
film_update_args.add_argument("rating", type=int, help='You must specify the Rating of the film, 1 - 10!')

#Create the Resource field to serialize the db data object into JSON 
resource_fields = {
    "id" : fields.Integer,
    "title" : fields.String,
    "director" : fields.String,
    "rating" : fields.Integer
}


#Create a resource for the API
class Film_db(Resource):
    """
    The Film Resource for the API 
    """
    #use the decorator to serialize the returned data
    @marshal_with(resource_fields)
    def get(self, film_id):
        #Query the DB for the film date depending on the film_id provided
        output = Film.query.filter_by(id=film_id).first()
        if output:
            return output, 200
        else: 
            abort(404, message ="There is no film with the ID " + str(film_id))
      
    
    def put(self, film_id):
        #Try and catch the put attempt
        try:
            #the parse_args() method searches the request for the criteria in the add_argument statements above
            args = film_put_args.parse_args() 
            #Add the args to the model object then commit the changes
            put_film = Film(id=film_id, title=args['title'], director=args['director'], rating=args['rating'])
            db.session.add(put_film)
            db.session.commit()
            return {"message":"Your film has been added!"}, 201 #Return a success message and an HTTP code
        #IF the fim_id is not found send an error message
        except exc.IntegrityError:
            abort(409, message ="A film with the ID " + str(film_id) + " already exists in the database. Please use a different ID")


    #use the decorator to serialize the returned data        
    @marshal_with(resource_fields)
    def patch(self, film_id):
        #Create the argument object
        args = film_update_args.parse_args()
        #create the Model object
        output = Film.query.filter_by(id=film_id).first()
        #Abort if there is nothing to update
        if not output:
            abort(404, message ="A film with the ID " + str(film_id) + " does not exist in the database. Please use a different ID")
        #chek if the args attributes are not None
        if args["title"]:
            output.title = args["title"]
        if args["director"]:
            output.director = args["director"]
        if args["rating"]:
            output.rating = args["rating"]
        #commit the changes to the Database
        db.session.commit()
        #return the info to the user
        return output, 200


    def delete(self, film_id):
        #find the film to be deleted
        output = Film.query.filter_by(id=film_id).first()
        if output:
            #delete the film and commit the changes
            db.session.delete(output)
            db.session.commit()
            #return a success message and an HTTP code
            return {"message":"Your film has been deleted!"}, 200
        else:
            #IF the fim_id is not found send an error message 
            abort(404, message ="A film with the ID " + str(film_id) + " does not exist in the database. Please use a different ID")


#link the resource with the URL string and the dynamic value
api.add_resource(Film_db, "/film/<int:film_id>")


#If this file is executed, not imported, run the application
if __name__ == "__main__":
    app.run(debug=True)
