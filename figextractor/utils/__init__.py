"""
Utility functions for the FigExtractor package.
"""

from .helpers import (
    setup_chrome_driver,
    get_page_dimensions,
    create_output_directory,
    get_bounding_box,
    compute_overlap,
    find_caption_text
)

__all__ = [
    'setup_chrome_driver',
    'get_page_dimensions',
    'create_output_directory',
    'get_bounding_box',
    'compute_overlap',
    'find_caption_text'
]
