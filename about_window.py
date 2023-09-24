import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, qApp

basedir = os.path.dirname(__file__)

class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowModality(Qt.ApplicationModal)  # Make the settings window modal
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # Make the settings window stay on top

    def init_ui(self):
        self.setWindowTitle("About")
        # Calculate the window's position to center it on the screen
        window_width = 400
        window_height = 200
        x = (qApp.desktop().screenGeometry().width() - window_width) // 2
        y = (qApp.desktop().screenGeometry().height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)
        layout = QVBoxLayout()

        # Add the logo as an image
        logo_label = QLabel(self)
        pixmap = QPixmap(os.path.join(basedir, "img/lab_logo.png"))  # Replace with the path to your logo image
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(logo_label)

        label = QLabel("Author: Atanu Shuvam Roy")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")

        layout.addWidget(label)

        software_label = QLabel("IoT Vision Lab | Dept. of CSE | IIT Kanpur")
        software_label.setAlignment(Qt.AlignCenter)
        software_label.setStyleSheet("font-size: 14px; color: #666;")

        layout.addWidget(software_label)

        # Add a clickable link to a website
        website_label = QLabel('<a href="https://pbagade0.wixsite.com/priyanka">Visit our website</a>')
        website_label.setAlignment(Qt.AlignCenter)
        website_label.setOpenExternalLinks(True)  # Make the link clickable
        website_label.setStyleSheet("font-size: 14px; color: blue;")

        layout.addWidget(website_label)

        version_label = QLabel("Version: 1.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 14px; color: #666;")

        layout.addWidget(version_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet("background-color: #007acc; color: white; font-weight: bold;")
        ok_button.setCursor(Qt.PointingHandCursor)  # Change cursor to a pointing hand

        layout.addWidget(ok_button)

        self.setLayout(layout)


class MainApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Main Application")

        layout = QVBoxLayout()

        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        about_button.setStyleSheet("background-color: #007acc; color: white; font-weight: bold;")
        about_button.setCursor(Qt.PointingHandCursor)  # Change cursor to a pointing hand

        layout.addWidget(about_button)

        self.setLayout(layout)

    def show_about(self):
        about_window = AboutWindow()
        about_window.exec_()



