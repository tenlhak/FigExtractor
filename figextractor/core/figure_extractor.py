"""
Module for extracting figures and their associated captions from PDF documents.
"""

import os
import cv2
import numpy as np
import logging
from PIL import Image
from selenium.webdriver.common.by import By
from ..utils.helpers import get_bounding_box, compute_overlap, find_caption_text

logger = logging.getLogger(__name__)

class FigureExtractor:
    def __init__(self, min_figure_size=100, caption_distance_threshold=50):
        """
        Initialize the figure extractor.
        
        Args:
            min_figure_size (int): Minimum size in pixels for a region to be considered a figure
            caption_distance_threshold (int): Maximum distance between figure and caption
        """
        self.min_figure_size = min_figure_size
        self.caption_distance_threshold = caption_distance_threshold

    def extract_figures_and_captions(self, pdf_path, html_dir, images, driver):
        """
        Extract figures and their associated captions from a PDF document.
        
        Args:
            pdf_path (str): Path to the PDF file
            html_dir (str): Directory containing HTML version of the PDF
            images (list): List of PIL Image objects for each page
            driver: Selenium WebDriver instance
            
        Returns:
            tuple: Lists of figures and captions for each page
        """
        figures = []
        captions = []
        
        for page_num, page_image in enumerate(images, 1):
            # Convert PIL image to OpenCV format
            cv_image = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)
            
            # Process HTML page
            html_path = os.path.join(html_dir, f'page{page_num}.html')
            if not os.path.exists(html_path):
                continue
                
            # Find figures in the page
            page_figures = self._detect_figures(cv_image)
            
            # Find captions in the HTML
            page_captions = self._detect_captions(driver, html_path)
            
            # Match figures with captions
            matched_figures, matched_captions = self._match_figures_and_captions(
                page_figures,
                page_captions,
                cv_image.shape
            )
            
            figures.append(matched_figures)
            captions.append(matched_captions)
            
        return figures, captions
        
    def _detect_figures(self, image):
        """
        Detect potential figure regions in an image using contour detection.
        
        Args:
            image: OpenCV image
            
        Returns:
            list: Detected figure regions with their bounding boxes
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Threshold the image
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        figures = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter small regions
            if w < self.min_figure_size or h < self.min_figure_size:
                continue
                
            # Extract the region
            region = image[y:y+h, x:x+w]
            
            figures.append({
                'bbox': (x, y, w, h),
                'image': Image.fromarray(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
            })
            
        return figures
        
    def _detect_captions(self, driver, html_path):
        """
        Detect figure captions in the HTML version of the page.
        
        Args:
            driver: Selenium WebDriver instance
            html_path (str): Path to the HTML file
            
        Returns:
            list: Detected captions with their bounding boxes and text
        """
        driver.get(f'file://{html_path}')
        
        captions = []
        # Find elements that might be captions (starting with "Figure" or "Fig.")
        elements = driver.find_elements(By.XPATH, "//div[starts-with(text(),'Figure') or starts-with(text(),'Fig.')]")
        
        for element in elements:
            bbox = get_bounding_box(element)
            text = element.text
            
            if text and bbox:
                captions.append({
                    'bbox': bbox,
                    'text': text
                })
                
        return captions
        
    def _match_figures_and_captions(self, figures, captions, image_shape):
        """
        Match detected figures with their corresponding captions based on proximity and layout.
        
        Args:
            figures (list): Detected figures
            captions (list): Detected captions
            image_shape (tuple): Shape of the page image
            
        Returns:
            tuple: Matched figures and captions
        """
        matched_figures = []
        matched_captions = []
        
        used_captions = set()
        
        for figure in figures:
            best_caption = None
            best_distance = float('inf')
            
            fig_bbox = figure['bbox']
            
            for i, caption in enumerate(captions):
                if i in used_captions:
                    continue
                    
                cap_bbox = caption['bbox']
                
                # Calculate distance between figure and caption
                distance = self._calculate_distance(fig_bbox, cap_bbox)
                
                if distance < self.caption_distance_threshold and distance < best_distance:
                    best_caption = caption
                    best_caption_idx = i
                    best_distance = distance
                    
            if best_caption:
                matched_figures.append(figure)
                matched_captions.append(best_caption)
                used_captions.add(best_caption_idx)
            else:
                # Figure without caption
                matched_figures.append(figure)
                matched_captions.append(None)
                
        return matched_figures, matched_captions
        
    def _calculate_distance(self, bbox1, bbox2):
        """Calculate the minimum distance between two bounding boxes."""
        x1, y1, w1, h1 = bbox1
        x2, y2, w2, h2 = bbox2
        
        # Calculate centers
        center1 = (x1 + w1/2, y1 + h1/2)
        center2 = (x2 + w2/2, y2 + h2/2)
        
        return np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)

# Create a default instance
extractor = FigureExtractor()
extract_figures_and_captions = extractor.extract_figures_and_captions
