"""
Statistics Tool.

Computes basic document statistics: word count, sentence count, average
sentence length, and the five most common words.
"""

import re
import logging
from collections import Counter

logger = logging.getLogger(__name__)


class StatisticsTool:
    """Computes word, sentence and frequency statistics for the document."""

    name = "statistics"

    def run(self, input_data: dict) -> dict:
        """
        Compute statistics for the given text.

        Args:
            input_data: Dictionary with key 'text'.

        Returns:
            A dictionary with keys 'success', 'stats', 'error'.
        """
        if not isinstance(input_data, dict):
            return {"success": False, "stats": None, "error": "Input must be a dictionary."}

        text = input_data.get("text", "")
        if not isinstance(text, str) or not text.strip():
            return {"success": False, "stats": None, "error": "Empty document."}

        words = re.findall(r"[A-Za-z']+", text)
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

        word_count = len(words)
        sentence_count = len(sentences)
        average_sentence_length = (
            round(word_count / sentence_count, 2) if sentence_count else 0
        )
        most_common = Counter(w.lower() for w in words).most_common(5)

        stats = {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "average_sentence_length": average_sentence_length,
            "most_common_words": most_common,
        }

        logger.info("StatisticsTool computed stats: %s", stats)
        return {"success": True, "stats": stats, "error": None}
