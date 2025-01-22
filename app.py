import bson
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

# access your MongoDB Atlas cluster
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")
client = MongoClient(connection_string)

# add in your database and collection from Atlas
db = client['test']
collection1 = db['users']
collection2 = db['notes']

users = collection1.find()
def inser_notes(subject , year,title ,description , file):
    collection2.insert_one(
        {
            "subject": subject,
            "year": year,
            "title": title,
            "description": description,
            "pdfLink": file
        }
    )


# function to generate the list of all the notes.e
def list_of_notes():
    documents = collection2.find()
    Notes = []
    for note in documents:
        Notes.append(note)
    return Notes


app = Flask(__name__)


# function to filter notes according to the user.
@app.route('/filter_notes', methods=['GET'])
def filter_notes():
    Notes = list_of_notes()
    subject = request.args.get('subject')
    year = request.args.get('year')

    filtered_notes = [note for note in Notes if
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

@app.route('/user-profile')
def userprofile():
    return render_template("userProfile.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Access form data
        email = request.form.get('email')
        password = request.form.get('password')
        # Here, you can add your authentication logic
        # For example, validate the credentials against a database
        if email == 'testmail@gmail.com' and password == 'testpassword':
            # Successful login logic
            return redirect(url_for('userprofile' , username= password))
        else:
            # Failed login logic
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        # Render the login page
        return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)