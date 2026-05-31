"""
Group C — Summary Tool tests.

Covers extractive summaries on multi-sentence documents, custom length,
and empty input.
"""

import pytest
from tools.summary_tool import SummaryTool

DOC = (
    "Photosynthesis is the process by which plants convert sunlight into energy. "
    "Chlorophyll absorbs light and helps drive the chemical reaction. "
    "Water and carbon dioxide are converted into glucose and oxygen. "
    "Photosynthesis is essential for life on Earth. "
    "Most photosynthesis happens in plant leaves."
)


@pytest.fixture
def summarizer() -> SummaryTool:
    return SummaryTool()


def test_basic_summary(summarizer):
    """C1: A multi-sentence document produces a non-empty summary."""
    result = summarizer.run({"text": DOC})
    assert result["success"] is True
    assert isinstance(result["summary"], str)
    assert len(result["summary"]) > 0


def test_custom_length(summarizer):
    """C2: A custom length parameter limits the number of sentences picked."""
    result = summarizer.run({"text": DOC, "length": 2})
    assert result["success"] is True
    # The summary should have at most the requested number of sentence endings.
    endings = sum(result["summary"].count(p) for p in ".!?")
    assert endings <= 2


def test_empty_document(summarizer):
    """C3: An empty document is reported as such."""
    result = summarizer.run({"text": "   "})
    assert result["success"] is False
    assert "empty" in result["error"].lower()
