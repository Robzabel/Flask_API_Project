import requests

BASE = "http://127.0.0.1:5000/"             #Global Variable for the base URL of the server

response = requests.get(BASE + "john")               #Create an object that holds the returned GET data. Use requests.get(BASE + "path/to/resource") you can chane the HTTP method to GET,POST,DELETE,PUT
print(response.json())                      #Print the response in a JSON format. use the .json() method to return the data not the response object