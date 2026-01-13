# scan-to-pdf

Python 3.12 CLI that sorts images and PDFs by creation time, converts them to a
single searchable PDF, and runs OCR (Japanese + English by default) on images.

## Prerequisites
- Python 3.12
- [uv](https://github.com/astral-sh/uv)
- Tesseract OCR with language data (`jpn`, `eng`, etc.)
  - macOS: `brew install tesseract tesseract-lang`
  - Linux: `apt install tesseract-ocr tesseract-ocr-jpn tesseract-ocr-eng`
  - Windows: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Python Dependencies
- `pytesseract`: Python wrapper for Tesseract OCR
- `pypdf`: PDF manipulation library for reading/writing PDFs
- `pillow`: Image processing library
- `tqdm`: Progress bar library for displaying conversion progress

### Development Dependencies (optional)
- `ruff`: Linter and code formatter
- `mypy`: Static type checker
- `pytest`: Testing framework

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
  -

## Testing
Run the test suite:
```bash
uv run pytest -v
```

Run tests with coverage (install `pytest-cov` first):
```bash
uv add --group dev pytest-cov
uv run pytest --cov=src/scan_to_pdf -v
```-lang jpn+eng
```

### Options
- `folder`: Full path to a folder containing images and/or PDFs (required)
- `--output`: Output PDF path (optional; defaults to `<folder>/output.pdf`)
- `--lang`: Tesseract language codes for OCR on images (optional; defaults to `jpn+eng`)
  - Examples: `jpn`, `eng`, `jpn+eng`, `fra`, `deu`, etc.
  - Use `+` to combine multiple languages

### Supported File Formats
#### Images (OCR will be applied)
- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- TIFF (`.tif`, `.tiff`)
- BMP (`.bmp`)
- GIF (`.gif`)
- WebP (`.webp`)

#### PDF (automatic text layer detection)
- PDF (`.pdf`)
  - PDFs with text layer: Merged as-is (no OCR needed)
  - PDFs without text layer: Merged with warning (OCR would require pdf2image)

## Notes
- Files are sorted by creation time when available, otherwise modification time.
- Images are OCRed and embedded so the resulting PDF is searchable.
- PDFs are automatically checked for text layer:
  - With text layer (>10% pages): Merged directly, preserving searchability
  - Without text layer: Merged with a warning (OCR on PDF pages requires additional libraries)
- For math-heavy documents, ensure the Tesseract math model is installed if
  available on your system.
