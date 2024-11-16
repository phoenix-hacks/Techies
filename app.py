from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
import random
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Set up MongoDB client for user collection
client = MongoClient('mongodb://localhost:27017/')  # Adjust to your MongoDB URI if needed
db = client['Zesty']
users_collection = db['users']
contacts_collection = db["contact_messages"]

# Set up Flask-PyMongo for registrationDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/registrationDB"  # Change this for your MongoDB URI
mongo = PyMongo(app)

# Home route to render index.html
@app.route('/')
def index():
    logged_in = 'user' in session
    return render_template('index.html', logged_in=logged_in)

# Sign In route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email_or_mobile = request.form['email_or_mobile']
        password = request.form['password']
        
        # Check if email or mobile exists in the database
        user = users_collection.find_one({'$or': [{'email': email_or_mobile}, {'mobile': email_or_mobile}]})
        
        if user and check_password_hash(user['password'], password):
            # Successful login
            session['user'] = email_or_mobile  # Store user in session
            return redirect(url_for('index'))
        else:
            # Invalid credentials
            return render_template('signin.html', error="Invalid email/mobile or password.")
    
    return render_template('signin.html')

# Sign Out route
@app.route('/signout')
def signout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('index'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Check if email or mobile already exists
        if users_collection.find_one({'$or': [{'email': email}, {'mobile': mobile}]}):
            return render_template('signup.html', error="Email or Mobile already registered.")
        
        # Insert new user into database
        users_collection.insert_one({'email': email, 'mobile': mobile, 'password': hashed_password})
        return redirect(url_for('signin'))

    return render_template('signup.html')

# Forgot Password route
@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/terms')
def terms():
    return render_template('tc.html')

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/corporate')
def corporate():
    return render_template('corporate.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/about')
def about():
    return render_template('corporate.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/offers')
def offers():
    return render_template('offers.html')

@app.route('/ride')
def ride():
    return render_template('ride.html')

@app.route('/partner')
def partner():
    return render_template('partner.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        # Get data from request
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Validation
        if not name or not email or not message:
            return jsonify({'error': 'All fields are required!'}), 400

        # Insert into MongoDB
        contacts_collection.insert_one({
            'name': name,
            'email': email,
            'message': message
        })

        return jsonify({'message': '"Thank you for contacting us! Your message has been sent successfully. We will get back to you soon."'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)  
