"""
Group D — Statistics Tool tests.

Covers word and sentence counts, average sentence length, and the most
common words.
"""

import pytest
from tools.statistics_tool import StatisticsTool

DOC = "Plants need light. Plants need water. Animals eat plants."


@pytest.fixture
def stats() -> StatisticsTool:
    return StatisticsTool()


def test_counts(stats):
    """D1: Counted values match the hand-verified expected values."""
    result = stats.run({"text": DOC})
    assert result["success"] is True
    s = result["stats"]
    assert s["word_count"] == 9  # plants, need, light, plants, need, water, animals, eat, plants
    assert s["sentence_count"] == 3


def test_average_sentence_length(stats):
    """D2: Average sentence length is word_count / sentence_count."""
    result = stats.run({"text": DOC})
    s = result["stats"]
    assert s["average_sentence_length"] == round(9 / 3, 2)


def test_most_common_words(stats):
    """D3: Most common words are returned in descending count order."""
    result = stats.run({"text": DOC})
    most_common = result["stats"]["most_common_words"]
    assert isinstance(most_common, list)
    assert len(most_common) <= 5
    # "plants" appears 3 times and should be the top word.
    assert most_common[0][0] == "plants"
    counts = [c for _, c in most_common]
    assert counts == sorted(counts, reverse=True)


def test_empty_document(stats):
    """An empty document produces an error rather than crashing."""
    result = stats.run({"text": ""})
    assert result["success"] is False
    assert "empty" in result["error"].lower()
