# tests/test_main.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from unittest.mock import patch, MagicMock
from src.main import WallpaperManager


class TestWallpaperManager(unittest.TestCase):

    def setUp(self):
        with patch('src.main.Config') as MockConfig, \
             patch('src.main.Logger') as MockLogger, \
             patch('src.main.OSCompatibilityChecker') as MockOSChecker, \
             patch('src.main.TaskScheduler') as MockScheduler, \
             patch('src.main.WallpaperChanger') as MockChanger:
            
            self.mock_config = MockConfig.return_value
            self.mock_logger = MockLogger.return_value
            self.mock_os_checker = MockOSChecker.return_value
            self.mock_scheduler = MockScheduler.return_value
            self.mock_wallpaper_changer = MockChanger.return_value

            self.manager = WallpaperManager()
            self.manager.config = self.mock_config
            self.manager.logger = self.mock_logger
            self.manager.scheduler = self.mock_scheduler
            self.manager.wallpaper_changer = self.mock_wallpaper_changer

    def test_start_service(self):
        """Test the start function, which sets up and starts the service."""
        self.manager.start()
        self.mock_scheduler.schedule_task.assert_called_once_with(
            self.mock_config.TASK_NAME, self.mock_config.WALLPAPER_CHANGE_INTERVAL
        )
        self.mock_wallpaper_changer.change_wallpaper.assert_called_once()
        self.mock_logger.log_message.assert_any_call("Setting up wallpaper manager")

    def test_stop_service(self):
        """Test the stop function, which stops the service and restores the default wallpaper."""
        self.manager.stop()
        self.mock_scheduler.remove_task.assert_called_once_with(self.mock_config.TASK_NAME)
        self.mock_wallpaper_changer.restore_default_wallpaper.assert_called_once()
        self.mock_logger.log_message.assert_any_call(
            "Application removed from startup and default wallpaper restored."
        )

    def test_change_now(self):
        """Test changing wallpaper immediately."""
        self.manager.change_now()
        self.mock_wallpaper_changer.change_wallpaper.assert_called_once()
        self.mock_logger.log_message.assert_called_once_with("Wallpaper changed manually")

    def test_update_interval(self):
        """Test updating the interval for changing wallpapers."""
        new_interval = 300
        self.manager.update_interval(new_interval)
        self.mock_scheduler.update_task.assert_called_once_with(self.mock_config.TASK_NAME, new_interval)
        self.assertEqual(self.manager.config.WALLPAPER_CHANGE_INTERVAL, new_interval)
        self.mock_logger.log_message.assert_called_once_with(
            f"Updated wallpaper change interval to {new_interval} seconds"
        )

    def test_add_subreddits(self):
        """Test adding new subreddits to the list."""
        initial_subreddits = ["wallpapers"]
        self.manager.config.SUBREDDITS = initial_subreddits
        new_subreddits = ["earthporn", "spaceporn"]
        self.manager.add_subreddits(new_subreddits)
        self.assertIn("earthporn", self.manager.config.SUBREDDITS)
        self.assertIn("spaceporn", self.manager.config.SUBREDDITS)
        self.mock_logger.log_message.assert_called_once_with("Added subreddits: earthporn, spaceporn")

    def test_remove_subreddits(self):
        """Test removing subreddits from the list."""
        self.manager.config.SUBREDDITS = ["wallpapers", "earthporn", "spaceporn"]
        self.manager.remove_subreddits(["earthporn"])
        self.assertNotIn("earthporn", self.manager.config.SUBREDDITS)
        self.mock_logger.log_message.assert_called_once_with("Removed subreddits: earthporn")

    def test_set_image_limit(self):
        """Test setting the maximum number of images to store."""
        new_limit = 50
        self.manager.set_image_limit(new_limit)
        self.assertEqual(self.manager.config.IMAGE_LIMIT, new_limit)
        self.mock_logger.log_message.assert_called_once_with(f"Set image limit to {new_limit}")

    def test_set_min_resolution(self):
        """Test setting the minimum resolution for downloaded images."""
        new_resolution = (2560, 1440)
        self.manager.set_min_resolution(new_resolution)
        self.assertEqual(self.manager.config.MIN_RESOLUTION, new_resolution)
        self.mock_logger.log_message.assert_called_once_with(f"Set minimum resolution to {new_resolution}")

    def test_show_config(self):
        """Test showing the current configuration."""
        self.mock_config.WALLPAPER_CHANGE_INTERVAL = 600
        self.mock_config.SUBREDDITS = ["wallpapers"]
        self.mock_config.IMAGE_LIMIT = 100
        self.mock_config.MIN_RESOLUTION = (1920, 1080)
        config_info = self.manager.show_config()
        expected_config = {
            "Change Interval": "600 seconds",
            "Subreddits": ["wallpapers"],
            "Image Limit": 100,
            "Min Resolution": (1920, 1080),
            "Image Folder": self.mock_config.IMAGE_FOLDER,
        }
        self.assertEqual(config_info, expected_config)


if __name__ == "__main__":
    unittest.main()
