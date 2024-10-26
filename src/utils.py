"""
Utility functions and classes for the Wallpaper Changer application.

This module provides utility classes for logging and OS compatibility checking.

Classes:
    Logger: Handles logging for the application.
    OSCompatibilityChecker: Checks if the current OS is compatible with the application.
"""

import platform
import logging

class Logger:
    """
    A class to handle logging for the Wallpaper Changer application.
    """

    def __init__(self):
        """Initialize the logger with basic configuration."""
        logging.basicConfig(filename='wallpaper_changer.log', level=logging.INFO,
                            format='%(asctime)s - %(message)s')

    def log_message(self, msg):
        """
        Log a message at the INFO level.

        Args:
            msg (str): The message to be logged.
        """
        logging.info(msg)

class OSCompatibilityChecker:
    """
    A class to check if the current operating system is compatible with the application.
    """

    @staticmethod
    def check_os_compatibility():
        """
        Check if the current OS is supported by the application.

        Returns:
            str: The name of the current operating system.

        Raises:
            OSError: If the current OS is not supported.
        """
        supported_os = ['Windows', 'Darwin', 'Linux']
        current_os = platform.system()
        if current_os not in supported_os:
            raise OSError(f"Unsupported operating system: {current_os}")
        return current_os
