"""A script to automatically login to fortinet firewall captive portal.

Given a username and password this script automatically monitors the network and logs in to the fortinet captive portal
when needed. It also send keepalive requests periodically to maintain the login.
"""
import os
import sys
import subprocess
import logging
import signal
import platform  # Import the platform module to check the OS

import requests
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QMessageBox, QHBoxLayout,
    QSpacerItem, QSizePolicy, QSplashScreen, QSystemTrayIcon, QMenu, QDesktopWidget, QLayout
)
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QThread, pyqtSignal
from about_window import AboutWindow
from db import initialize_database, get_saved_credentials, check_credentials_exist, \
    save_credentials
from settings_window import SettingsWindow
from utils.notification_manager import NotificationManager

if platform.system() == "Windows":
    import ctypes

    myappid = u'iitk.fortinet.iotlab.atanuroy911'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

main_window = None

basedir = os.path.dirname(__file__)

log_out_url = 'https://gateway.iitk.ac.in:1003/logout?a'

app_name = "IITK Fortinet Login App"
# Provide the path to the icon you want to use
icon_path = os.path.join(basedir, "img/icon.ico")  # Replace with your icon path


class FortinetLoginApp(QWidget):

    def __init__(self, app, username, password):
        super().__init__()

        self.app = app
        self.username = username
        self.password = password
        self.init_ui()
        self.first_login = True  # Add a flag to track the first login

    # Inside your FortinetLoginApp class, modify the init_ui method as follows:
    def init_ui(self):
        global log_text, app_name

        layout = QVBoxLayout()
        # Determine the screen size
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()
        print(screen_height)
        print(screen_width)
        # Create a QHBoxLayout for the logos
        logo_layout = QHBoxLayout()
        # Add an empty spacer to push the first logo to the right
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        logo_layout.addSpacerItem(spacer)
        # Load and display the first logo on the left
        logo1 = QLabel()
        pixmap1 = QPixmap(os.path.join(basedir, "img/logo1.png"))  # Replace with the actual path to your first logo

        # Resize the first logo (e.g., to a width of 100 pixels)
        pixmap1 = pixmap1.scaledToWidth(int(screen_height * 0.12), Qt.SmoothTransformation)

        logo1.setPixmap(pixmap1)
        logo_layout.addWidget(logo1)

        # Add an empty spacer to push the first logo to the right
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        logo_layout.addSpacerItem(spacer)

        # Load and display the second logo on the right
        logo2 = QLabel()
        pixmap2 = QPixmap(
            os.path.join(basedir, "img/Fortinet_logo.png"))  # Replace with the actual path to your second logo

        # Resize the second logo (e.g., to a width of 100 pixels)
        pixmap2 = pixmap2.scaledToWidth(int(screen_height * 0.12), Qt.SmoothTransformation)

        logo2.setPixmap(pixmap2)
        logo_layout.addWidget(logo2)
        # Add an empty spacer to push the first logo to the right
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        logo_layout.addSpacerItem(spacer)
        # Add the logo layout to the main layout
        layout.addLayout(logo_layout)

        # Create a container for the username and password section
        input_container = QVBoxLayout()
        input_container.setSizeConstraint(QLayout.SetFixedSize)  # This sets the size to be fixed

        username_label = QLabel("Username:")
        username_label.setFixedHeight(20)
        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(20)
        # Style the username input field
        self.username_input.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        min-height: 20px; /* Set the desired fixed width */
                        max-height: 20px; /* Set the desired fixed width */
                    }
                """)

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        password_label.setFixedHeight(20)
        self.password_input.setFixedHeight(20)

        # Style the password input field
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        min-height: 20px; /* Set the desired fixed width */
                        max-height: 20px; /* Set the desired fixed width */
                    }
                """)

        input_container.addWidget(username_label)
        input_container.addWidget(self.username_input)
        input_container.addWidget(password_label)
        input_container.addWidget(self.password_input)


        layout.addLayout(input_container)

        self.run_button = QPushButton("Start Service")
        self.stop_button = QPushButton("Stop Service")
        self.save_info_button = QPushButton("Save Info")

        if self.username:
            self.save_info_button.setText("Update Info")

        # Create a "Show Log" button
        self.clear_log_button = QPushButton("Clear Log")

        # Style the buttons
        button_style = """
                    QPushButton {
                        padding: 8px 16px;
                        background-color: #4CAF50; /* Green background */
                        color: white;
                        border: none;
                        border-radius: 4px;
                    }

                    QPushButton:hover {
                        background-color: #45a049; /* Darker green on hover */
                    }

                    QPushButton:pressed {
                        background-color: #367d41; /* Slightly darker green when pressed */
                    }
                    QPushButton:disabled { color: gray; background-color: lightgray;}
                """

        clear_log_button_style = """
                            QPushButton {
                                padding: 8px 16px;
                                background-color: #4C4F50; /* Green background */
                                color: white;
                                border: none;
                                border-radius: 4px;
                            }

                            QPushButton:hover {
                                background-color: #454049; /* Darker green on hover */
                            }

                            QPushButton:pressed {
                                background-color: #364d41; /* Slightly darker green when pressed */
                            }
                            QPushButton:disabled { color: gray; background-color: lightgray;}
                        """

        self.run_button.setStyleSheet(button_style)
        self.stop_button.setStyleSheet(button_style)
        self.save_info_button.setStyleSheet(button_style)
        self.clear_log_button.setStyleSheet(clear_log_button_style)

        self.log_text = QTextEdit()
        self.log_text.setFixedHeight(int(screen_height*0.1))
        self.log_text.setReadOnly(True)
        self.log_text.setVisible(True)  # Initially hide the log section



        layout.addWidget(self.run_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.save_info_button)
        layout.addWidget(self.log_text)
        layout.addWidget(self.clear_log_button)

        # Create a QHBoxLayout for the icons
        icon_layout = QHBoxLayout()
        icon_layout.setAlignment(Qt.AlignRight)

        # Create a QPushButton for the settings icon
        settings_button = QPushButton()
        settings_pixmap = QPixmap(
            os.path.join(basedir, "img/settings_icon.png"))  # Replace with the actual path to your settings icon
        settings_button.setIcon(QIcon(settings_pixmap))
        settings_button.setToolTip('Settings')
        settings_button.setIconSize(settings_pixmap.rect().size())

        # Apply styles for different button states
        settings_button.setStyleSheet("""
                    QPushButton {
                        border: none;
                        padding: 0;
                    }
                    QPushButton:hover {
                        background-color: #E0E0E0;
                    }
                    QPushButton:pressed {
                        background-color: #C0C0C0;
                    }
                """)

        # Create a QPushButton for the info icon
        info_button = QPushButton()
        info_pixmap = QPixmap(
            os.path.join(basedir, "img/info_icon.png"))  # Replace with the actual path to your info icon
        info_button.setIcon(QIcon(info_pixmap))
        info_button.setToolTip('Info')
        info_button.setIconSize(info_pixmap.rect().size())

        # Apply styles for different button states
        info_button.setStyleSheet("""
                    QPushButton {
                        border: none;
                        padding: 0;
                    }
                    QPushButton:hover {
                        background-color: #E0E0E0;
                    }
                    QPushButton:pressed {
                        background-color: #C0C0C0;
                    }
                """)

        # Create a QPushButton for the info icon
        quit_button = QPushButton()
        quit_pixmap = QPixmap(
            os.path.join(basedir, "img/quit_icon.png"))  # Replace with the actual path to your info icon
        quit_button.setIcon(QIcon(quit_pixmap))
        quit_button.setToolTip('Exit App')
        quit_button.setIconSize(quit_pixmap.rect().size())

        # Apply styles for different button states
        quit_button.setStyleSheet("""
                            QPushButton {
                                border: none;
                                padding: 0;
                            }
                            QPushButton:hover {
                                background-color: #E0E0E0;
                            }
                            QPushButton:pressed {
                                background-color: #C0C0C0;
                            }
                        """)

        icon_layout.addWidget(settings_button)
        icon_layout.addWidget(info_button)
        icon_layout.addWidget(quit_button)

        layout.addLayout(icon_layout)

        self.run_button.clicked.connect(self.start_script)
        self.stop_button.clicked.connect(self.stop_script)
        self.save_info_button.clicked.connect(self.save_info)

        self.clear_log_button.clicked.connect(self.clear_log)

        self.settings_window = SettingsWindow()  # Create the settings window
        settings_button.clicked.connect(self.show_settings)

        self.about_window = AboutWindow()  # Create about window
        info_button.clicked.connect(self.show_about)

        quit_button.clicked.connect(self.exit_application)
        self.setLayout(layout)

        self.running = False
        self.stop_button.setEnabled(False)  # Disable the "Stop Service" button initially

        self.username_input.setText(self.username)
        self.password_input.setText(self.password)

        # Create a QSystemTrayIcon and set its icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join(basedir, "img/icon.png")))  # Replace with your tray icon path
        self.tray_icon.setToolTip("IITK Fortinet Login App")
        # Create a context menu for the system tray icon
        self.tray_menu = QMenu()
        show_action = self.tray_menu.addAction("Show Application")
        self.start_action = self.tray_menu.addAction("Start Service")
        self.stop_action = self.tray_menu.addAction("Stop Service")
        self.stop_action.setEnabled(False)
        exit_action = self.tray_menu.addAction("Exit")

        self.tray_icon.setContextMenu(self.tray_menu)

        # Connect actions to functions
        show_action.triggered.connect(self.show_application)
        self.start_action.triggered.connect(self.start_script)
        self.stop_action.triggered.connect(self.stop_script)
        exit_action.triggered.connect(self.exit_application)

        # Handle double-click event
        self.tray_icon.activated.connect(self.trayIconActivated)

        # Show the system tray icon
        self.tray_icon.show()

        if screen_width == 1920:
            window_width = int(screen_width * 0.2)
            window_height = int(screen_height * 0.5)
        elif screen_width == 1680:
            window_width = int(screen_width * 0.2)  # Different rule for 1366x768
            window_height = int(screen_height * 0.5)  # Different rule for 1366x768
        elif screen_width == 1600:
            window_width = int(screen_width * 0.22)  # Different rule for 1366x768
            window_height = int(screen_height * 0.55)  # Different rule for 1366x768
        elif screen_width == 1440:
            window_width = int(screen_width * 0.22)  # Different rule for 1366x768
            window_height = int(screen_height * 0.55)  # Different rule for 1366x768
        elif screen_width == 1400:
            window_width = int(screen_width * 0.23)  # Different rule for 1366x768
            window_height = int(screen_height * 0.50)  # Different rule for 1366x768
        elif screen_width == 1366:
            window_width = int(screen_width * 0.25)  # Different rule for 1366x768
            window_height = int(screen_height * 0.62)  # Different rule for 1366x768
        elif screen_width == 1360:
            window_width = int(screen_width * 0.25)  # Different rule for 1366x768
            window_height = int(screen_height * 0.62)  # Different rule for 1366x768
        elif screen_width == 1280:
            if screen_height == 768:
                window_width = int(screen_width * 0.2)  # Different rule for 1280x720
                window_height = int(screen_height * 0.6)
            elif screen_height == 720:
                window_width = int(screen_width * 0.2)
                window_height = int(screen_height * 0.65)
            elif screen_height == 960:
                window_width = int(screen_width * 0.2)
                window_height = int(screen_height * 0.52)
            elif screen_height == 1024:
                window_width = int(screen_width * 0.23)
                window_height = int(screen_height * 0.53)
            else:
                window_width = int(screen_width * 0.2)  # Different rule for 1280x720
                window_height = int(screen_height * 0.6)  # Different rule for 1280x720

        elif screen_width == 1024:
            window_width = int(screen_width * 0.23)  # Different rule for 1366x768
            window_height = int(screen_height * 0.62)  # Different rule for 1366x768
        elif screen_width == 800:
            window_width = int(screen_width * 0.25)  # Different rule for 1366x768
            window_height = int(screen_height * 0.75)  # Different rule for 1366x768


        else:
            # Default rules for other resolutions
            window_width = int(screen_width * 0.2)
            window_height = int(screen_height * 0.55)

        # Set the window size
        self.setFixedSize(window_width, window_height)

        # Define Auto Layout constraints for the central widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.setMinimumSize(int(screen_width * 0.2), int(screen_height * 0.5))  # Set a minimum size

        # Calculate the window position to center it on the screen
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set the window position
        self.move(x_position, y_position)

        self.script_thread = ScriptThread(os.path.join(basedir, 'utils/authenticator.py'),
                                          username=self.username_input.text(), password=self.password_input.text())
        self.script_thread.log_signal.connect(self.append_log)

        self.username_input.textChanged.connect(self.redeclare_script_thread)
        self.password_input.textChanged.connect(self.redeclare_script_thread)

    def redeclare_script_thread(self):
        self.script_thread = ScriptThread(os.path.join(basedir, 'utils/authenticator.py'),
                                          username=self.username_input.text(), password=self.password_input.text())
        self.script_thread.log_signal.connect(self.append_log)

    def show_application(self):
        self.show()
        # self.tray_icon.setVisible(False)  # Hide the system tray icon when the app is shown

    def trayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            # self.tray_icon.setVisible(False)  # Hide the system tray icon when the app is shown

    def exit_application(self):
        self.stop_script()  # Stop the script if running
        self.app.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.setVisible(True)
        self.show_notification()  # Show a system notification when minimized

    def show_notification(self):
        # Create an instance of NotificationManager
        manager = NotificationManager(app_name)
        # Call the show_notification method
        manager.show_notification("Running in Background. Check System Tray", icon_path)

    def start_script(self):
        # Disable the "Start Service" button when it's clicked
        if not self.username_input.text() or not self.password_input.text():
            QMessageBox.warning(
                self,
                "No/Invalid Input",
                "Please Enter Your IITK WiFi Credentials",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
            )
            self.show()
        else:
            if not self.username or not self.password:
                self.save_info()
            self.run_button.setEnabled(False)
            self.start_action.setEnabled(False)
            self.log_text.clear()
            self.script_thread.start()
            # Enable the "Stop Service" button
            self.stop_button.setEnabled(True)
            self.stop_action.setEnabled(True)

            self.running = True

    # TODO: Unexpected Quit Handle - DONE
    def stop_script(self):
        if hasattr(self, 'script_thread') and self.script_thread.isRunning():
            self.script_thread.stop()
            # Enable the "Start Service" button when the service is stopped
            self.run_button.setEnabled(True)
            self.start_action.setEnabled(True)

            # Disable the "Stop Service" button
            self.stop_button.setEnabled(False)
            self.stop_action.setEnabled(False)

            self.running = False

    def append_log(self, log_message, sig):
        self.log_text.append(log_message)
        if not sig:
            self.stop_button.setEnabled(False)
            self.run_button.setEnabled(True)

    def clear_log(self):
        self.log_text.clear()

    # def toggle_log_visibility(self):
    #     # Toggle the visibility of the log section
    #     if self.log_text.isVisible():
    #         # Determine the screen size
    #         screen = QDesktopWidget().screenGeometry()
    #         screen_width, screen_height = screen.width(), screen.height()
    #
    #         # Calculate the window size as a percentage of the screen size (e.g., 80% width and 60% height)
    #         window_width = int(screen_width * 0.2)
    #         window_height = int(screen_height * 0.3)
    #
    #         # Set the window size
    #         self.setFixedSize(window_width, window_height)
    #
    #         self.show_log_button.setText('Show Log')
    #     else:
    #         # Determine the screen size
    #         screen = QDesktopWidget().screenGeometry()
    #         screen_width, screen_height = screen.width(), screen.height()
    #
    #         # Calculate the window size as a percentage of the screen size (e.g., 80% width and 60% height)
    #         window_width = int(screen_width * 0.2)
    #         window_height = int(screen_height * 0.5)
    #
    #         # Set the window size
    #         self.setFixedSize(window_width, window_height)
    #
    #         self.show_log_button.setText('Hide Log')
    #     self.log_text.setVisible(not self.log_text.isVisible())

    def save_info(self):
        # You can implement the logic to save the entered username and password here
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            result = QMessageBox.warning(
                None,
                "Save Credentials",
                "Are you sure you want to save credentials ?",
                buttons=QMessageBox.Ok | QMessageBox.Cancel,
                defaultButton=QMessageBox.Ok,
            )
            if result == QMessageBox.Ok:
                save_credentials(username, password)
                self.username = username
                self.password = password
                QMessageBox.information(
                    None,
                    "Information",
                    "Credentials Saved",
                    buttons=QMessageBox.Ok,
                    defaultButton=QMessageBox.Ok,
                )

        else:
            QMessageBox.warning(
                None,
                "No Credentials",
                "Please recheck the form",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
            )

    def log_to_widget(self, msg):
        log_message = f"{msg}"
        self.log_text.append(log_message)

    def show_settings(self):
        self.settings_window.show()

        # Disable the main window while the settings window is open
        # self.setEnabled(False)

    def show_about(self):
        self.about_window.show()


