import sqlite3
import numpy as np

# Connect to SQLite database
def connect_db():
    return sqlite3.connect('users.db')

# Create the user table if it doesn't exist
def create_user_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            upi_id TEXT NOT NULL,
            face_encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Save user details to the database
def save_user_to_db(name, email, phone, upi_id, face_encoding):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, phone, upi_id, face_encoding) VALUES (?, ?, ?, ?, ?)",
                   (name, email, phone, upi_id, face_encoding.tobytes()))
    conn.commit()
    conn.close()

# Load known faces from the database
def load_known_faces():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, face_encoding, upi_id FROM users")
    known_faces = []
    known_names = []
    known_upi_ids = []
    for row in cursor.fetchall():
        name, face_encoding, upi_id = row
        known_faces.append(np.frombuffer(face_encoding))
        known_names.append(name)
        known_upi_ids.append(upi_id)
    conn.close()
    return known_faces, known_names, known_upi_ids