from wallpaper_changer import WallpaperChanger
from utils import Logger

def main():
    logger = Logger()
    changer = WallpaperChanger()
    
    try:
        changer.change_wallpaper()
    except Exception as e:
        logger.log_message(f"Error changing wallpaper: {str(e)}")

if __name__ == "__main__":
    main()
