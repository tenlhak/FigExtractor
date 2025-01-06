# Required Tools

This directory should contain the following third-party tools:

## Directory Structure
```
tools/
├── imagemagick/          # ImageMagick executable and dependencies
├── xpdf-tools/           # XPDF Tools (pdftohtml, etc.)
├── chromedriver/         # ChromeDriver executable
└── README.md            # This file
```

## Required Downloads

1. **ImageMagick**
   - Download from: https://imagemagick.org/script/download.php
   - Version: 7.1.1 or later
   - Place in: `tools/imagemagick/`

2. **XPDF Tools**
   - Download from: https://www.xpdfreader.com/download.html
   - Version: 4.05 or later
   - Place in: `tools/xpdf-tools/`

3. **ChromeDriver**
   - Download from: https://chromedriver.chromium.org/downloads
   - Version: Match with your Chrome browser version
   - Place in: `tools/chromedriver/`

## Installation Notes

1. Download each tool from the official website
2. Extract/install them in their respective directories
3. Ensure the executables have proper permissions
4. Update the paths in `config.py` if necessary

Note: Don't commit the actual tool binaries to Git. This directory is mainly for local development.
