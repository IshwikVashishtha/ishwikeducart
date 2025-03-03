import base64
from bson.binary import Binary
from bson import ObjectId
from gridfs import GridFS
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime
from user import User
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail , Message
from flask_socketio import SocketIO, join_room, emit

# Load environment variables
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")
client = MongoClient(connection_string)

# Access the database and collections
db = client['test']
users_collection = db['users']
notes_collection = db['notes']
fs_files= db['fs.files']
file_chunks = db['fs.chunks']
fs = GridFS(db)
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

socketio = SocketIO(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Create uploads directory if not exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

def get_private_room(user1, user2):
    """Unique room name for two users."""
    return '-'.join(sorted([user1, user2]))

@socketio.on('join')
def on_join(data):
    room = data['room']
    username = data['username']
    join_room(room)
    # Inform the room that a new user has joined (optional)
    emit('message', {'message': f'{username} has joined the chat.'}, room=room)

@socketio.on('message')
def handle_chat(data):
    room = data['room']
    # Broadcast the chat message to everyone in the room
    emit('message', data, room=room)

def send_verification_email(email):
    token = s.dumps(email, salt='email-confirm')
    confirm_url = url_for('confirm_email', token=token, _external=True)
    subject = "EMAIL VERIFICATION"
    body = f'''Click the link to confirm your email valid for 10 min only.:{confirm_url}'''

    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def insert_note(subject, year, title, description, file_content, original_filename):
    # Store the file in GridFS and get the file_id
    file_id = fs.put(file_content, filename=original_filename)

    # Save the note with a reference to the file_id
    notes_collection.insert_one({
        "subject": subject.lower(),
        "year": f"{year} year",
        "title": title,
        "description": description,
        "file_id": file_id,  # Reference to the GridFS file
        "user_id": str(current_user.id),
        "original_filename": original_filename,
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

@login_required
@app.route('/upload_note', methods=['POST'])
def upload_note():
    title = request.form.get('title')
    description = request.form.get('description')
    subject = request.form.get('subject')
    year = request.form.get('year')
    file = request.files.get('file')

    if not file or file.filename == '':
        flash('No file uploaded', 'danger')
        return redirect(url_for('home'))

    if allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        file_content = file.read()  # Read the file content
        insert_note(subject, year, title, description, file_content, original_filename)
        flash('File uploaded successfully!', 'success')
    else:
        flash('Allowed file types are PDF and DOC', 'danger')
    return redirect(url_for('userprofile', user_id=current_user.username))

@app.route('/download_note/<note_id>')
def download_note(note_id):
    try:
        note = notes_collection.find_one({"_id": ObjectId(note_id)})
        if note and 'file_id' in note:
            file_id = note['file_id']
            gridfs_file = fs.get(file_id)  # Retrieve the file from GridFS
            file_content = gridfs_file.read()
            original_filename = note['original_filename']

            # Set the correct content type based on file extension
            extension = original_filename.rsplit('.', 1)[1].lower()
            if extension == 'pdf':
                content_type = 'application/pdf'
            elif extension == 'doc':
                content_type = 'application/msword'
            else:
                content_type = 'application/octet-stream'

            # Create a response for the file download
            response = make_response(file_content)
            response.headers['Content-Type'] = content_type
            response.headers['Content-Disposition'] = f'attachment; filename="{original_filename}"'
            return response
        else:
            flash('Note not found', 'danger')
            return redirect(url_for('Notes'))
    except:
        flash('Invalid note ID', 'danger')
        return redirect(url_for('Notes'))
@app.route('/profile_page/<user_id>', methods=['GET', 'POST'])
# @login_required
def userprofile(user_id):
    if not user_id:
        flash("LOGIN FIRST!")
        return redirect(url_for('login'))
    user_data = users_collection.find_one({"username": user_id})
    if not user_data:
        flash("User not found!", "danger")
        return redirect(url_for('index'))

    user_notes = list(notes_collection.find({"user_id": str(user_data['_id'])}))

    # Process profile image for display:
    stored_image = user_data.get('profile_image', 'default.jpg')
    if isinstance(stored_image, dict) and 'data' in stored_image:
        # Convert binary image data to a Base64 string and get its MIME type
        profile_image_data = base64.b64encode(stored_image['data']).decode('utf-8')
        image_content_type = stored_image.get('content_type', 'image/jpeg')
    else:
        # If not stored as binary, assume it's a filename for a static default image.
        profile_image_data = None
        image_content_type = None

    # Build the user_profile dict and include these values
    user_profile = {
        'username': user_data.get('username', ''),
        'email': user_data.get('email', ''),
        'points': user_data.get('points', 0),
        'role': user_data.get('role', 'student'),
        'badges': user_data.get('badges', []),
        'followers': user_data.get('followers', []),
        'following': user_data.get('following', []),
        # We'll use these in the template to decide which image source to use
        'profile_image': user_data.get('profile_image', 'default.jpg'),
        'profile_image_data': profile_image_data,
        'image_content_type': image_content_type,
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

        # Handle the uploaded profile image
        profile_image = request.files.get('profile_image')
        if profile_image and profile_image.filename != '':
            # Read the file's binary data
            image_data = profile_image.read()
            # Store both the binary data and the content type
            updates["profile_image"] = {
                "data": Binary(image_data),
                "content_type": profile_image.content_type  # e.g., "image/png" or "image/jpeg"
            }

        if updates:
            users_collection.update_one(
                {"username": user_id},
                {"$set": updates}
            )
            flash("Profile updated successfully!", "success")
            return redirect(url_for('userprofile', user_id=redirect_user_id))

    return render_template("profile_page.html",
                           user_profile=user_profile,
                           username=user_id,
                           notes=user_notes,
                           user_id=user_id)

@app.route('/chat')
def chat():
    """
    Expect query parameters:
      - username: current user's username (e.g. 'john')
      - target: the username of the person being chatted with (e.g. 'chintu')
    """
    current_username = request.args.get('username')
    target_username = request.args.get('target')
    if not current_username or not target_username:
        # You could redirect to an error page or home page if parameters are missing
        return "Missing username or target", 400

    room = get_private_room(current_username, target_username)
    return render_template('chat.html',
                           room=room,
                           username=current_username,
                           target=target_username)

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
@login_required
@app.route('/follow/<username>') #this username belongs to the user whose profile we are searching
def follow(username):
    if username == current_user.username:
        flash("You cannot follow yourself.", "danger")
        return redirect(url_for('userprofile', user_id=current_user.username))

    user_to_follow = users_collection.find_one({"username": username})
    if not user_to_follow:
        flash("User not found.", "danger")
        return redirect(url_for('index'))

    # Check if already following (using current_user.user_data)
    if username in current_user.user_data.get("following", []):
        flash(f"Already following {username}.", "info")
        return redirect(url_for('userprofile', user_id=username))

    # Add username to current user's following list...
    users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$push": {"following": username}}
    )
    # ...and add current user's username to the other user's followers list.
    users_collection.update_one(
        {"_id": user_to_follow["_id"]},
        {"$push": {"followers": current_user.username}}
    )
    flash(f"Now following {username}.", "success")
    return redirect(url_for('userprofile', user_id=username))

@login_required
@app.route('/unfollow/<username>') #this username belongs to the user whose profile we are searching
def unfollow(username):
    if username == current_user.username:
        flash("You cannot unfollow yourself.", "danger")
        return redirect(url_for('userprofile', user_id=current_user.username))

    user_to_unfollow = users_collection.find_one({"username": username})
    if not user_to_unfollow:
        flash("User not found.", "danger")
        return redirect(url_for('index'))

    # Check if not following
    if username not in current_user.user_data.get("following", []):
        flash(f"You are not following {username}.", "info")
        return redirect(url_for('userprofile', user_id=username))

    # Remove username from current user's following list...
    users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$pull": {"following": username}}
    )
    # ...and remove current user's username from the other user's followers list.
    users_collection.update_one(
        {"_id": user_to_unfollow["_id"]},
        {"$pull": {"followers": current_user.username}}
    )
    flash(f"Unfollowed {username}.", "success")
    return redirect(url_for('userprofile', user_id=username))

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
    note = notes_collection.find_one({'_id': note_id})
    file_id = note['file_id']
    file_chunks.delete_many({"files_id": file_id})
    fs_files.delete_one({"_id": file_id})
    notes_collection.delete_one({"_id":note_id})
    return redirect(url_for("userprofile" , user_id= current_user.username))

if __name__ == "__main__":
    app.run(debug=True , port=5001)