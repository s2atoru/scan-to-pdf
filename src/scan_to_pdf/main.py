from __future__ import annotations

import argparse
import io
from collections.abc import Iterable
from pathlib import Path

import pytesseract
from PIL import Image, ImageOps
from pypdf import PdfReader, PdfWriter
from tqdm import tqdm

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".bmp",
    ".gif",
    ".webp",
}

PDF_EXTENSION = ".pdf"

SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | {PDF_EXTENSION}


def get_creation_timestamp(path: Path) -> float:
    """Return creation timestamp if available, otherwise modification time.

    Args:
        path: Path to the file.

    Returns:
        Creation timestamp (or modification time if creation time unavailable).
    """
    stats = path.stat()
    return getattr(stats, "st_birthtime", stats.st_mtime)


def collect_files(folder: Path) -> list[Path]:
    """Collect supported files in creation-time order from the folder.

    Supports both images and PDFs.

    Args:
        folder: Path to the folder containing files.

    Returns:
        List of file paths sorted by creation time.

    Raises:
        FileNotFoundError: If the folder does not exist.
        NotADirectoryError: If the path is not a directory.
    """
    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder}")

    files = [
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(files, key=get_creation_timestamp)


def has_text_layer(pdf_path: Path, threshold: float = 0.1) -> bool:
    """Check if a PDF has a text layer (is OCR'd or text-based).

    This function extracts text from each page and determines if at least
    a certain percentage of pages contain extractable text.

    Args:
        pdf_path: Path to the PDF file.
        threshold: Minimum ratio of pages with text to consider PDF as having
            a text layer. Default 0.1 means at least 10% of pages should have
            text.

    Returns:
        True if the PDF appears to have a text layer, False otherwise.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    if total_pages == 0:
        return False

    pages_with_text = 0
    for page in reader.pages:
        text = page.extract_text().strip()
        if text:  # Page has extractable text
            pages_with_text += 1

    # Return True if at least threshold% of pages have text
    return (pages_with_text / total_pages) >= threshold


def image_to_pdf_bytes(image_path: Path, language: str) -> bytes:
    """Convert a single image to searchable PDF bytes using Tesseract OCR.

    Args:
        image_path: Path to the image file.
        language: Tesseract language codes (e.g., 'jpn+eng').

    Returns:
        PDF data as bytes.
    """
    with Image.open(image_path) as img:
        processed = ImageOps.exif_transpose(img).convert("RGB")
        pdf_data = pytesseract.image_to_pdf_or_hocr(
            processed, extension="pdf", lang=language
        )
    if isinstance(pdf_data, str):
        return pdf_data.encode("utf-8")
    return pdf_data


def assemble_pdf(
    file_paths: Iterable[Path], output_pdf: Path, language: str = "jpn+eng"
) -> None:
    """Combine images and PDFs into one searchable PDF in the given order.

    For images, OCR is applied to create a searchable PDF.
    For PDFs without a text layer, a warning is printed and they are added
    as-is (OCR on PDF pages would require pdf2image library).

    Args:
        file_paths: Paths to image files and/or PDF files.
        output_pdf: Output PDF file path.
        language: Tesseract language codes for OCR on images (e.g., 'jpn+eng').
    """
    writer = PdfWriter()
    file_list = list(file_paths)

    with tqdm(total=len(file_list), desc="Converting to PDF", unit="file") as pbar:
        for path in file_list:
            if path.suffix.lower() == PDF_EXTENSION:
                # Check if PDF needs OCR
                if has_text_layer(path):
                    # Add existing PDF pages directly (already has text layer)
                    reader = PdfReader(path)
                    for page in reader.pages:
                        writer.add_page(page)
                else:
                    # PDF has no text layer - add with warning
                    print(
                        f"Warning: {path.name} has no text layer. Adding as-is "
                        "without OCR."
                    )
                    reader = PdfReader(path)
                    for page in reader.pages:
                        writer.add_page(page)
            elif path.suffix.lower() in IMAGE_EXTENSIONS:
                # Convert image to searchable PDF
                pdf_bytes = image_to_pdf_bytes(path, language)
                reader = PdfReader(io.BytesIO(pdf_bytes))
                for page in reader.pages:
                    writer.add_page(page)
            pbar.update(1)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as pdf_file:
        writer.write(pdf_file)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Create a searchable PDF by sorting images and PDFs by creation time and "
            "running OCR on images."
        )
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="Full path to the folder containing images and/or PDFs.",
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
    """CLI entry point for converting images and PDFs to a searchable PDF."""
    args = parse_args()
    files = collect_files(args.folder)
    if not files:
        raise SystemExit("No supported files found in the specified folder.")

    output_pdf = args.output or args.folder / "output.pdf"
    assemble_pdf(files, output_pdf, language=args.lang)
    print(f"Saved searchable PDF to {output_pdf}")


if __name__ == "__main__":
    run_cli()
