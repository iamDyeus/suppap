import unittest
from unittest.mock import patch, MagicMock
from main import get_images
from config import MIN_SCORE

class TestImageRetrieval(unittest.TestCase):
    @patch("main.reddit")
    def test_get_images_above_min_score(self, mock_reddit):
        # Set up mock subreddit posts with different scores
        mock_subreddit = MagicMock()
        mock_subreddit.hot.return_value = [
            MagicMock(score=MIN_SCORE + 1, url="http://image1.jpg"),
            MagicMock(score=MIN_SCORE + 10, url="http://image2.png"),
            MagicMock(score=MIN_SCORE - 1, url="http://image3.jpg"),  # Should be excluded
        ]
        mock_reddit.subreddit.return_value = mock_subreddit
        images = get_images("some_subreddit")
        # Assert that only images above MIN_SCORE are included
        self.assertEqual(len(images), 2)
        self.assertNotIn("http://image3.jpg", images)

    @patch("main.reddit")
    def test_get_images_only_images(self, mock_reddit):
        # Set up mock posts with different file types
        mock_subreddit = MagicMock()
        mock_subreddit.hot.return_value = [
            MagicMock(score=MIN_SCORE + 5, url="http://image.jpg"),
            MagicMock(score=MIN_SCORE + 5, url="http://not_image.gif"),
        ]
        mock_reddit.subreddit.return_value = mock_subreddit
        images = get_images("some_subreddit")
        # Assert only image URLs are returned
        self.assertEqual(len(images), 1)
        self.assertIn("http://image.jpg", images)
        
    def test_invalid_min_score(self):
        # Test if MIN_SCORE is set to None or an invalid type
        with self.assertRaises(TypeError):
            MIN_SCORE = "invalid_value"
            get_images("some_subreddit")

    @patch("main.reddit")
    def test_get_images_empty_subreddit(self, mock_reddit):
        # Set up mock subreddit with no posts
        mock_subreddit = MagicMock()
        mock_subreddit.hot.return_value = []
        mock_reddit.subreddit.return_value = mock_subreddit
        images = get_images("some_subreddit")
        # Assert that no images are returned
        self.assertEqual(len(images), 0)

    @patch("main.reddit")
    def test_get_images_invalid_url(self, mock_reddit):
        # Set up mock posts with invalid URLs
        mock_subreddit = MagicMock()
        mock_subreddit.hot.return_value = [
            MagicMock(score=MIN_SCORE + 5, url="http://invalid_url.txt"),
        ]
        mock_reddit.subreddit.return_value = mock_subreddit
        images = get_images("some_subreddit")
        # Assert no invalid URLs are returned
        self.assertEqual(len(images), 0)

if __name__ == "__main__":
    unittest.main()
