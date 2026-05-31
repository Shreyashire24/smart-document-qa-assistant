"""
File Reader Tool.

Loads and extracts text content from .pdf and .txt files. Returns a
uniform result dictionary with success / text / metadata / error keys.
"""

import os
import logging
from config import SUPPORTED_EXTENSIONS

logger = logging.getLogger(__name__)


class FileReaderTool:
    """Reads supported document files and returns their text content."""

    name = "file_reader"

    def run(self, file_path: str) -> dict:
        """
        Load a file and return its text content.

        Args:
            file_path: Absolute or relative path to a .pdf or .txt file.

        Returns:
            A dictionary with keys: 'success', 'text', 'metadata', 'error'.
        """
        logger.info("FileReaderTool received path: %s", file_path)

        if not isinstance(file_path, str) or not file_path:
            return self._error("File path must be a non-empty string.")

        if not os.path.exists(file_path):
            return self._error(f"File not found: {file_path}")

        extension = os.path.splitext(file_path)[1].lower()
        if extension not in SUPPORTED_EXTENSIONS:
            return self._error(f"Unsupported file format: {extension}")

        try:
            if extension == ".txt":
                text = self._read_txt(file_path)
            else:
                text = self._read_pdf(file_path)
        except Exception as exc:  # noqa: BLE001
            return self._error(f"Failed to read file: {exc}")

        if not text.strip():
            return self._error("The document is empty.")

        return {
            "success": True,
            "text": text,
            "metadata": {
                "file_path": file_path,
                "extension": extension,
                "character_count": len(text),
            },
            "error": None,
        }

    # ----- private helpers -----

    def _read_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as fh:
            return fh.read()

    def _read_pdf(self, file_path: str) -> str:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ImportError(
                "pypdf is required to read PDF files. "
                "Install it with: pip install pypdf"
            ) from exc

        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _error(self, message: str) -> dict:
        logger.error(message)
        return {
            "success": False,
            "text": None,
            "metadata": None,
            "error": message,
        }
