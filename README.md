# Suppap (Surprise Wallpaper)

## 🎉 Surprise Your Friends with Random Wallpapers!

Suppap (short for Surprise Wallpaper) is a fun, mischievous little application designed to add a dash of excitement to your (or your friends') computer experience. It periodically changes the desktop wallpaper to random images from popular subreddits, keeping things fresh and unpredictable!

### 🚀 Main Features

- Automatically downloads images from selected subreddits
- Changes wallpaper at set intervals
- Works on Windows, macOS, and Linux
- Easy to set up and run in the background
- Perfect for pranking friends or adding variety to your own desktop

## 🛠 Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/suppap.git
   cd suppap
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

To restore the default wallpaper and stop the application:
```
python src/main.py --back-to-normal
```


## ⚙ Configuration

You can customize the application by editing the `config.py` file:

- Change the wallpaper update interval
- Add or remove subreddits to fetch images from
- Modify the image folder location

## 🎭 Prank Ideas

1. Secretly install it on a friend's computer for a harmless prank
2. Set it up on public computers in your office or school (with permission, of course!)
3. Use it for a fun party game - guess the subreddit!

## 🤝 Contributing

We'd love your help to make Suppap even more awesome! Here are some ideas:

- Implement a better CLI for easier configuration
- Add support for more image sources beyond Reddit
- Create a feature to schedule different wallpaper themes for different times of day
- Improve error handling and logging
- Write unit tests to ensure reliability
- Add a feature to blend or transition between wallpapers

Feel free to fork the repo and submit pull requests with your improvements!

## ⚠️ Disclaimer

Please use Suppap responsibly. Always get permission before installing it on someone else's computer, and be mindful of potentially inappropriate content from Reddit.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Remember, with great power comes great responsibility... to prank your friends responsibly! Enjoy Suppap! 🎊🖼️