import os
import sys
import logging
from figextractor.core.pdf_processor import process_pdf
from config import Config

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(Config.OUTPUT_DIR, 'extraction.log')),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point for the application"""
    # Initialize configuration and create necessary directories
    Config.initialize()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting FigExtractor")
    
    # Process each PDF in the input directory
    input_files = [f for f in os.listdir(Config.INPUT_DIR) 
                  if f.endswith('.pdf') and not f.startswith('._')]
    
    if not input_files:
        logger.warning("No PDF files found in input directory")
        return
    
    logger.info(f"Found {len(input_files)} PDF files to process")
    
    for pdf_file in input_files:
        try:
            pdf_path = os.path.join(Config.INPUT_DIR, pdf_file)
            logger.info(f"Processing {pdf_file}")
            
            process_pdf(pdf_path)
            
            logger.info(f"Successfully processed {pdf_file}")
            
        except Exception as e:
            logger.error(f"Error processing {pdf_file}: {str(e)}")
            continue

if __name__ == "__main__":
    main()
