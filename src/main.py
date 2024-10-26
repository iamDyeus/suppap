"""
Wallpaper Changer Application

This script serves as the entry point for the Wallpaper Changer application.
It sets up the scheduled task for changing wallpapers and handles command-line arguments.

Functions:
    parse_arguments(): Parse command-line arguments.
    main(): The main function that runs the application.

Classes:
    WallpaperManager: Manages the wallpaper changing functionality and scheduling.
"""

import argparse
from config import Config
from utils import Logger, OSCompatibilityChecker
from scheduler import TaskScheduler
from wallpaper_changer import WallpaperChanger

class WallpaperManager:
    """
    Manages the wallpaper changing functionality and scheduling.

    This class is responsible for setting up the application, scheduling tasks,
    and managing the wallpaper changing process.
    """

    def __init__(self):
        """Initialize the WallpaperManager with necessary components."""
        self.config = Config()
        self.logger = Logger()
        self.os = OSCompatibilityChecker.check_os_compatibility()
        self.scheduler = TaskScheduler(self.os)
        self.wallpaper_changer = WallpaperChanger()

    def setup(self):
        """Set up the wallpaper manager, including scheduling tasks and downloading initial images."""
        self.logger.log_message("Setting up wallpaper manager")
        self.scheduler.schedule_task(self.config.TASK_NAME, self.config.WALLPAPER_CHANGE_INTERVAL)
        downloaded_images = self.wallpaper_changer.image_manager.download_images(10)
        self.logger.log_message(f"Downloaded {len(downloaded_images)} images")
        if downloaded_images:
            self.wallpaper_changer.change_wallpaper()
        self.logger.log_message("Wallpaper manager setup complete")

    def cleanup(self):
        """Remove the application from startup and restore default wallpaper."""
        self.scheduler.remove_task(self.config.TASK_NAME)
        self.wallpaper_changer.restore_default_wallpaper()
        self.logger.log_message("Application removed from startup and default wallpaper restored.")

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Wallpaper Changer Application")
    parser.add_argument('--back-to-normal', action='store_true', help="Restore the default wallpaper and remove scheduled task")
    return parser.parse_args()

def main():
    """
    The main function that runs the Wallpaper Changer application.

    This function handles command-line arguments and sets up or cleans up the application.
    """
    args = parse_arguments()
    manager = WallpaperManager()

    if args.back_to_normal:
        manager.cleanup()
        print("Default wallpaper restored and scheduled task removed.")
    else:
        manager.setup()
        print("Wallpaper Changer set up successfully. The wallpaper will change periodically.")

if __name__ == "__main__":
    main()
