import os

class Config:
    # Base paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Directory paths
    INPUT_DIR = os.path.join(BASE_DIR, "input")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    TEMP_DIR = os.path.join(BASE_DIR, "temp")
    
    # Tool paths
    XPDF_PATH = os.path.join(BASE_DIR, "tools", "xpdf-tools", "bin64", "pdftohtml.exe")
    IMAGEMAGICK_PATH = os.path.join(BASE_DIR, "tools", "imagemagick", "magick.exe")
    CHROME_DRIVER_PATH = os.path.join(BASE_DIR, "tools", "chromedriver", "chromedriver.exe")
    
    # Processing settings
    DPI = 150
    RASTER_SCALE = 3
    
    # Chrome options
    CHROME_OPTIONS = ["--headless"]

    @classmethod
    def initialize(cls):
        """Create necessary directories if they don't exist"""
        for directory in [cls.INPUT_DIR, cls.OUTPUT_DIR, cls.TEMP_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
