"""
Configuration module for the Smart Document Q&A Assistant.

All constants and configuration values are stored here so they can be
changed in a single place without modifying business logic.
"""

# Supported file extensions for the File Reader Tool.
SUPPORTED_EXTENSIONS = [".pdf", ".txt"]

# Default number of sentences returned by the Summary Tool.
DEFAULT_SUMMARY_LENGTH = 3

# Default maximum number of search results returned by the Search Tool.
DEFAULT_MAX_SEARCH_RESULTS = 5

# Logging configuration shared across the project.
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# Keywords that exit the interactive loop in main.py.
EXIT_KEYWORDS = ["exit", "quit", "q"]
