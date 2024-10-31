"""
Image Manager for the Wallpaper Changer application.

This module handles downloading images from Reddit and managing the local image collection.

Classes:
    ImageManager: Manages downloading and selecting images for wallpapers.
"""

import os
import random
import requests
from config import Config

class ImageManager:
    """
    A class to manage downloading and selecting images for wallpapers.
    """

    def __init__(self):
        """Initialize the ImageManager with configuration and track used images."""
        self.config = Config()
        self.used_images = set()

    def download_images(self, count=10):
        """
        Download multiple images from random subreddits specified in the configuration.

        Args:
            count (int): Number of images to download. Default is 10.

        Returns:
            list: List of file paths of the downloaded images.
        """
        downloaded_images = []
        for _ in range(count):
            image_path = self.download_image()
            if image_path:
                downloaded_images.append(image_path)
        return downloaded_images

    def download_image(self):
        """
        Download an image from a random subreddit specified in the configuration.

        Returns:
            str: The file path of the downloaded image, or None if download fails.
        """
        subreddit = random.choice(self.config.SUBREDDITS)
        url = f"https://www.reddit.com/r/{subreddit}/random.json"
        headers = {'User-agent': 'WallpaperChanger Bot 1.0'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Handle different response formats
            if isinstance(data, list):
                post_data = data[0]['data']['children'][0]['data']
            elif isinstance(data, dict):
                post_data = data['data']['children'][0]['data']
            else:
                raise ValueError("Unexpected Reddit API response format")

            image_url = post_data['url']
            score = post_data['score']
            # Check if the URL ends with an image extension
            if not image_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # If it's an imgur link without an extension, append .jpg
                if 'imgur.com' in image_url and not image_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_url += '.jpg'
                else:
                    # If it's not a direct image link or imgur, skip this post
                    raise ValueError("Not a direct image link")

            image_name = f"{subreddit}_{len(os.listdir(self.config.IMAGE_FOLDER)) + 1}.jpg"
            image_path = os.path.join(self.config.IMAGE_FOLDER, image_name)
            
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
            
            return {"url": image_path, "score": score}

        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Error downloading image from r/{subreddit}: {e}")
            return None

    def get_random_image(self):
        """
        Select a random image from the local collection, avoiding recent duplicates.

        Returns:
            str: The file path of the selected image, or None if no images are available.
        """
        available_images = set(os.listdir(self.config.IMAGE_FOLDER)) - self.used_images
        if not available_images:
            self.used_images.clear()
            available_images = set(os.listdir(self.config.IMAGE_FOLDER))
        
        if available_images:
            chosen_image = random.choice(list(available_images))
            self.used_images.add(chosen_image)
            return os.path.join(self.config.IMAGE_FOLDER, chosen_image)
        else:
            return None
