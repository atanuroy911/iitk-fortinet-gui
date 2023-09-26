import os
import sqlite3

from PyQt5.QtWidgets import QMessageBox

basedir = os.path.expanduser('~/.iitkfauth')
os.makedirs(basedir, exist_ok=True)
settings_dir = os.path.join(basedir, 'settings.db')

def get_settings():
    try:
        # Initialize the SQLite database connection
        conn = sqlite3.connect(settings_dir)
        cursor = conn.cursor()

        # Create a settings table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                            id INTEGER PRIMARY KEY,
                            start_at_startup INTEGER,
                            start_minimized INTEGER,
                            update_url TEXT)''')

        # Fetch the last saved settings (assuming there's only one row)
        cursor.execute("SELECT start_at_startup, start_minimized, update_url FROM settings WHERE id = 1")
        result = cursor.fetchone()

        if result:
            start_at_startup, start_minimized, update_url = result

            # Close the database connection
            conn.close()
            return start_at_startup, start_minimized, update_url

        conn.close()

    except sqlite3.Error as e:
        QMessageBox.warning(self, "SQLite Error", f"SQLite error: {str(e)}", QMessageBox.Ok)
