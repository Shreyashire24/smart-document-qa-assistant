"""
Main entry point for the Smart Document Q&A Assistant.

Usage:
    python main.py path/to/document.pdf
    python main.py path/to/document.txt
"""

import argparse
import logging
from agent import Agent
from config import LOG_FORMAT, LOG_LEVEL, EXIT_KEYWORDS


def setup_logging() -> None:
    """Configure root logging using values from config.py."""
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)


def parse_arguments() -> argparse.Namespace:
    """Parse the document file path from the command line."""
    parser = argparse.ArgumentParser(
        description=(
            "Smart Document Q&A Assistant — ask questions about a local "
            "PDF or text document."
        )
    )
    parser.add_argument("file", help="Path to a .pdf or .txt document.")
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_arguments()

    agent = Agent()
    print(f"Loading document: {args.file}")
    load_result = agent.load_document(args.file)
    if not load_result["success"]:
        print(f"Could not load document: {load_result['error']}")
        return

    meta = load_result["metadata"]
    print(f"Document loaded ({meta['character_count']} characters).")
    print("Ask a question about the document. Type 'exit' to quit.\n")

    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if question.lower() in EXIT_KEYWORDS:
            print("Goodbye.")
            break
        if not question:
            continue

        answer = agent.ask(question)
        print(answer + "\n")


if __name__ == "__main__":
    main()
