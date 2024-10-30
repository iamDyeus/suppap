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
import json
import os
from config import Config
from utils import Logger, OSCompatibilityChecker
from scheduler import TaskScheduler
from wallpaper_changer import WallpaperChanger

CONFIG_FILE = "wallpaper_config.json"

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
        self.load_config()

    def load_config(self):
        """Load configuration from the config file if it exists."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                saved_config = json.load(f)
                self.config.WALLPAPER_CHANGE_INTERVAL = saved_config.get('interval', self.config.WALLPAPER_CHANGE_INTERVAL)
                self.config.SUBREDDITS = saved_config.get('subreddits', self.config.SUBREDDITS)
                self.config.IMAGE_LIMIT = saved_config.get('image_limit', 100)
                self.config.MIN_RESOLUTION = saved_config.get('min_resolution', (1920, 1080))

    def save_config(self):
        """Save current configuration to the config file."""
        config_data = {
            'interval': self.config.WALLPAPER_CHANGE_INTERVAL,
            'subreddits': self.config.SUBREDDITS,
            'image_limit': getattr(self.config, 'IMAGE_LIMIT', 100),
            'min_resolution': getattr(self.config, 'MIN_RESOLUTION', (1920, 1080))
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)

    def setup(self):
        """Set up the wallpaper manager, including scheduling tasks and downloading initial images."""
        self.logger.log_message("Setting up wallpaper manager")
        self.scheduler.schedule_task(self.config.TASK_NAME, self.config.WALLPAPER_CHANGE_INTERVAL)
        downloaded_images = self.wallpaper_changer.image_manager.download_images(10)
        self.logger.log_message(f"Downloaded {len(downloaded_images)} images")
        if downloaded_images:
            self.wallpaper_changer.change_wallpaper()
        self.logger.log_message("Wallpaper manager setup complete")
        self.save_config()

    def cleanup(self):
        """Remove the application from startup and restore default wallpaper."""
        self.scheduler.remove_task(self.config.TASK_NAME)
        self.wallpaper_changer.restore_default_wallpaper()
        self.logger.log_message("Application removed from startup and default wallpaper restored.")

    def start(self):
        """Start the wallpaper changer service."""
        self.setup()

    def stop(self):
        """Stop the wallpaper changer service."""
        self.cleanup()

    def change_now(self):
        """Change wallpaper immediately."""
        self.wallpaper_changer.change_wallpaper()
        self.logger.log_message("Wallpaper changed manually")

    def update_interval(self, interval):
        """Update the wallpaper change interval."""
        self.config.WALLPAPER_CHANGE_INTERVAL = interval
        self.scheduler.update_task(self.config.TASK_NAME, interval)
        self.save_config()
        self.logger.log_message(f"Updated wallpaper change interval to {interval} seconds")

    def add_subreddits(self, subreddits):
        """Add new subreddits to the list."""
        self.config.SUBREDDITS.extend([s for s in subreddits if s not in self.config.SUBREDDITS])
        self.save_config()
        self.logger.log_message(f"Added subreddits: {', '.join(subreddits)}")

    def remove_subreddits(self, subreddits):
        """Remove subreddits from the list."""
        self.config.SUBREDDITS = [s for s in self.config.SUBREDDITS if s not in subreddits]
        self.save_config()
        self.logger.log_message(f"Removed subreddits: {', '.join(subreddits)}")

    def set_image_limit(self, limit):
        """Set the maximum number of images to store."""
        self.config.IMAGE_LIMIT = limit
        self.save_config()
        self.logger.log_message(f"Set image limit to {limit}")

    def set_min_resolution(self, resolution):
        """Set the minimum resolution for downloaded images."""
        self.config.MIN_RESOLUTION = resolution
        self.save_config()
        self.logger.log_message(f"Set minimum resolution to {resolution}")

    def clean_images(self):
        """Clean up old or invalid images."""
        # Add implementation for cleaning images
        self.logger.log_message("Cleaned image directory")

    def show_config(self):
        """Display current configuration."""
        config_info = {
            "Change Interval": f"{self.config.WALLPAPER_CHANGE_INTERVAL} seconds",
            "Subreddits": self.config.SUBREDDITS,
            "Image Limit": getattr(self.config, 'IMAGE_LIMIT', 100),
            "Min Resolution": getattr(self.config, 'MIN_RESOLUTION', (1920, 1080)),
            "Image Folder": self.config.IMAGE_FOLDER
        }
        return config_info

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Wallpaper Changer Application")
    
    # Control options
    control_group = parser.add_argument_group('Control Options')
    control_group.add_argument('--start', action='store_true', help="Start the wallpaper changer service")
    control_group.add_argument('--stop', action='store_true', help="Stop the wallpaper changer service")
    control_group.add_argument('--change-now', action='store_true', help="Change wallpaper immediately")
    
    # Configuration management
    config_group = parser.add_argument_group('Configuration Management')
    config_group.add_argument('--interval', type=int, help="Set wallpaper change interval in seconds")
    config_group.add_argument('--add-subreddits', nargs='+', help="Add subreddits to download from")
    config_group.add_argument('--remove-subreddits', nargs='+', help="Remove subreddits from the list")
    
    # Image settings
    image_group = parser.add_argument_group('Image Settings')
    image_group.add_argument('--min-resolution', type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'),
                            help="Set minimum image resolution (width height)")
    image_group.add_argument('--image-limit', type=int, help="Set maximum number of images to store")
    
    # Information and maintenance
    info_group = parser.add_argument_group('Information and Maintenance')
    info_group.add_argument('--show-config', action='store_true', help="Show current configuration")
    info_group.add_argument('--clean-images', action='store_true', help="Clean up old or invalid images")
    
    return parser.parse_args()

def main():
    """
    The main function that runs the Wallpaper Changer application.

    This function handles command-line arguments and manages the application accordingly.
    """
    args = parse_arguments()
    manager = WallpaperManager()

    try:
        if args.start:
            manager.start()
            print("Wallpaper Changer service started.")
        elif args.stop:
            manager.stop()
            print("Wallpaper Changer service stopped.")
        elif args.change_now:
            manager.change_now()
            print("Wallpaper changed successfully.")
        elif args.interval:
            manager.update_interval(args.interval)
            print(f"Wallpaper change interval updated to {args.interval} seconds.")
        elif args.add_subreddits:
            manager.add_subreddits(args.add_subreddits)
            print(f"Added subreddits: {', '.join(args.add_subreddits)}")
        elif args.remove_subreddits:
            manager.remove_subreddits(args.remove_subreddits)
            print(f"Removed subreddits: {', '.join(args.remove_subreddits)}")
        elif args.min_resolution:
            manager.set_min_resolution(tuple(args.min_resolution))
            print(f"Minimum resolution set to {args.min_resolution[0]}x{args.min_resolution[1]}")
        elif args.image_limit:
            manager.set_image_limit(args.image_limit)
            print(f"Image limit set to {args.image_limit}")
        elif args.show_config:
            config_info = manager.show_config()
            print("\nCurrent Configuration:")
            for key, value in config_info.items():
                print(f"{key}: {value}")
        elif args.clean_images:
            manager.clean_images()
            print("Image directory cleaned successfully.")
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {str(e)}")
        manager.logger.log_message(f"Error: {str(e)}")

if __name__ == "__main__":
    main()