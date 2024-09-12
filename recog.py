import cv2
import face_recognition
import sqlite3
import numpy as np
import webbrowser
import tkinter as tk
from tkinter import messagebox

from database import load_known_faces

# Global variable to stop the camera feed
camera_active = True

# UPI Payment Redirection
def initiate_upi_payment(upi_id, amount, note):
    upi_link = f"upi://pay?pa={upi_id}&pn=Payment&tn={note}&am={amount}&cu=INR"
    webbrowser.open(upi_link)

# Show information about the detected person
def show_popup(name, upi_id):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Face Detected", f"Name: {name}\nUPI ID: {upi_id}\nRedirecting to payment app...")
    root.destroy()

# Confirmation to proceed with payment
def confirm_payment(name, upi_id):
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askyesno("Confirm Payment", f"Detected {name}.\nProceed with UPI payment to {upi_id}?")
    root.destroy()
    return response

# Function to close the camera
def close_camera():
    global camera_active
    camera_active = False
    print("Camera feed closed.")

# Handle manual window close event in OpenCV
def is_window_closed(window_name):
    try:
        return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1
    except:
        return True

# Start Face Recognition with enhanced UI and close button
def start_face_recognition():
    global camera_active
    camera_active = True

    # Ask for camera permission
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    response = messagebox.askyesno("Camera Permission", "Do you want to allow the camera for face detection?")
    root.destroy()

    if not response:
        print("Camera permission denied.")
        return

    # Create a Tkinter window for the "Close Camera" button
    control_window = tk.Tk()
    control_window.title("Control Panel")

    # Add a "Close Camera" button
    close_button = tk.Button(control_window, text="Close Camera", command=close_camera)
    close_button.pack(pady=10)

    # Position the control window
    control_window.geometry("200x100")

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Failed to open the webcam.")
        control_window.destroy()
        return

    known_faces, known_names, known_upi_ids = load_known_faces()

    if len(known_faces) == 0:
        print("No known faces loaded. Please register users.")
        video_capture.release()
        control_window.destroy()
        return

    # Name of the OpenCV window
    window_name = 'Live Face Recognition'

    while camera_active:
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to capture image from webcam.")
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"
            upi_id = None

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                upi_id = known_upi_ids[first_match_index]

                # Show Popup with Detected Information
                show_popup(name, upi_id)

                # Ask for confirmation to proceed with payment
                if confirm_payment(name, upi_id):
                    initiate_upi_payment(upi_id, 100, "Payment for services")
                    print(f"Redirecting to UPI payment for {name} (UPI ID: {upi_id})")
                else:
                    print("Payment cancelled.")

            # Draw rectangle around the face
            top, right, bottom, left = [v * 4 for v in face_location]  # Scale back up
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        # Display the frame
        cv2.imshow(window_name, frame)

        # Handle manual window close button
        if is_window_closed(window_name):
            print("Camera window closed manually.")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera and close OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()
    control_window.destroy()

if __name__ == '__main__':
    start_face_recognition()