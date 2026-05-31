"""
Group B — Search Tool tests.

Covers matching keywords, no-match queries, stopword-only queries, and
empty input.
"""

import pytest
from tools.search_tool import SearchTool

DOC = (
    "Photosynthesis is how plants convert sunlight into chemical energy. "
    "The chlorophyll in plant cells absorbs light. "
    "Photosynthesis happens mainly in the leaves of plants."
)


@pytest.fixture
def search() -> SearchTool:
    return SearchTool()


def test_keyword_match(search):
    """B1: A keyword query returns sentences containing the keyword."""
    result = search.run({"question": "what about chlorophyll", "text": DOC})
    assert result["success"] is True
    assert len(result["results"]) >= 1
    assert any("chlorophyll" in r["sentence"].lower() for r in result["results"])


def test_no_match(search):
    """B2: A query with no document matches returns an empty list."""
    result = search.run({"question": "tell me about volcanoes", "text": DOC})
    assert result["success"] is True
    assert result["results"] == []


def test_stopwords_only(search):
    """B3: A question containing only stopwords is rejected."""
    result = search.run({"question": "what is the", "text": DOC})
    assert result["success"] is False
    assert "keyword" in result["error"].lower()


def test_empty_input(search):
    """B4: Missing question or text returns a clear error."""
    result = search.run({"question": "", "text": ""})
    assert result["success"] is False
    assert "missing" in result["error"].lower()


def test_results_are_ranked(search):
    """Results are sorted by score in descending order."""
    long_doc = (
        "Plants need sunlight. "
        "Plants need sunlight and water to grow. "
        "Animals eat plants."
    )
    result = search.run({"question": "plants and sunlight", "text": long_doc})
    scores = [r["score"] for r in result["results"]]
    assert scores == sorted(scores, reverse=True)
