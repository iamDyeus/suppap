"""
Configuration settings for the Wallpaper Changer application.

This module contains the Config class which stores all configuration variables
for the application, including wallpaper change interval, image folder location,
and OS-specific commands for changing wallpapers.

Classes:
    Config: Stores all configuration settings for the application.
"""

import os


class Config:
    """
    A class to store all configuration settings for the Wallpaper Changer application.
    """
   # MIN_SCORE = 100
    WALLPAPER_CHANGE_INTERVAL = 60  # 1 hour in seconds
    IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'images')
    SUBREDDITS = ['EarthPorn', 'CityPorn', 'SpacePorn', 'Art']

    # OS-specific configurations
    WINDOWS_COMMAND = 'REG ADD "HKCU\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "{}" /f'
    MACOS_COMMAND = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"{}\"'"
    LINUX_COMMAND = "gsettings set org.gnome.desktop.background picture-uri file://{}"

    TASK_NAME = "WallpaperChanger"

    def __init__(self):
        """Initialize the Config class and create the image folder if it doesn't exist."""
        if not os.path.exists(self.IMAGE_FOLDER):
            os.makedirs(self.IMAGE_FOLDER)
