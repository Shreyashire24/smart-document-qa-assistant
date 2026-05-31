"""
Agent module.

The Agent class owns the loaded document and a registry of tools. It
performs rule-based intent detection on the user's question, dispatches
to the appropriate tool, and formats the result for the user.
"""

import logging
from tools.file_reader import FileReaderTool
from tools.search_tool import SearchTool
from tools.summary_tool import SummaryTool
from tools.statistics_tool import StatisticsTool

logger = logging.getLogger(__name__)


class Agent:
    """Single intelligent agent that routes user questions to tools."""

    def __init__(self) -> None:
        self.file_reader = FileReaderTool()
        self.tools = {
            "summary": SummaryTool(),
            "statistics": StatisticsTool(),
            "search": SearchTool(),
        }
        self.document_text: str | None = None
        self.document_metadata: dict | None = None

    # ----- document loading -----

    def load_document(self, file_path: str) -> dict:
        """Use the File Reader Tool to load a document into memory."""
        result = self.file_reader.run(file_path)
        if result["success"]:
            self.document_text = result["text"]
            self.document_metadata = result["metadata"]
        return result

    # ----- intent detection -----

    def detect_intent(self, question: str) -> str:
        """Classify the user's question into one of three intents."""
        if not isinstance(question, str):
            return "unknown"
        q = question.lower()
        if not q.strip():
            return "unknown"

        summary_keywords = [
            "summary", "summarize", "summarise", "tl;dr", "brief", "overview",
        ]
        statistics_keywords = [
            "how many", "count", "number of", "most common",
            "word count", "average",
        ]

        if any(k in q for k in summary_keywords):
            return "summary"
        if any(k in q for k in statistics_keywords):
            return "statistics"
        return "search"

    # ----- main dispatch -----

    def ask(self, question: str) -> str:
        """Process a question end-to-end and return a formatted answer."""
        if not self.document_text:
            return "No document is loaded. Please load a document first."

        intent = self.detect_intent(question)
        logger.info("Detected intent: %s", intent)

        if intent == "unknown":
            return "I could not understand your question. Please rephrase it."

        tool = self.tools[intent]
        payload = {"question": question, "text": self.document_text}
        result = tool.run(payload)
        return self._format(intent, result)

    # ----- formatting -----

    def _format(self, intent: str, result: dict) -> str:
        if not result.get("success"):
            return f"Error: {result.get('error', 'Unknown error.')}"

        if intent == "summary":
            return f"Summary:\n{result['summary']}"

        if intent == "statistics":
            stats = result["stats"]
            common = ", ".join(f"{w} ({c})" for w, c in stats["most_common_words"])
            return (
                "Document statistics:\n"
                f"- Words: {stats['word_count']}\n"
                f"- Sentences: {stats['sentence_count']}\n"
                f"- Average sentence length: {stats['average_sentence_length']} words\n"
                f"- Most common words: {common}"
            )

        # search
        results = result["results"]
        if not results:
            return "No matching content found in the document."
        lines = ["Top matches:"]
        for r in results:
            lines.append(f"  [sentence {r['position']}] {r['sentence']}")
        return "\n".join(lines)
