from __future__ import annotations

import argparse
import io
from pathlib import Path
from typing import Iterable

import pytesseract
from PIL import Image, ImageOps
from pypdf import PdfReader, PdfWriter

SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".bmp",
    ".gif",
    ".webp",
}


def get_creation_timestamp(path: Path) -> float:
    """Return creation timestamp if available, otherwise modification time."""
    stats = path.stat()
    return getattr(stats, "st_birthtime", stats.st_mtime)


def collect_images(folder: Path) -> list[Path]:
    """Collect supported image files in creation-time order from the folder."""
    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder}")

    images = [
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(images, key=get_creation_timestamp)


def image_to_pdf_bytes(image_path: Path, language: str) -> bytes:
    """Convert a single image to searchable PDF bytes using Tesseract OCR."""
    with Image.open(image_path) as img:
        processed = ImageOps.exif_transpose(img).convert("RGB")
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(
            processed, extension="pdf", lang=language
        )
    return pdf_bytes


def assemble_pdf(
    image_paths: Iterable[Path], output_pdf: Path, language: str = "jpn+eng"
) -> None:
    """Combine images into one searchable PDF in the given order."""
    writer = PdfWriter()

    for path in image_paths:
        pdf_bytes = image_to_pdf_bytes(path, language)
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            writer.add_page(page)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as pdf_file:
        writer.write(pdf_file)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Create a searchable PDF by sorting images by creation time and "
            "running OCR."
        )
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="Full path to the folder containing images.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=("Output PDF path. Defaults to <folder>/output.pdf."),
    )
    parser.add_argument(
        "--lang",
        default="jpn+eng",
        help=(
            "Tesseract language codes, e.g., 'jpn', 'eng', or 'jpn+eng' for "
            "mixed documents."
        ),
    )
    return parser.parse_args()


def run_cli() -> None:
    """CLI entry point for converting images to a searchable PDF."""
    args = parse_args()
    images = collect_images(args.folder)
    if not images:
        raise SystemExit("No supported images found in the specified folder.")

    output_pdf = args.output or args.folder / "output.pdf"
    assemble_pdf(images, output_pdf, language=args.lang)
    print(f"Saved searchable PDF to {output_pdf}")


if __name__ == "__main__":
    run_cli()
