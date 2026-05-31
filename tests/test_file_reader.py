"""
Group A — File Reader Tool tests.

Covers loading valid .txt files, missing files, unsupported file
extensions, and empty files.
"""

import os
import pytest
from tools.file_reader import FileReaderTool

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
SAMPLE_TXT = os.path.join(FIXTURE_DIR, "sample.txt")
EMPTY_TXT = os.path.join(FIXTURE_DIR, "empty.txt")


@pytest.fixture
def reader() -> FileReaderTool:
    return FileReaderTool()


def test_load_valid_txt(reader):
    """A1: Loading a valid .txt file returns its text and metadata."""
    result = reader.run(SAMPLE_TXT)
    assert result["success"] is True
    assert "photosynthesis" in result["text"].lower()
    assert result["metadata"]["character_count"] == len(result["text"])
    assert result["metadata"]["extension"] == ".txt"
    assert result["error"] is None


def test_missing_file(reader):
    """A3: A path that does not exist returns a clear error."""
    result = reader.run("does_not_exist.txt")
    assert result["success"] is False
    assert result["text"] is None
    assert "not found" in result["error"].lower()


def test_unsupported_extension(reader, tmp_path):
    """A4: A path with an unsupported extension is rejected."""
    bad_file = tmp_path / "data.docx"
    bad_file.write_text("dummy", encoding="utf-8")
    result = reader.run(str(bad_file))
    assert result["success"] is False
    assert "unsupported" in result["error"].lower()


def test_empty_file(reader):
    """A5: An empty file is reported instead of returning empty text."""
    result = reader.run(EMPTY_TXT)
    assert result["success"] is False
    assert "empty" in result["error"].lower()


def test_invalid_path_type(reader):
    """Non-string paths are rejected without raising."""
    result = reader.run(None)
    assert result["success"] is False
    assert "string" in result["error"].lower() or "path" in result["error"].lower()
