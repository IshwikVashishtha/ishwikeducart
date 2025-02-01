# import bson
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, LoginManager, current_user, logout_user, UserMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

# Load environment variables
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")
client = MongoClient(connection_string)

# Access the database and collections
db = client['test']
users_collection = db['users']
notes_collection = db['notes']

# Function to insert a new note

@login_required
def insert_note(subject, year, title, description, file):
    notes_collection.insert_one({
        "subject": subject,
        "year": year,
        "title": title,
        "description": description,
        "pdfLink": file
    })

# Function to insert a new user
def insert_user(email, password , notes = [""] , username="username", bio="tell about your self" ):
    users_collection.insert_one({
        "bio":bio,
        "username":username,
        "email": email,
        "password": password,
        "user_notes":notes
    })

# Function to generate the list of all notes
def list_of_notes():
    return list(notes_collection.find())

def editprofile(username ,  bio):
    pass




# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.username = user_data['username']
        self.id = user_data['email']
        self.user_data = user_data

# User loader for Flask-Login
@login_manager.user_loader
def load_user(email):
    user_data = users_collection.find_one({'email': email})
    if user_data:
        return User(user_data)
    return None






# initial Home page

@app.route('/profile_page/<user_id>')
@login_required
def userprofile(user_id):
    requested_user = users_collection.find_one({"username" : user_id})
    return render_template("profile_page.html"  , username=user_id , bio= requested_user['bio'])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/notes')
def notes():
    return render_template("Notes.html" , Notes = list_of_notes())

@app.route('/resources')
def resources():
    return render_template("resources.html" )



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
            message = flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login' ,  messages = message))
    return render_template("register.html")

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        # Check if the username and password match
        user_data = users_collection.find_one({'email': user_email})
        if user_data and check_password_hash(user_data['password'], user_password):
            user = User(user_data)
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('userprofile', user_id=user_data['username']))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template("login.html")

@app.route('/log-out')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for("index"))

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


if __name__ == "__main__":
    app.run(debug=True)