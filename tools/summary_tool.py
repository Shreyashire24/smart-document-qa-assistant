"""
Summary Tool.

Generates a short extractive summary of a document. Sentences are scored
by the sum of their non-stopword word frequencies. Sentences near the
start receive a small bonus. The top-scoring sentences are then returned
in original document order.
"""

import re
import logging
from collections import Counter
from config import DEFAULT_SUMMARY_LENGTH

logger = logging.getLogger(__name__)


class SummaryTool:
    """Produces an extractive summary based on word frequency."""

    name = "summary"

    STOPWORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "of", "in", "on", "at", "to", "for", "and", "or", "but",
        "it", "its", "as", "by", "with", "about", "from", "this",
        "that", "these", "those", "has", "have", "had",
    }

    def run(self, input_data: dict) -> dict:
        """
        Generate an extractive summary of the document text.

        Args:
            input_data: Dictionary with key 'text' and optional 'length'.

        Returns:
            A dictionary with keys 'success', 'summary', 'error'.
        """
        if not isinstance(input_data, dict):
            return {"success": False, "summary": "", "error": "Input must be a dictionary."}

        text = input_data.get("text", "")
        length = input_data.get("length", DEFAULT_SUMMARY_LENGTH)

        if not isinstance(text, str) or not text.strip():
            return {"success": False, "summary": "", "error": "Empty document."}

        sentences = self._split_sentences(text)
        if not sentences:
            return {"success": False, "summary": "", "error": "No sentences found."}

        word_frequencies = self._word_frequencies(text)
        scored = []
        for index, sentence in enumerate(sentences):
            score = self._score_sentence(sentence, word_frequencies)
            # Small bonus for sentences near the beginning of the document.
            if index < 3:
                score *= 1.1
            scored.append((index, sentence.strip(), score))

        top = sorted(scored, key=lambda x: x[2], reverse=True)[:length]
        top_in_order = sorted(top, key=lambda x: x[0])
        summary = " ".join(s for _, s, _ in top_in_order)

        logger.info("SummaryTool produced summary with %d sentences.", len(top_in_order))
        return {"success": True, "summary": summary, "error": None}

    # ----- private helpers -----

    def _split_sentences(self, text: str) -> list:
        return [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    def _word_frequencies(self, text: str) -> Counter:
        words = re.findall(r"[A-Za-z']+", text.lower())
        words = [w for w in words if w not in self.STOPWORDS and len(w) > 2]
        return Counter(words)

    def _score_sentence(self, sentence: str, freqs: Counter) -> float:
        words = re.findall(r"[A-Za-z']+", sentence.lower())
        return sum(freqs.get(w, 0) for w in words)
