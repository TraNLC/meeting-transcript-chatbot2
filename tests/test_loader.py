"""Tests for transcript loader."""

import pytest
from pathlib import Path
from src.data.loader import TranscriptLoader


def test_load_txt_file():
    """Test loading TXT file."""
    loader = TranscriptLoader()
    content = loader.load_file("data/transcripts/sample_meeting.txt")
    assert isinstance(content, str)
    assert len(content) > 0
    assert "TRANSCRIPT" in content


def test_load_nonexistent_file():
    """Test loading non-existent file."""
    loader = TranscriptLoader()
    with pytest.raises(FileNotFoundError):
        loader.load_file("nonexistent.txt")


def test_load_unsupported_format():
    """Test loading unsupported file format."""
    loader = TranscriptLoader()
    with pytest.raises(ValueError):
        loader.load_file("test.pdf")
