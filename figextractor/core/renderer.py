import os
import re
import tempfile
import subprocess
import shutil
from PIL import Image
from config import Config

def render_pdf(filename, customize_dpi=None):
    """
    Renders PDF pages as images using ImageMagick or Ghostscript.
    
    Args:
        filename (str): Path to the PDF file
        customize_dpi (int, optional): Custom DPI setting. Defaults to Config.DPI
        
    Returns:
        list: List of PIL Image objects, one per page
    """
    output_dpi = str(customize_dpi if customize_dpi else Config.DPI)
    output_dir = tempfile.mkdtemp()
    
    raster_density = str(Config.RASTER_SCALE * 100)

    try:
        if os.name == 'nt':
            command = [
                Config.IMAGEMAGICK_PATH,
                '-density', raster_density,
                filename,
                '-resample', output_dpi,
                '-set', 'colorspace', 'RGB',
                os.path.join(output_dir, 'image.png')
            ]
            print('Executing command:', ' '.join(command))
            subprocess.call(command)
        else:
            command = [
                'gs',
                '-q',
                '-sDEVICE=png16m',
                '-o', os.path.join(output_dir, 'file-%02d.png'),
                '-r' + output_dpi,
                filename
            ]
            subprocess.call(command)

        # Process images
        files = [f for f in os.listdir(output_dir) 
                if os.path.isfile(os.path.join(output_dir, f)) 
                and not f.startswith('.')]
        files = natural_sort(files)
        
        images = []
        for f in files:
            if f.endswith('.png'):
                page_im = Image.open(os.path.join(output_dir, f)).convert('RGB')
                page_im.load()
                images.append(page_im)
                
        return images
    
    finally:
        # Clean up temp directory
        shutil.rmtree(output_dir)

def natural_sort(l):
    """Sorts strings containing numbers in human order"""
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)
