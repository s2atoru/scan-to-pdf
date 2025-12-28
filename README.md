# scan-to-pdf

Python 3.12 CLI that sorts images by creation time, converts them to a
single searchable PDF, and runs OCR (Japanese + English by default).

## Prerequisites
- Python 3.12
- [uv](https://github.com/astral-sh/uv)
- Tesseract OCR with language data (`jpn`, `eng`, etc.)
  - macOS: `brew install tesseract tesseract-lang`

## Setup
```bash
uv sync
```

## Usage
```bash
uv run scan-to-pdf /full/path/to/folder --output /full/path/to/output.pdf \
  --lang jpn+eng
```
- `folder`: full path to a folder containing images (png, jpg, jpeg, tif,
  tiff, bmp, gif, webp)
- `--output`: optional; defaults to `<folder>/output.pdf`
- `--lang`: Tesseract language codes, e.g., `jpn`, `eng`, or `jpn+eng`

## Notes
- Images are sorted by creation time when available, otherwise modification
  time.
- Each page is OCRed and embedded so the PDF is searchable.
- For math-heavy documents, ensure the Tesseract math model is installed if
  available on your system.
