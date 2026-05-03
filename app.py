import sqlite3
import os
import logging
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import scrython
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app=Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        db.commit()

init_db()

@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.path}")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user is None or not check_password_hash(user['password'], password):
            logger.warning(f"Failed login attempt for username: '{username}'")
            error = 'Invalid username or password.'
        else:
            session['user_id'] = user['id']
            session['username'] = user['username']
            logger.info(f"User logged in successfully: '{username}'")
            return redirect(url_for('index'))
            
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        
        if not username or not password:
            logger.warning("Registration failed: Missing username or password.")
            error = 'Username and password are required.'
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            logger.warning(f"Registration failed: Username '{username}' already exists.")
            error = f"User {username} is already registered."
        else:
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            
            logger.info(f"New user registered: '{username}'")
            
            # Automatically login the user after registration
            user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
            
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    username = session.get('username')
    session.clear()
    if username:
        logger.info(f"User logged out: '{username}'")
    return redirect(url_for('index'))

@app.route('/background_card')
def getcard():
    card = scrython.cards.Random()
    return jsonify(card.image_uris['normal']) 

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    logger.info("Starting Synergy Flask server")
    app.run(debug=True)


#TODO:
# - Add user profile page with card collection and deck management
# - Add a section for users to add notes for their campaign or quest ideas
# - Update passwords to force complexity requirements and add password reset functionality