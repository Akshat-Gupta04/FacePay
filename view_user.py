import sqlite3

# Function to view all users in the database
def view_registered_users():
    conn = sqlite3.connect('users.db')  # Connect to your database
    cursor = conn.cursor()

    # Execute SQL query to retrieve all user data
    cursor.execute("SELECT id, name, email, phone, upi_id FROM users")

    # Fetch all rows from the result
    users = cursor.fetchall()

    # Display the user details
    print("Registered Users:")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Phone: {user[3]}, UPI ID: {user[4]}")

    # Close the connection
    conn.close()

# Run the function
if __name__ == '__main__':
    view_registered_users()