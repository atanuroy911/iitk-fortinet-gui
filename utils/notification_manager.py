import os
from plyer import notification as plyer_notification

basedir = os.path.dirname(__file__)


class NotificationManager:
    def __init__(self, app_name):
        self.app_name = app_name

    def show_notification(self, message, icon_path=None):
        icon_path = icon_path or os.path.join(basedir, "img/icon.ico")  # Replace with the path to your default icon
        plyer_notification.notify(
            title=self.app_name,
            message=message,
            app_name=self.app_name,
            timeout=5,
            app_icon=icon_path
        )

