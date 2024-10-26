"""
Wallpaper Changer module for the Wallpaper Changer application.

This module contains the WallpaperChanger class, which is responsible for
changing the desktop wallpaper and restoring the default wallpaper.

Classes:
    WallpaperChanger: Handles changing and restoring desktop wallpapers.
"""

import subprocess
import ctypes
import os
from image_manager import ImageManager
from utils import OSCompatibilityChecker, Logger
from config import Config

class WallpaperChanger:
    """
    A class to handle changing and restoring desktop wallpapers.
    """

    def __init__(self):
        """Initialize the WallpaperChanger with necessary components."""
        self.image_manager = ImageManager()
        self.config = Config()
        self.logger = Logger()
        self.os = OSCompatibilityChecker.check_os_compatibility()
        self.default_wallpaper = self._get_default_wallpaper()

    def change_wallpaper(self):
        """
        Change the desktop wallpaper to a random image from the collection.
        If no images are available, download a new one.
        """
        image_path = self.image_manager.get_random_image()
        if not image_path:
            self.logger.log_message("No images found. Downloading a new image.")
            image_path = self.image_manager.download_image()
        
        if image_path:
            success = self.set_wallpaper(image_path)
            if success:
                self.log_wallpaper_change(image_path)
            else:
                self.logger.log_message(f"Failed to set wallpaper: {image_path}")
        else:
            self.logger.log_message("Failed to change wallpaper: No image available")

    def set_wallpaper(self, image_path):
        """
        Set the desktop wallpaper to the specified image.

        Args:
            image_path (str): The file path of the image to set as wallpaper.
        """
        try:
            if self.os == 'Windows':
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
            elif self.os == 'Darwin':  # macOS
                script = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
                subprocess.run(['osascript', '-e', script], check=True)
            else:  # Linux
                subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', f'file://{image_path}'], check=True)
            return True
        except Exception as e:
            self.logger.log_message(f"Error setting wallpaper: {e}")
            return False

    def log_wallpaper_change(self, image_path):
        """
        Log the wallpaper change event.

        Args:
            image_path (str): The file path of the new wallpaper image.
        """
        self.logger.log_message(f"Wallpaper changed to: {image_path}")

    def restore_default_wallpaper(self):
        """Restore the desktop wallpaper to the default image."""
        success = self.set_wallpaper(self.default_wallpaper)
        if success:
            self.logger.log_message(f"Restored default wallpaper: {self.default_wallpaper}")
        else:
            self.logger.log_message(f"Failed to restore default wallpaper: {self.default_wallpaper}")

    def _get_default_wallpaper(self):
        """
        Get the file path of the current default wallpaper.

        Returns:
            str: The file path of the default wallpaper.
        """
        if self.os == 'Windows':
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop")
            return winreg.QueryValueEx(key, "Wallpaper")[0]
        elif self.os == 'Darwin':  # macOS
            return subprocess.check_output(["osascript", "-e", 'tell app "finder" to get posix path of (get desktop picture as alias)']).decode().strip()
        else:  # Linux (assuming GNOME)
            return subprocess.check_output(["gsettings", "get", "org.gnome.desktop.background", "picture-uri"]).decode().strip().strip("'")
