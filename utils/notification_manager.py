import os

class NotificationManager:
    def __init__(self, app_name):
        self.app_name = app_name or 'IITK Fortinet Login'

    def show_notification(self, message, icon_path=None):
        if icon_path is None:
            icon_path = os.path.join(os.path.dirname(__file__), "img/icon.icns")  # Replace with your default icon path

        if os.name == 'posix' and os.uname().sysname == 'Darwin':  # Check if the OS is macOS
            try:
                # Use osascript to trigger a macOS notification
                os.system(f"osascript -e 'display notification \"{message}\" with title \"{self.app_name}\"'")
            except Exception as e:
                print(f"Error displaying macOS notification: {e}")
        else:
            # For non-macOS platforms, you can continue using plyer or other libraries
            from plyer import notification as plyer_notification
            plyer_notification.notify(
                title=self.app_name,
                message=message,
                app_name=self.app_name,
                timeout=5,
                app_icon=icon_path
            )

