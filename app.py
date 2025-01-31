# import bson
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

# access your MongoDB Atlas cluster
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")
client = MongoClient(connection_string)

# add in your database and collection from Atlas
db = client['test']
users_collection = db['users']
collection2 = db['notes']

users = users_collection.find()
def insert_note(subject , year,title ,description , file):
    collection2.insert_one(
        {
            "subject": subject,
            "year": year,
            "title": title,
            "description": description,
            "pdfLink": file
        }
    )

def insert_user(email , password):
    users_collection.insert_one(
        {
            "email": email,
            "password": password
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
app.secret_key = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"

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

@app.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        # print(user_email , user_password)
        if users_collection.find_one({'email': user_email}):
            flash('Email already exists. Choose a different one.', 'danger')
        else:
            hashed_password = generate_password_hash(user_password, salt_length=5)
            insert_user(user_email, hashed_password)
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login' , methods=['GET', 'POST'])
def login():
    
    return render_template("login.html")

@app.route('/log-out')
def logout():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)