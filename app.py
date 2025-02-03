from bson import ObjectId
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, LoginManager, current_user, logout_user, UserMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")
client = MongoClient(connection_string)

# Access the database and collections
db = client['test']
users_collection = db['users']
notes_collection = db['notes']

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create uploads directory if not exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def insert_note(subject, year, title, description, filename):
    notes_collection.insert_one({
        "subject": subject,
        "year": year,
        "title": title,
        "description": description,
        "pdfLink": filename,
        "user_id": str(current_user.id),
        "created_at": datetime.utcnow()
    })


def insert_user(email, password, username, bio="Tell about yourself", notes=None):
    if notes is None:
        notes = []
    users_collection.insert_one({
        "bio": bio,
        "username": username,
        "email": email,
        "password": password,
        "user_notes": notes
    })


def list_of_notes():
    return list(notes_collection.find())


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data.get('username', '')
        self.email = user_data.get('email')
        self.user_data = user_data

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(id):
    try:
        user_data = users_collection.find_one({'_id': ObjectId(id)})
        if user_data:
            return User(user_data)
    except:
        return None
    return None


@app.route('/upload_note', methods=['POST'])
@login_required
def upload_note():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        subject = request.form.get('subject')
        year = request.form.get('year')

        if 'file' not in request.files:
            flash('No file uploaded', 'danger')
            return redirect(url_for('userprofile', user_id=current_user.username))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('userprofile', user_id=current_user.username))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user.id}_{int(datetime.utcnow().timestamp())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            insert_note(subject, year, title, description, unique_filename)
            flash('Note uploaded successfully!', 'success')
        else:
            flash('Allowed file type is PDF only', 'danger')

        return redirect(url_for('userprofile', user_id=current_user.username))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/profile_page/<user_id>', methods=['GET', 'POST'])
@login_required
def userprofile(user_id):
    requested_user = users_collection.find_one({"username": user_id})
    if not requested_user:
        flash("User not found!", "danger")
        return redirect(url_for('index'))

    user_notes = list(notes_collection.find({"user_id": str(requested_user['_id'])}))

    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()
        new_bio = request.form.get('bio', '').strip()

        updates = {}
        redirect_user_id = user_id

        if new_username and new_username != user_id:
            if users_collection.find_one({"username": new_username}):
                flash("Username already exists!", "danger")
            else:
                updates["username"] = new_username
                redirect_user_id = new_username

        if new_bio:
            updates["bio"] = new_bio

        if updates:
            users_collection.update_one(
                {"username": user_id},
                {"$set": updates}
            )
            flash("Profile updated successfully!", "success")
            return redirect(url_for('userprofile', user_id=redirect_user_id))

    return render_template("profile_page.html",
                           username=user_id,
                           bio=requested_user.get('bio', ''),
                           notes=user_notes,
                           user_id=user_id)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/notes')
def notes():
    return render_template("Notes.html", Notes=list_of_notes())


@app.route('/resources')
def resources():
    return render_template("resources.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        username = request.form.get('username')

        if users_collection.find_one({'email': user_email}):
            flash('Email already exists. Choose a different one.', 'danger')
        elif users_collection.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            hashed_password = generate_password_hash(user_password, salt_length=5)
            insert_user(user_email, hashed_password, username)
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
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


@app.route('/filter_notes', methods=['GET'])
def filter_notes():
    Notes = list_of_notes()
    subject = request.args.get('subject')
    year = request.args.get('year')

    filtered_notes = [note for note in Notes if
                      (subject == "" or note['subject'] == subject) and
                      (year == "" or note['year'] == year)]

    return render_template("notes.html", Notes=filtered_notes)


if __name__ == "__main__":
    app.run(debug=True)