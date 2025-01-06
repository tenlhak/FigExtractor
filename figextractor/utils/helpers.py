"""
Helper functions for the FigExtractor package.
"""

import os
import re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from config import Config

logger = logging.getLogger(__name__)

def setup_chrome_driver():
    """
    Initialize and configure Chrome WebDriver for PDF processing.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    chrome_options = Options()
    for option in Config.CHROME_OPTIONS:
        chrome_options.add_argument(option)
    
    service = Service(executable_path=Config.CHROME_DRIVER_PATH)
    
    try:
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
        raise

def get_page_dimensions(element):
    """
    Get the dimensions of a page from its HTML element.
    
    Args:
        element: Selenium WebElement representing the page
        
    Returns:
        tuple: (width, height) in pixels
    """
    try:
        width = element.get_attribute("width")
        height = element.get_attribute("height")
        return int(width), int(height)
    except (ValueError, AttributeError) as e:
        logger.error(f"Failed to get page dimensions: {str(e)}")
        return None, None

def create_output_directory(pdf_name):
    """
    Create output directory structure for a PDF file.
    
    Args:
        pdf_name (str): Name of the PDF file
        
    Returns:
        str: Path to the created output directory
    """
    output_dir = os.path.join(Config.OUTPUT_DIR, os.path.splitext(pdf_name)[0])
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def get_bounding_box(element):
    """
    Get the bounding box coordinates of an HTML element.
    
    Args:
        element: Selenium WebElement
        
    Returns:
        tuple: (x, y, width, height) or None if unavailable
    """
    try:
        location = element.location
        size = element.size
        return (
            location['x'],
            location['y'],
            size['width'],
            size['height']
        )
    except Exception:
        return None

def compute_overlap(box1, box2):
    """
    Compute the overlap ratio between two bounding boxes.
    
    Args:
        box1 (tuple): First box coordinates (x, y, width, height)
        box2 (tuple): Second box coordinates (x, y, width, height)
        
    Returns:
        float: Overlap ratio between 0 and 1
    """
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Calculate intersection
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)
    
    if x_right < x_left or y_bottom < y_top:
        return 0.0
        
    intersection = (x_right - x_left) * (y_bottom - y_top)
    
    # Calculate areas
    area1 = w1 * h1
    area2 = w2 * h2
    
    # Return overlap ratio
    return intersection / min(area1, area2)

def find_caption_text(element):
    """
    Extract and clean caption text from an HTML element.
    
    Args:
        element: Selenium WebElement containing caption text
        
    Returns:
        str: Cleaned caption text
    """
    try:
        text = element.text.strip()
        
        # Remove multiple whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Check if it's actually a caption
        if text.lower().startswith(('figure', 'fig.', 'fig')):
            return text
        
        return None
    except Exception:
        return None

def natural_sort(l):
    """
    Sort strings containing numbers in natural order.
    
    Args:
        l (list): List of strings to sort
        
    Returns:
        list: Sorted list
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def validate_pdf_path(pdf_path):
    """
    Validate that a PDF file exists and is accessible.
    
    Args:
        pdf_path (str): Path to PDF file
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return False
        
    if not os.access(pdf_path, os.R_OK):
        logger.error(f"PDF file not readable: {pdf_path}")
        return False
        
    return True

def sanitize_filename(filename):
    """
    Sanitize a filename by removing or replacing invalid characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Remove control characters
    filename = "".join(char for char in filename if ord(char) >= 32)
    
    return filename.strip()
