import sqlite3
import os
import platform


basedir = os.path.expanduser('~/.iitkfauth')
os.makedirs(basedir, exist_ok=True)
credential_dir = os.path.join(basedir, 'credentials.db')

# Function to create or connect to the credentials database
def initialize_database():
    conn = sqlite3.connect(credential_dir)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
        """
    )
    conn.commit()
    conn.close()


# Function to check if credentials exist in the database
def check_credentials_exist():
    conn = sqlite3.connect(credential_dir)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credentials")
    rows = cursor.fetchall()
    conn.close()
    return len(rows) > 0


# Function to retrieve saved credentials from the database
def get_saved_credentials():
    conn = sqlite3.connect(credential_dir)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM credentials")
    row = cursor.fetchone()
    conn.close()
    return row if row else (None, None)


# Function to save credentials to the database
def save_credentials(username, password):
    conn = sqlite3.connect(credential_dir)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM credentials")
    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


# Function to prompt for new credentials and handle overwrite confirmation
def prompt_for_credentials():
    username, password = get_saved_credentials()

    if username is None and password is None:
        print("No saved credentials found. Please enter new credentials:")
    else:
        print("Saved credentials found. Do you want to update them? (yes/no)")
        choice = input().strip().lower()
        if choice != "yes":
            return username, password

    new_username = input("Username: ")
    new_password = input("Password: ")

    if (new_username, new_password) != (username, password):
        print("New credentials differ from the saved ones. Do you want to overwrite them? (yes/no)")
        choice = input().strip().lower()
        if choice != "yes":
            return username, password

    save_credentials(new_username, new_password)
    return new_username, new_password

# # Initialize the database
# initialize_database()
#
# # Check if credentials exist in the database
# if not check_credentials_exist():
#     username, password = prompt_for_credentials()
#     save_credentials(username, password)
# else:
#     username, password = get_saved_credentials()
#
# # Now you can use the retrieved or entered username and password in your application.
# print("Username:", username)
# print("Password:", password)