def show_splash_screen(app):
    app.processEvents()  # Allow the splash screen to update
    splash_pix = QPixmap(os.path.join(basedir, "img/Splash.png"))  # Replace with the path to your splash image
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    # Simulate some time-consuming initialization process
    # You can replace this with your actual initialization code
    for i in range(1, 10000):
        splash.showMessage(f"Loading... ", Qt.AlignBottom | Qt.AlignRight, Qt.white)
        app.processEvents()
        # QTimer.singleShot(2000, lambda: None)  # Simulate a 2-second delay

    # Close the splash screen and show the main window
    splash.finish(main_window)


class ScriptThread(QThread):
    log_signal = pyqtSignal(str, bool)
    stop_signal = pyqtSignal()

    def __init__(self, script_path, username, password):
        super().__init__()
        self.script_path = script_path
        self.username = username
        self.password = password
        self.stopped = False

    def run(self):
        self.log_signal.emit(f'Logging with username {self.username}', True)
        try:
            cmd = ["python", self.script_path, "-u", self.username, "-p", self.password]

            # Check if the OS is not Windows (assuming Unix-like OS supports os.setsid)
            if platform.system() != "Windows":
                self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                preexec_fn=os.setsid)
            else:
                self.process = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            for line in iter(self.process.stdout.readline, b''):
                log_message = line.decode("utf-8").strip()
                # print(log_message)
                self.log_signal.emit(log_message, True)

                if self.stopped:
                    break

            self.process.stdout.close()
            self.process.wait()
        except Exception as e:
            self.log_signal.emit(f"Error: {str(e)}", False)
            error_notification(str(e))

        finally:
            self.log_signal.emit("Script finished.", False)

    def stop(self):
        self.stopped = True

        # Check if the OS is not Windows (assuming Unix-like OS supports os.killpg)
        try:
            if platform.system() != "Windows":
                os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
            else:
                # Send a Ctrl+C signal to the subprocess
                self.process.terminate()
                try:
                    response = requests.get(log_out_url, headers={'User-Agent': 'Mozilla/5.0'})
                except:
                    self.log_signal.emit(f'Error in opening url: {log_out_url}.', False)

                if response.status_code == 200:
                    self.log_signal.emit('Successfully logged out.', True)


        except Exception as e:
            self.log_signal.emit(f"Error while Quitting: {str(e)}", False)
            error_notification(str(e))


def error_notification(msg):
    print(msg)
    if 'Invalid user' in msg:
        QMessageBox.critical(
            None,
            "Invalid Username/Password",
            "Please Check Your Username & Password",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
        )
    else:
        QMessageBox.critical(
            None,
            "ERROR",
            f"Check Log",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
        )


def main():
    app = QApplication(sys.argv)

    app_icon = QIcon(os.path.join(basedir, "img/icon.ico"))  # Replace with the path to your application icon
    app.setWindowIcon(app_icon)

    app.setApplicationName(app_name)
    # Setup logging.
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    # Show the splash screen and wait for some time
    show_splash_screen(app)

    # Initialize the database
    initialize_database()

    username, password = None, None

    if not check_credentials_exist():
        QMessageBox.warning(
            None,
            "No Credentials Found",
            "Please Enter your IITK Login Username and Password in the next window and save it",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
        )
    else:
        username, password = get_saved_credentials()

    global main_window
    # print(username, password)
    main_window = FortinetLoginApp(app, username, password)
    main_window.setWindowTitle("IITK Fortinet Captive Portal Login")

    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
