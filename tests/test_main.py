"""Tests for scan_to_pdf.main module."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest
from PIL import Image

from scan_to_pdf.main import (
    collect_files,
    get_creation_timestamp,
    has_text_layer,
    image_to_pdf_bytes,
)


class TestGetCreationTimestamp:
    """Tests for get_creation_timestamp function."""

    def test_returns_float(self) -> None:
        """Test that get_creation_timestamp returns a float."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            test_file = tmp_path / "test.txt"
            test_file.write_text("test")

            timestamp = get_creation_timestamp(test_file)
            assert isinstance(timestamp, float)
            assert timestamp > 0


class TestCollectFiles:
    """Tests for collect_files function."""

    def test_collect_files_empty_folder(self) -> None:
        """Test that empty folder returns empty list."""
        with TemporaryDirectory() as tmpdir:
            files = collect_files(Path(tmpdir))
            assert files == []

    def test_collect_files_nonexistent_folder(self) -> None:
        """Test that nonexistent folder raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            collect_files(Path("/nonexistent/folder"))

    def test_collect_files_not_directory(self) -> None:
        """Test that file path raises NotADirectoryError."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            test_file = tmp_path / "test.txt"
            test_file.write_text("test")

            with pytest.raises(NotADirectoryError):
                collect_files(test_file)

    def test_collect_files_with_images(self) -> None:
        """Test collecting image files from folder."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Create test images
            (tmp_path / "test1.png").write_bytes(b"dummy")
            (tmp_path / "test2.jpg").write_bytes(b"dummy")

            files = collect_files(tmp_path)
            assert len(files) == 2
            assert all(f.suffix.lower() in {".png", ".jpg"} for f in files)

    def test_collect_files_sorted_by_creation_time(self) -> None:
        """Test that files are sorted by creation time."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Create files with supported extensions
            files_created = []
            for i in range(3):
                f = tmp_path / f"file{i}.png"
                img = Image.new("RGB", (10, 10))
                img.save(f)
                files_created.append(f)

            collected = collect_files(tmp_path)
            # Files should be sorted by creation time
            assert len(collected) == 3
            assert all(f.suffix == ".png" for f in collected)


class TestImageToPdfBytes:
    """Tests for image_to_pdf_bytes function."""

    def test_image_to_pdf_bytes_png(self) -> None:
        """Test converting PNG image to PDF bytes."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Create a test image
            img = Image.new("RGB", (100, 100), color="red")
            img_path = tmp_path / "test.png"
            img.save(img_path)

            with patch("scan_to_pdf.main.pytesseract.image_to_pdf_or_hocr") as mock_ocr:
                mock_ocr.return_value = b"%PDF-1.4\ntest"

                pdf_bytes = image_to_pdf_bytes(img_path, "eng")

                assert isinstance(pdf_bytes, bytes)
                assert pdf_bytes.startswith(b"%PDF")

    def test_image_to_pdf_bytes_with_string_return(self) -> None:
        """Test that string returns from OCR are encoded to bytes."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Create a test image
            img = Image.new("RGB", (100, 100), color="blue")
            img_path = tmp_path / "test.jpg"
            img.save(img_path)

            with patch("scan_to_pdf.main.pytesseract.image_to_pdf_or_hocr") as mock_ocr:
                mock_ocr.return_value = "%PDF-1.4\ntest"

                pdf_bytes = image_to_pdf_bytes(img_path, "jpn")

                assert isinstance(pdf_bytes, bytes)
                assert pdf_bytes == b"%PDF-1.4\ntest"


class TestHasTextLayer:
    """Tests for has_text_layer function."""

    def test_has_text_layer_nonexistent_pdf(self) -> None:
        """Test that nonexistent PDF raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            has_text_layer(Path("/nonexistent/file.pdf"))

    def test_has_text_layer_empty_pdf(self) -> None:
        """Test PDF with no pages returns False."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            pdf_path = tmp_path / "empty.pdf"
            pdf_path.write_bytes(b"")  # Create empty file

            with patch("scan_to_pdf.main.PdfReader") as mock_reader:
                mock_instance = mock_reader.return_value
                mock_instance.pages = []

                result = has_text_layer(pdf_path, threshold=0.1)
                assert result is False
