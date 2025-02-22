from bson import ObjectId
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime
from user import User
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail , Message

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
app.config['ALLOWED_EXTENSIONS'] = {'pdf' , 'doc'}

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("APP_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("EMAIL")

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Create uploads directory if not exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)


def send_verification_email(email):
    token = s.dumps(email, salt='email-confirm')
    confirm_url = url_for('confirm_email', token=token, _external=True)
    subject = "EMAIL VERIFICATION"
    body = f'''Click the link to confirm your email and do not share it with anyone:{confirm_url}'''

    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def insert_note(subject, year, title, description, filename):
    notes_collection.insert_one({
        "subject": subject.lower(),
        "year": f"{year} year",
        "title": title,
        "description": description,
        "pdfLink": filename,
        "user_id": str(current_user.id),
        "created_at": datetime.utcnow()
    })

def list_of_notes():
    return list(notes_collection.find())

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
            unique_filename = f"{current_user.id}{int(datetime.utcnow().timestamp())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            insert_note(subject, year, title, description, unique_filename)
            flash('Note uploaded successfully!', 'success')
        else:
            flash('Allowed file type is PDF only', 'danger')

        return redirect(url_for('userprofile', user_id=current_user.username))


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/profile_page/<user_id>', methods=['GET', 'POST'])
# @login_required
def userprofile(user_id): # user_id is the user_name of the user
    user_data = users_collection.find_one({"username": user_id})
    if not user_data:
        flash("User not found!", "danger")
        return redirect(url_for('index'))

    user_notes = list(notes_collection.find({"user_id": str(user_data['_id'])}))
    # Initialize default values if certain fields don't exist
    user_profile = {
        'username': user_data.get('username', ''),
        'email': user_data.get('email', ''),
        'points': user_data.get('points', 0),
        'role': user_data.get('role', 'student'),
        'badges': user_data.get('badges', []),
        'followers': user_data.get('followers', []),
        'following': user_data.get('following', []),
        'profile_image': user_data.get('profile_image', 'default.jpg'),
        'social_links': user_data.get('social_links', {}),
        'achievements': user_data.get('achievements', []),
        'bio': user_data.get('bio', 'No bio available'),
        'created_on': user_data.get('created_on', datetime.now())
    }

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
                           user_profile= user_profile,
                           username=user_id,
                           bio=user_data.get('bio', ''),
                           notes=user_notes,
                           user_id=user_id)

@app.route('/')
def index():
    users_list = [doc["username"] for doc in users_collection.find({}, {"username": 1, "_id": 0})]
    # print(users_list)
    return render_template("index.html" , users_names= users_list)

@login_required
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

        # Check existing users
        if users_collection.find_one({'email': user_email}):
            flash('Email already exists. Choose a different one.', 'danger')
        elif users_collection.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            hashed_password = generate_password_hash(user_password)
            users_collection.insert_one({
                'email': user_email,
                'username': username,
                'password': hashed_password,
                'is_verified': False,
                'bio': 'Tell about yourself',
                'points': 0,
                'badges': [],
                'followers': [],
                'following': [],
                'profile_image': 'default.jpg',
                'social_links': {},
                'achievements': [],
                'created_at': datetime.utcnow(),
                'user_notes': []
            })

            send_verification_email(user_email)
            flash('A confirmation email has been sent. Please check your inbox.', 'success')
            return redirect(url_for('login' , email=user_email))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        user_data = users_collection.find_one({'email': user_email})

        if user_data:
            if not user_data.get('is_verified', False):
                flash('Please verify your email before logging in.', 'danger')
                return redirect(url_for('login'))

            if check_password_hash(user_data['password'], user_password):
                user = User(user_data)
                login_user(user)
                flash('Login successful.', 'success')
                return redirect(url_for('userprofile', user_id=user_data['username']))
            else:
                flash('Invalid email or password.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for("index"))

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=600) #Link expires in 10 min
        user = users_collection.find_one({'email': email})
        if user and not user.get('is_verified', False):
            users_collection.update_one({'email': email}, {'$set': {'is_verified': True}})
            flash("Your email has been verified!", "success")
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for('login'))

# @app.route('/resend_mail')
# def re_send_mail():
#     # First, try to get the email from the query parameter.
#     email = request.args.get('email')
#
#     # If the user is logged in, use their email instead.
#     if current_user.is_authenticated:
#         email = current_user.email
#
#     if not email:
#         flash('No email provided for verification.', 'danger')
#         return redirect(url_for('login'))
#
#     user = users_collection.find_one({'email': email})
#     if not user:
#         flash('No user found with that email. Please register.', 'danger')
#         return redirect(url_for('register'))
#
#     if user.get('is_verified', False):
#         flash('Your email is already verified. Please log in.', 'info')
#     else:
#         send_verification_email(email)
#         flash('A new confirmation email has been sent!', 'success')
#
#     return redirect(url_for('login'))

@app.route('/filter_notes', methods=['GET'])
def filter_notes():
    Notes = list_of_notes()
    subject = request.args.get('subject').lower()
    # year = request.args.get('year')

    filtered_notes = [note for note in Notes if
                      (subject == "" or note['subject'] == subject)]

    return render_template("notes.html", Notes=filtered_notes)

@app.route('/delete' , methods=['POST'] )
def delete():
    note_id = ObjectId(str(request.form.get('note_id')))
    notes_collection.delete_one({"_id":note_id})
    return redirect(url_for("userprofile" , user_id= current_user.username))

if __name__ == "__main__":
    app.run(debug=True , port=5001)