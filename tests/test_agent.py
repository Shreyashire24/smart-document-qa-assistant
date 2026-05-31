"""
Group E — Agent (integration) tests.

Covers intent detection, end-to-end question answering, fallback for
unknown intents, and the guard for asking before loading a document.
"""

import os
import pytest
from agent import Agent

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
SAMPLE_TXT = os.path.join(FIXTURE_DIR, "sample.txt")


@pytest.fixture
def loaded_agent() -> Agent:
    agent = Agent()
    result = agent.load_document(SAMPLE_TXT)
    assert result["success"] is True
    return agent


def test_intent_summary(loaded_agent):
    """E1: A question with a summary keyword is classified as summary."""
    assert loaded_agent.detect_intent("Can you summarize this document?") == "summary"
    answer = loaded_agent.ask("summarize this")
    assert answer.startswith("Summary:")


def test_intent_statistics(loaded_agent):
    """E2: A question with a statistics phrase is classified as statistics."""
    assert loaded_agent.detect_intent("How many words are in this?") == "statistics"
    answer = loaded_agent.ask("how many words")
    assert "Words:" in answer
    assert "Sentences:" in answer


def test_intent_search(loaded_agent):
    """E3: A generic question is classified as search."""
    assert loaded_agent.detect_intent("What about chlorophyll?") == "search"
    answer = loaded_agent.ask("what about chlorophyll")
    assert answer.startswith("Top matches:") or answer.startswith(
        "No matching content"
    )


def test_intent_unknown(loaded_agent):
    """E4: An empty question is treated as unknown."""
    assert loaded_agent.detect_intent("") == "unknown"
    assert loaded_agent.detect_intent("   ") == "unknown"


def test_ask_before_loading():
    """E5: Asking before any document is loaded returns a guarded message."""
    agent = Agent()
    answer = agent.ask("summarize this")
    assert "No document is loaded" in answer
