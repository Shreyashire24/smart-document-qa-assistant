"""
Search Tool.

Performs keyword-based search inside a document. Splits the document into
sentences, extracts non-stopword keywords from the user's question, scores
each sentence by how many keywords it contains, and returns the top-scoring
sentences with their position number.
"""

import re
import logging
from config import DEFAULT_MAX_SEARCH_RESULTS

logger = logging.getLogger(__name__)


class SearchTool:
    """Finds sentences in the document that match the user's question."""

    name = "search"

    STOPWORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "of", "in", "on", "at", "to", "for", "and", "or", "but",
        "what", "who", "where", "when", "why", "how", "which",
        "does", "do", "did", "this", "that", "these", "those",
        "it", "its", "as", "by", "with", "about", "from",
    }

    def run(self, input_data: dict) -> dict:
        """
        Search the document for sentences matching the question.

        Args:
            input_data: Dictionary with keys 'question' and 'text'.

        Returns:
            A dictionary with keys 'success', 'results', 'error'.
        """
        question = input_data.get("question", "") if isinstance(input_data, dict) else ""
        text = input_data.get("text", "") if isinstance(input_data, dict) else ""

        if not question or not text:
            return {"success": False, "results": [], "error": "Missing question or text."}

        keywords = self._extract_keywords(question)
        if not keywords:
            return {"success": False, "results": [], "error": "No usable keywords in question."}

        logger.info("SearchTool extracted keywords: %s", keywords)

        sentences = self._split_sentences(text)
        matches = []
        for index, sentence in enumerate(sentences):
            score = self._score_sentence(sentence, keywords)
            if score > 0:
                matches.append({
                    "sentence": sentence.strip(),
                    "position": index + 1,
                    "score": score,
                })

        matches.sort(key=lambda m: m["score"], reverse=True)
        top_matches = matches[:DEFAULT_MAX_SEARCH_RESULTS]
        return {"success": True, "results": top_matches, "error": None}

    # ----- private helpers -----

    def _extract_keywords(self, question: str) -> list:
        words = re.findall(r"[A-Za-z']+", question.lower())
        return [w for w in words if w not in self.STOPWORDS and len(w) > 2]

    def _split_sentences(self, text: str) -> list:
        return [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    def _score_sentence(self, sentence: str, keywords: list) -> int:
        lower = sentence.lower()
        return sum(1 for kw in keywords if kw in lower)
