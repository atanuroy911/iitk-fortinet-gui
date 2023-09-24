import os
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QDialog, qApp, QMessageBox, \
    QTabWidget, \
    QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
import winreg as reg


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowModality(Qt.ApplicationModal)  # Make the settings window modal
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # Make the settings window stay on top

        # Load last saved settings
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle("Settings")

        # Calculate the window's position to center it on the screen
        window_width = 400
        window_height = 200
        x = (qApp.desktop().screenGeometry().width() - window_width) // 2
        y = (qApp.desktop().screenGeometry().height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

        layout = QVBoxLayout()

        # Create a tab widget
        tab_widget = QTabWidget()

        # Create tabs
        startup_tab = QWidget()
        software_update_tab = QWidget()

        # Add tabs to the tab widget
        tab_widget.addTab(startup_tab, "Startup Options")
        tab_widget.addTab(software_update_tab, "Software Update")

        # Add the tab widget to the layout
        layout.addWidget(tab_widget)

        # Create widgets for the Startup Options tab
        startup_layout = QVBoxLayout()
        self.startup_checkbox = QCheckBox("Start automatically at startup")
        self.minimized_checkbox = QCheckBox("Start minimized")
        startup_layout.addWidget(self.startup_checkbox)
        startup_layout.addWidget(self.minimized_checkbox)
        startup_tab.setLayout(startup_layout)

        # Create widgets for the Software Update tab
        update_layout = QVBoxLayout()

        # Center align the widgets in the layout
        update_layout.setAlignment(Qt.AlignHCenter)

        update_url_label = QLabel("Update URL:")
        self.update_url_edit = QLineEdit()
        update_layout.addWidget(update_url_label)
        update_layout.addWidget(self.update_url_edit)

        # Create a horizontal layout for the Check for Update button
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignHCenter)

        check_update_button = QPushButton("Check for Update")
        check_update_button.clicked.connect(self.check_update)
        check_update_button.setStyleSheet("""
                QPushButton {
                    background-color: #155e75; /* Green background color */
                    color: white; /* White text color */
                    padding: 10px 20px; /* Padding (top/bottom, left/right) */
                    border: none; /* No border */
                    min-width: 100px; /* Set minimum width */
                }
                QPushButton:hover {
                    background-color: #164e63; /* Darker green color on hover */
                }
                QPushButton:pressed {
                    background-color: #083344; /* Darker green color when pressed */
                }
            """)
        button_layout.addWidget(check_update_button)

        update_layout.addLayout(button_layout)  # Add the button layout to the main layout

        software_update_tab.setLayout(update_layout)

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet("""
                QPushButton {
                    background-color: #065f46; /* Green background color */
                    color: white; /* White text color */
                    padding: 10px 20px; /* Padding (top/bottom, left/right) */
                    border: none; /* No border */
                }
                QPushButton:hover {
                    background-color: #064e3b; /* Darker green color on hover */
                }
                QPushButton:clicked {
                    background-color: #022c22; /* Darker green color on hover */
                }
            """)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def load_settings(self):
        try:
            # Initialize the SQLite database connection
            conn = sqlite3.connect("settings.db")
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
                self.startup_checkbox.setChecked(bool(start_at_startup))
                self.minimized_checkbox.setChecked(bool(start_minimized))
                self.update_url_edit.setText(str(update_url))

            # Close the database connection
            conn.close()

        except sqlite3.Error as e:
            QMessageBox.warning(self, "SQLite Error", f"SQLite error: {str(e)}", QMessageBox.Ok)

    def save_settings(self):
        try:
            # Initialize the SQLite database connection
            conn = sqlite3.connect("settings.db")
            cursor = conn.cursor()

            # Create a settings table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                                id INTEGER PRIMARY KEY,
                                start_at_startup INTEGER,
                                start_minimized INTEGER,
                                update_url TEXT)''')

            # Get the checkbox states and update URL
            start_at_startup = int(self.startup_checkbox.isChecked())
            start_minimized = int(self.minimized_checkbox.isChecked())
            update_url = self.update_url_edit.text()  # Get the update URL from the QLineEdit

            # Insert or update settings in the database (assuming there's only one row)
            cursor.execute('''INSERT OR REPLACE INTO settings (id, start_at_startup, start_minimized, update_url)
                              VALUES (1, ?, ?, ?)''', (start_at_startup, start_minimized, update_url))

            # Commit changes and close the database connection
            conn.commit()
            conn.close()

            key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_path = os.path.abspath(sys.argv[0])

            if start_at_startup:
                # Add the application to startup
                with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE) as registry_key:
                    reg.SetValueEx(registry_key, "YourAppName", 0, reg.REG_SZ, app_path)
            else:
                # Remove the application from startup
                try:
                    with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE) as registry_key:
                        reg.DeleteValue(registry_key, "YourAppName")
                except FileNotFoundError:
                    pass

            QMessageBox.information(self, "Settings Saved", "Settings have been saved.", QMessageBox.Ok)

        except sqlite3.Error as e:
            QMessageBox.warning(self, "SQLite Error", f"SQLite error: {str(e)}", QMessageBox.Ok)

    def check_update(self):
        QMessageBox.information(self, "Update", "No Updates Available", QMessageBox.Ok)
        # Add code to check for software updates using the update URL
        # You can use self.update_url_edit.text() to get the URL entered by the user
        # Display the update status to the user using QMessageBox or another widget