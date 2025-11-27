"""
Resource loading utilities for the AI Digital Twin backend.

This module is responsible for loading and exposing personal data resources
used to enrich the Digital Twin's behaviour. It reads:

1. A LinkedIn/CV-style PDF (linkedin.pdf) using pypdf
2. A natural-language professional summary (summary.txt)
3. A communication style description (style.txt)
4. Structured factual information (facts.json)

The loaded content is made available as module-level variables:

- linkedin : str  -> extracted text from the LinkedIn PDF (or fallback message)
- summary  : str  -> professional summary text
- style    : str  -> communication style description
- facts    : dict -> structured facts about the persona

These resources can then be combined into prompts or used by downstream logic
in server.py or other backend components.
"""

# ============================================================
# Imports
# ============================================================

from pypdf import PdfReader
import json
from typing import Any, Dict


# ============================================================
# Helper Functions
# ============================================================

def _load_linkedin_pdf(path: str = "./data/linkedin.pdf") -> str:
    """
    Load and extract text content from the LinkedIn/CV PDF.

    Parameters
    ----------
    path : str, optional
        Relative path to the PDF file, by default "./data/linkedin.pdf".

    Returns
    -------
    str
        The concatenated text extracted from all pages of the PDF.
        If the file is not found, returns a fallback message.
    """
    try:
        # Create a PdfReader instance for the given file path
        reader: PdfReader = PdfReader(path)

        # Accumulate extracted text from all pages
        extracted_text: str = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text

        return extracted_text or "LinkedIn profile could not be extracted"

    except FileNotFoundError:
        # Graceful fallback if the PDF is missing
        return "LinkedIn profile not available"


def _load_text_file(path: str) -> str:
    """
    Load a UTF-8 text file from disk.

    Parameters
    ----------
    path : str
        Relative path to the text file.

    Returns
    -------
    str
        The full contents of the file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _load_json_file(path: str) -> Dict[str, Any]:
    """
    Load a JSON file from disk and parse it into a Python dictionary.

    Parameters
    ----------
    path : str
        Relative path to the JSON file.

    Returns
    -------
    Dict[str, Any]
        The parsed JSON content.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Resource Loading (Module-Level)
# ============================================================

# Extracted LinkedIn/CV-style information as plain text
linkedin: str = _load_linkedin_pdf("./data/linkedin.pdf")

# Professional summary describing the persona
summary: str = _load_text_file("./data/summary.txt")

# Communication style preferences
style: str = _load_text_file("./data/style.txt")

# Structured factual profile (name, location, specialties, education, etc.)
facts: Dict[str, Any] = _load_json_file("./data/facts.json")
