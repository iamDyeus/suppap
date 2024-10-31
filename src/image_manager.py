 import os
import random
import requests
import logging
from config import Config

class ImageManager:
    """
    A class to manage downloading and selecting images for wallpapers.
    """

    def __init__(self):
        """Initialize the ImageManager with configuration and track used images."""
        self.config = Config()
        self.used_images = set()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
                logging.info(f"Downloaded image: {image_path}")
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
            post_data = self.extract_post_data(data)
            image_url = post_data['url']

            # Check if the URL ends with an image extension
            if not image_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # If it's an imgur link without an extension, append .jpg
                if 'imgur.com' in image_url:
                    image_url += '.jpg'
                else:
                    raise ValueError("Not a direct image link")

            image_name = f"{subreddit}_{len(os.listdir(self.config.IMAGE_FOLDER)) + 1}.jpg"
            image_path = os.path.join(self.config.IMAGE_FOLDER, image_name)

            image_response = requests.get(image_url)
            image_response.raise_for_status()

            with open(image_path, 'wb') as f:
                f.write(image_response.content)
            return image_path
        
        except (requests.RequestException, ValueError, KeyError) as e:
            logging.error(f"Error downloading image from r/{subreddit}: {e}")
            return None

    def extract_post_data(self, data):
        """Extract post data from the Reddit API response."""
        if isinstance(data, list):
            return data[0]['data']['children'][0]['data']
        elif isinstance(data, dict):
            return data['data']['children'][0]['data']
        else:
            raise ValueError("Unexpected Reddit API response format")

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
            logging.info(f"Selected image: {chosen_image}")
            return os.path.join(self.config.IMAGE_FOLDER, chosen_image)
        else:
            logging.warning("No images available")
            return None

# UI/UX enhancement: Displaying the image in a simple GUI
from tkinter import Tk, Label, Button, PhotoImage

class ImageViewer:
    """
    A simple GUI to display the selected image using Tkinter.
    """

    def __init__(self, image_manager):
        self.image_manager = image_manager
        self.window = Tk()
        self.window.title("Wallpaper Changer")
        self.label = Label(self.window)
        self.label.pack()
        self.button = Button(self.window, text="Change Wallpaper", command=self.update_image)
        self.button.pack()
        self.update_image()

    def update_image(self):
        image_path = self.image_manager.get_random_image()
        if image_path:
            img = PhotoImage(file=image_path)
            self.label.config(image=img)
            self.label.image = img
        else:
            self.label.config(text="No images available")

    def run(self):
        self.window.mainloop()

# Example usage
if __name__ == "__main__":
    manager = ImageManager()
    manager.download_images(5)
    viewer = ImageViewer(manager)
    viewer.run()


  
