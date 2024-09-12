from flask import Flask, request, render_template, jsonify
import face_recognition
import os
import sqlite3
from database import create_user_table, save_user_to_db

app = Flask(__name__)

# Create user table if it doesn't exist
create_user_table()

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        upi_id = request.form['upi_id']
        
        # Save the uploaded photo temporarily
        photo = request.files['photo']
        photo_path = f"photos/{name}.jpg"
        photo.save(photo_path)
        
        # Generate face encoding from the uploaded photo
        image = face_recognition.load_image_file(photo_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            save_user_to_db(name, email, phone, upi_id, face_encoding)
            return jsonify({'status': 'success', 'message': 'User registered successfully!'})
        else:
            return jsonify({'status': 'fail', 'message': 'No face detected. Try again.'})
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)