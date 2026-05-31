# Smart Document Q&A Assistant

A lightweight, fully offline Python command-line application that lets a user load a local document (`.pdf` or `.txt`) and ask questions about its content in natural language. The system classifies each question into an intent — **summary**, **statistics**, or **keyword search** — routes it to the matching tool, and returns a structured, human-readable answer.

Developed as part of the **Applied System Software (DIP392)** course at Riga Technical University.

---

## Table of Contents

1. [Project Goal](#project-goal)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Example Session](#example-session)
7. [Architecture](#architecture)
8. [Tools](#tools)
9. [Configuration](#configuration)
10. [Testing](#testing)
11. [Deployment Strategy](#deployment-strategy)
12. [Project Evolution](#project-evolution)
13. [Author](#author)

---

## Project Goal

To provide a lightweight, fully offline assistant that helps users quickly extract specific information from long documents without having to read them in full. Useful for students reviewing study materials, employees scanning long reports, and researchers exploring articles.

The system runs entirely on the local machine and does **not** depend on any paid API, large language model, or external web service.

## Features

- Loads and parses both `.pdf` and `.txt` files locally.
- Classifies user questions into three intents using rule-based pattern matching:
  - **Summary** — for questions containing words like *summarize*, *summary*, *overview*.
  - **Statistics** — for questions containing phrases like *how many*, *count*, *number of*, *average*.
  - **Keyword search** — for all other non-empty questions.
- Returns structured answers with sentence positions for traceability.
- Handles invalid input (missing file, unsupported format, empty document, unrecognised question) without crashing.
- Logs every agent decision and every tool call for full traceability.
- Fully offline, no API keys required, no paid services.

## Project Structure

```
smart-document-qa-assistant/
├── main.py                       # CLI entry point and interactive loop
├── agent.py                      # Agent class — intent detection and dispatch
├── config.py                     # Centralised configuration values
├── requirements.txt              # External dependencies
├── README.md                     # This file
├── .gitignore                    # Files excluded from version control
├── tools/                        # Tool package
│   ├── __init__.py
│   ├── file_reader.py            # Reads .pdf and .txt files
│   ├── search_tool.py            # Keyword search inside documents
│   ├── summary_tool.py           # Extractive summarisation
│   └── statistics_tool.py        # Word/sentence/frequency statistics
├── tests/                        # Pytest test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── sample.txt
│   │   └── empty.txt
│   ├── test_file_reader.py       # Group A scenarios
│   ├── test_search_tool.py       # Group B scenarios
│   ├── test_summary_tool.py      # Group C scenarios
│   ├── test_statistics_tool.py   # Group D scenarios
│   └── test_agent.py             # Group E integration scenarios
└── sample_documents/             # Example documents to try the app
    └── photosynthesis.txt
```

## Installation

The system requires **Python 3.10 or newer**.

```bash
# 1. Clone or download this repository.
git clone https://github.com/<your-username>/smart-document-qa-assistant.git
cd smart-document-qa-assistant

# 2. Create a virtual environment.
python -m venv .venv

# 3. Activate the virtual environment.
#    Windows (PowerShell):
.venv\Scripts\Activate.ps1
#    Windows (cmd.exe):
.venv\Scripts\activate.bat
#    Linux/macOS:
source .venv/bin/activate

# 4. Install dependencies.
pip install -r requirements.txt
```

No API keys, environment variables, or external services are required.

## Usage

```bash
python main.py <path-to-document>
```

The path can point to any `.pdf` or `.txt` file on your machine. A sample document is provided in `sample_documents/`.

### Quick start

```bash
python main.py sample_documents/photosynthesis.txt
```

After launching, the program prints a confirmation message and enters an interactive loop where you can type one question after another. Type `exit`, `quit`, or `q` (or press `Ctrl+C`) to leave the loop.

### Supported question types

| Intent | Example questions |
|---|---|
| Summary | *"summarize this document"*, *"give me an overview"*, *"tl;dr"* |
| Statistics | *"how many words"*, *"how many sentences"*, *"average sentence length"*, *"most common words"* |
| Keyword search | *"what does it say about chlorophyll"*, *"who is mentioned in chapter two"*, *"where does photosynthesis happen"* |

## Example Session

```
$ python main.py sample_documents/photosynthesis.txt
Loading document: sample_documents/photosynthesis.txt
Document loaded (1985 characters).
Ask a question about the document. Type 'exit' to quit.

> summarize this document
Summary:
Photosynthesis is the biological process by which green plants, algae,
and some bacteria convert light energy into chemical energy. During
photosynthesis, water absorbed by the roots and carbon dioxide taken in
from the air are combined to produce glucose and oxygen. Photosynthesis
is divided into two main stages: the light-dependent reactions and the
light-independent reactions, also known as the Calvin cycle.

> how many words
Document statistics:
- Words: 305
- Sentences: 13
- Average sentence length: 23.46 words
- Most common words: the (29), and (15), photosynthesis (10), of (10), is (8)

> what about chlorophyll
Top matches:
  [sentence 2] The process takes place inside specialised organelles
  called chloroplasts, which contain the green pigment chlorophyll.
  [sentence 3] Chlorophyll absorbs energy from sunlight, especially in
  the red and blue parts of the visible spectrum, and uses that energy
  to drive a series of chemical reactions.

> exit
Goodbye.
```

## Architecture

The system is implemented as a **single intelligent agent** following the classic `Input → Reasoning → Tool Use → Output` workflow.

```
                ┌─────────────────────────────────────────┐
                │             main.py (CLI)              │
                │  argparse  •  interactive input loop   │
                └────────────────────┬───────────────────┘
                                     │ user question
                                     ▼
                ┌─────────────────────────────────────────┐
                │                Agent                    │
                │  intent detection   tool registry       │
                │  result formatting                       │
                └──────┬──────┬──────────────┬────────────┘
                       │      │              │
              ┌────────▼─┐  ┌─▼────────┐  ┌──▼────────────┐
              │ Summary  │  │  Stats   │  │   Search      │
              │  Tool    │  │  Tool    │  │   Tool        │
              └──────────┘  └──────────┘  └───────────────┘
                       ▲
                       │ document text (loaded once at startup)
                ┌──────┴──────────────────────────────────┐
                │           File Reader Tool              │
                │     .txt (open)   •   .pdf (pypdf)      │
                └─────────────────────────────────────────┘
```

### Tool API (internal contract)

Every tool exposes a single public `run` method and returns a dictionary with a fixed shape:

```python
{
    "success": bool,          # True if the tool produced a usable result
    # tool-specific fields:   text/metadata, results, summary, or stats
    "error":  str | None,     # human-readable error message on failure
}
```

This uniform contract keeps the agent simple and makes every tool independently testable.

## Tools

| Tool | Purpose | Input | Output |
|---|---|---|---|
| **File Reader** | Loads and extracts text from `.pdf` and `.txt` files. | `str` file path | `dict` with `text` and `metadata` |
| **Search** | Keyword search over the document. | `dict` with `question`, `text` | `dict` with ranked `results` |
| **Summary** | Extractive summary based on word frequency. | `dict` with `text`, optional `length` | `dict` with `summary` |
| **Statistics** | Word count, sentence count, average sentence length, most common words. | `dict` with `text` | `dict` with `stats` |

## Configuration

All tunable values live in `config.py`:

| Constant | Purpose |
|---|---|
| `SUPPORTED_EXTENSIONS` | File extensions the File Reader accepts. |
| `DEFAULT_SUMMARY_LENGTH` | Default number of sentences in a generated summary. |
| `DEFAULT_MAX_SEARCH_RESULTS` | Maximum number of sentences returned by Search. |
| `LOG_FORMAT`, `LOG_LEVEL` | Logging format and level used across the project. |
| `EXIT_KEYWORDS` | Words that exit the interactive loop. |

No environment variables are needed.

## Testing

The project uses **pytest**. The test suite is organised into five groups that mirror the system's architecture:

| Group | File | Covers |
|---|---|---|
| A | `tests/test_file_reader.py` | Loading `.txt` files, missing files, unsupported formats, empty files. |
| B | `tests/test_search_tool.py` | Keyword matching, no-match queries, stopword-only queries, empty input, result ranking. |
| C | `tests/test_summary_tool.py` | Multi-sentence summary, custom length, empty document. |
| D | `tests/test_statistics_tool.py` | Word/sentence counts, average sentence length, most common words. |
| E | `tests/test_agent.py` | End-to-end intent detection, formatted answers, fallback for unknown intent, guard before loading. |

### Run the tests

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

## Deployment Strategy

The system is currently deployed as a **local command-line application** distributed through this GitHub repository. This strategy matches the design and the needs of the users:

- Single-user, fully offline.
- No network or API dependencies.
- Plain text output suitable for a terminal.
- One-command installation from a Git checkout.

### Future deployment stages

| Stage | Description |
|---|---|
| 1. Local CLI (current) | Distributed through this repository. |
| 2. Python wheel | Package and publish to a private package index. Installation becomes a single `pip install`. |
| 3. HTTP service | Wrap the `Agent` in a small FastAPI app exposing `/load` and `/ask` endpoints. |
| 4. LLM-enhanced agent | Optionally replace rule-based intent detection with an external LLM behind the same internal Tool API. |

Each future stage would go through a staged release in a test environment before any user-facing deployment, using the existing `pytest` suite as the regression baseline.

## Project Evolution

This project was developed in four submission stages, with the repository commit history reflecting each stage:

| Stage | Date | Focus |
|---|---|---|
| **Step 1** | 24.04 | Concept, agent approach, tool list, programming concepts. |
| **Step 2** | 08.05 | Implementation — modules, agent logic, tool integration. |
| **Step 3** | 15.05 | Testing process, test scenarios, deployment preparation, data conversion. |
| **Final** | 22.05 | Final report, deployment strategy, GitHub link. |

## Author

**Shreyas Hirekodathakallu Anantharamaiah**
Student ID: **231ADB170**
Course: **Applied System Software (DIP392)**
Riga Technical University
