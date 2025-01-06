"""
PDF processing module for extracting figures and captions from PDF documents.
"""

import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..utils.helpers import get_page_dimensions, create_output_directory
from .renderer import render_pdf
from .figure_extractor import extract_figures_and_captions
from config import Config

logger = logging.getLogger(__name__)

def setup_chrome_driver():
    """Initialize Chrome WebDriver with appropriate options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    return webdriver.Chrome(
        executable_path=Config.CHROME_DRIVER_PATH,
        options=chrome_options
    )

def process_pdf(pdf_path):
    """
    Process a single PDF file to extract figures and captions.
    
    Args:
        pdf_path (str): Path to the PDF file to process
        
    Returns:
        dict: Extracted data containing figures and their metadata
    """
    try:
        pdf_name = os.path.basename(pdf_path)
        logger.info(f"Processing PDF: {pdf_name}")
        
        # Create output directories
        output_dir = create_output_directory(pdf_name)
        xpdf_dir = os.path.join(output_dir, 'xpdf')
        if not os.path.exists(xpdf_dir):
            os.makedirs(xpdf_dir)
            
        # Initialize data structure
        data = {pdf_name: {'figures': [], 'pages_annotated': []}}
        
        # Render PDF pages
        images = render_pdf(pdf_path, customize_dpi=Config.DPI)
        logger.info(f"Successfully rendered {len(images)} pages")
        
        # Convert PDF to HTML using XPDF
        pdf_html_path = os.path.join(xpdf_dir, os.path.splitext(pdf_name)[0])
        convert_to_html(pdf_path, pdf_html_path)
        
        # Setup Chrome driver
        driver = setup_chrome_driver()
        
        try:
            # Extract figures and captions
            figures, captions = extract_figures_and_captions(
                pdf_path=pdf_path,
                html_dir=xpdf_dir,
                images=images,
                driver=driver
            )
            
            # Process and save results
            for page_num, (page_figures, page_captions) in enumerate(zip(figures, captions), 1):
                for fig_num, (figure, caption) in enumerate(zip(page_figures, page_captions), 1):
                    figure_data = {
                        'page': page_num,
                        'figure_number': fig_num,
                        'region_bb': figure['bbox'],
                        'caption_text': caption['text'] if caption else '',
                        'caption_bb': caption['bbox'] if caption else None
                    }
                    
                    # Save figure image
                    figure_path = os.path.join(output_dir, f'page_{page_num}_figure_{fig_num}.jpg')
                    figure['image'].save(figure_path)
                    
                    # Save caption text
                    if caption:
                        caption_path = os.path.join(output_dir, f'page_{page_num}_caption_{fig_num}.txt')
                        with open(caption_path, 'w', encoding='utf-8') as f:
                            f.write(caption['text'])
                    
                    data[pdf_name]['figures'].append(figure_data)
                
                data[pdf_name]['pages_annotated'].append(page_num)
            
            # Save metadata
            metadata_path = os.path.join(output_dir, 'metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Successfully processed {pdf_name}")
            return data
            
        finally:
            driver.quit()
            
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {str(e)}")
        raise
        
def convert_to_html(pdf_path, output_path):
    """Convert PDF to HTML using XPDF tools."""
    try:
        command = [
            Config.XPDF_PATH,
            pdf_path,
            output_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting PDF to HTML: {str(e)}")
        raise
