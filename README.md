# FigExtractor

FigExtractor is a powerful Python tool designed to automatically extract figures and their associated captions from PDF documents. It's particularly useful for researchers, academics, and anyone working with scientific papers who needs to extract and analyze figures programmatically.

## Features

- Extracts figures and diagrams from PDF documents
- Identifies and associates captions with their corresponding figures
- Supports multi-column layouts
- Handles complex document structures
- Exports figures as high-quality images
- Generates JSON metadata for extracted figures
- Cross-platform support (Windows, Linux, macOS)

## Prerequisites

- Python 3.7+
- Chrome/Chromium browser (for web content rendering)
- Required third-party tools:
  - ImageMagick
  - XPDF Tools
  - ChromeDriver

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FigExtractor.git
cd FigExtractor
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Download and install required third-party tools:
   - [ImageMagick](https://imagemagick.org/script/download.php)
   - [XPDF Tools](https://www.xpdfreader.com/download.html)
   - [ChromeDriver](https://chromedriver.chromium.org/downloads)

4. Place the downloaded tools in the `tools/` directory:
```
tools/
├── imagemagick/
├── xpdf-tools/
└── chromedriver/
```

5. Update `config.py` with your local paths if necessary.

## Usage

1. Place your PDF files in the `input/` directory.

2. Run the extractor:
```bash
python main.py
```

3. Find extracted figures and data in the `output/` directory:
   - Figures are saved as JPG files
   - Captions are saved as TXT files
   - Metadata is saved as JSON files

## Output Format

For each processed PDF, FigExtractor creates:
- A directory containing extracted figures as JPG files
- Text files containing the associated captions
- A JSON file with metadata including:
  - Figure locations
  - Caption text
  - Page numbers
  - Bounding box coordinates

Example JSON output:
```json
{
    "example.pdf": {
        "figures": [
            {
                "page": 1,
                "region_bb": [100, 200, 400, 300],
                "figure_type": "Figure",
                "caption_bb": [100, 500, 400, 520],
                "caption_text": "Figure 1: Example diagram..."
            }
        ]
    }
}
```

## Project Structure

```
FigExtractor/
├── config.py           # Configuration settings
├── figextractor/      # Main package
│   ├── core/          # Core functionality
│   └── utils/         # Utility functions
├── input/             # Input PDFs
├── output/            # Extracted figures
├── tools/             # Third-party tools
├── requirements.txt
└── main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses modified components from various open-source projects
- Thanks to all contributors and maintainers of the required tools
