import os
import sqlite3
import cv2
import face_recognition
import pickle
import base64
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from deepface import DeepFace

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max payload

DB_PATH = 'facepay.db'

# ----------------------------
# Database and User Functions
# ----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            upi_id TEXT NOT NULL,
            password TEXT NOT NULL,
            face_encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user_to_db(username, upi_id, password, face_embedding):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    encoding_blob = pickle.dumps(face_embedding)
    cursor.execute('''
        INSERT INTO users (username, upi_id, password, face_encoding)
        VALUES (?, ?, ?, ?)
    ''', (username, upi_id, generate_password_hash(password), encoding_blob))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user_credentials(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user[3], password):
        return True
    return False

# ----------------------------
# Face Processing Functions
# ----------------------------
def process_captured_image(captured_image_data):
    """
    Decodes a base64-encoded image string (e.g., "data:image/jpeg;base64,..."),
    converts it to RGB, and computes a face embedding using DeepFace.
    """
    try:
        header, encoded = captured_image_data.split(',', 1)
    except Exception as e:
        print("Error splitting image data:", e)
        return None
    image_data = base64.b64decode(encoded)
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        return None
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    try:
        # Pass the numpy array via the img_path parameter.
        # enforce_detection=False to be more forgiving.
        representations = DeepFace.represent(img_path=rgb_img, model_name="Facenet", enforce_detection=False)
        if representations and len(representations) > 0:
            return representations[0]["embedding"]
        else:
            return None
    except Exception as e:
        print("Error in DeepFace representation:", e)
        return None

def match_face(face_embedding):
    """
    Compares the provided face_embedding with stored embeddings using cosine similarity.
    Returns the first matching user whose cosine distance is below the threshold.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    from scipy.spatial.distance import cosine
    threshold = 0.6  # Increased threshold for more lenient matching. Adjust as needed.
    for user in users:
        stored_embedding = pickle.loads(user[4])
        try:
            distance = cosine(face_embedding, stored_embedding)
            print(f"Computed distance for user {user[1]}: {distance}")  # Debug: Print distance
            if distance < threshold:
                return user
        except Exception as e:
            print("Error computing cosine distance:", e)
    return None
# ----------------------------
# Routes
# ----------------------------

@app.route('/')
def index():
    # Pass the username (if available) to the template
    return render_template('index.html', username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        upi_id = request.form['upi_id']
        password = request.form['password']
        captured_image_data = request.form.get('captured_image')
        if not captured_image_data:
            return "No face image captured. Please try again."
        face_embedding = process_captured_image(captured_image_data)
        if face_embedding is None:
            return "Face not detected in the captured image. Please try again."
        add_user_to_db(username, upi_id, password, face_embedding)
        session['username'] = username  # Auto-log in after registration
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user_credentials(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template('login.html')

# New route to process live face scan for login
@app.route('/login_scan', methods=['POST'])
def login_scan():
    captured_image_data = request.form.get('captured_image')
    if not captured_image_data:
        return jsonify({'status': 'error', 'message': 'No face image captured.'})
    face_embedding = process_captured_image(captured_image_data)
    if face_embedding is None:
        return jsonify({'status': 'error', 'message': 'Face not detected.'})
    user = match_face(face_embedding)
    if user is None:
        return jsonify({'status': 'error', 'message': 'No matching user found.'})
    # Return the recognized username
    return jsonify({'status': 'success', 'username': user[1]})

# Payment Flow (Two-Step Process)
@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST' and 'captured_image' in request.form and 'amount' not in request.form:
        captured_image_data = request.form['captured_image']
        target_embedding = process_captured_image(captured_image_data)
        if target_embedding is None:
            return "Target face not detected. Please try again."
        target_user = match_face(target_embedding)
        if target_user is None:
            return "No matching user found. Please try again."
        session['target_username'] = target_user[1]
        session['target_upi'] = target_user[2]
        return render_template('pay_amount.html', target_name=target_user[1], target_upi=target_user[2])
    if request.method == 'POST' and 'amount' in request.form:
        amount = request.form['amount']
        target_upi = session.get('target_upi')
        if not target_upi:
            return "Target information missing. Please try again."
        # Payment processing logic would be integrated here.
        return f"Payment of {amount} made to {target_upi}"
    return render_template('pay_scan.html')

# Ask Money Flow (Two-Step Process)
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST' and 'captured_image' in request.form and 'amount' not in request.form:
        captured_image_data = request.form['captured_image']
        target_embedding = process_captured_image(captured_image_data)
        if target_embedding is None:
            return "Target face not detected. Please try again."
        target_user = match_face(target_embedding)
        if target_user is None:
            return "No matching user found. Please try again."
        session['target_username'] = target_user[1]
        session['target_upi'] = target_user[2]
        return render_template('ask_amount.html', target_name=target_user[1], target_upi=target_user[2])
    if request.method == 'POST' and 'amount' in request.form:
        amount = request.form['amount']
        target_upi = session.get('target_upi')
        if not target_upi:
            return "Target information missing. Please try again."
        # UPI request logic would be integrated here.
        return f"Requesting {amount} from {target_upi}"
    return render_template('ask_scan.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Logout route for completeness
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)