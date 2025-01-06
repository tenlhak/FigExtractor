"""
Core module for FigExtractor.
Contains the main functionality for PDF processing and figure extraction.
"""

from .pdf_processor import process_pdf
from .figure_extractor import extract_figures_and_captions

__all__ = ['process_pdf', 'extract_figures_and_captions']
