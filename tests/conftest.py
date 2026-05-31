"""Pytest configuration — adds the project root to sys.path."""

import os
import sys

# Ensure the project root (one level up from tests/) is on sys.path so
# `import agent`, `import config`, etc. work when running pytest from the
# repository root.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
