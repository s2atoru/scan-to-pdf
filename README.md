# scan-to-pdf

Python 3.12 CLI that sorts images by creation time, converts them to a
single searchable PDF, and runs OCR (Japanese + English by default).

## Prerequisites
- Python 3.12
- [uv](https://github.com/astral-sh/uv)
- Tesseract OCR with language data (`jpn`, `eng`, etc.)
  - macOS: `brew install tesseract tesseract-lang`
  - Linux: `apt install tesseract-ocr tesseract-ocr-jpn tesseract-ocr-eng`
  - Windows: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Python Dependencies
- `pytesseract`: Python wrapper for Tesseract OCR
- `pypdf`: PDF manipulation library
- `pillow`: Image processing library

## Setup
```bash
uv sync
```

## Installation
To install the `scan-to-pdf` command to `~/.local/bin/`:
```bash
uv tool install .
```

Or for development mode (editable install):
```bash
uv pip install -e .
```

**Note**: Ensure `~/.local/bin` is in your PATH. Add this to your shell profile if needed:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

After installation, you can run the command from anywhere:
```bash
scan-to-pdf /full/path/to/folder --output /full/path/to/output.pdf --lang jpn+eng
```

### Uninstall
```bash
uv tool uninstall scan-to-pdf
```

Or if installed with `uv pip install -e .`:
```bash
uv pip uninstall scan-to-pdf
```

## Usage (without installation)
For development or one-time use without installation:
```bash
uv run scan-to-pdf /full/path/to/folder --output /full/path/to/output.pdf \
  --lang jpn+eng
```

### Options
- `folder`: Full path to a folder containing images (required)
- `--output`: Output PDF path (optional; defaults to `<folder>/output.pdf`)
- `--lang`: Tesseract language codes (optional; defaults to `jpn+eng`)
  - Examples: `jpn`, `eng`, `jpn+eng`, `fra`, `deu`, etc.
  - Use `+` to combine multiple languages

### Supported Image Formats
- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- TIFF (`.tif`, `.tiff`)
- BMP (`.bmp`)
- GIF (`.gif`)
- WebP (`.webp`)

## Notes
- Images are sorted by creation time when available, otherwise modification
  time.
- Each page is OCRed and embedded so the PDF is searchable.
- For math-heavy documents, ensure the Tesseract math model is installed if
  available on your system.
