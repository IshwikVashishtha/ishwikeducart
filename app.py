import bson
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
# access your MongoDB Atlas cluster
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")
client = MongoClient(connection_string)

# add in your database and collection from Atlas
db = client['test']
collection1 = db['users']
collection2 = db['notes']

users = collection1.find()


app = Flask(__name__)
# function to generate the list of all the notes.e
def list_of_notes():
    documents = collection2.find()
    Notes = []
    for note in documents:
        Notes.append(note)
    return Notes

# function to filter notes according to the user.
def filter_notes():
    subject = request.args.get('subject')
    year = request.args.get('year')

    filtered_notes = [note for note in notes if
                      (subject == "" or note['subject'] == subject) and
                      (year == "" or note['year'] == year)]

    return render_template("notes.html" , Notes=filtered_notes)

# initial Home page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/notes')
def notes():
    return render_template("Notes.html" , Notes = list_of_notes())

@app.route('/resources')
def resources():
    return render_template("resources.html")

if __name__ == "__main__":
    app.run(debug=True)