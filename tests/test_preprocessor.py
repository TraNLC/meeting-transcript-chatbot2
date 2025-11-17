"""Tests for text preprocessor."""

import pytest
from src.data.preprocessor import TranscriptPreprocessor


def test_clean_text():
    """Test text cleaning."""
    # Test multiple spaces
    text = "This  is   a    test"
    cleaned = TranscriptPreprocessor.clean_text(text)
    assert cleaned == "This is a test"
    
    # Test multiple newlines
    text = "Line 1\n\n\nLine 2"
    cleaned = TranscriptPreprocessor.clean_text(text)
    assert "Line 1" in cleaned
    assert "Line 2" in cleaned


def test_truncate_text():
    """Test text truncation."""
    # Test short text (no truncation)
    text = "Short text"
    truncated = TranscriptPreprocessor.truncate_text(text, max_length=100)
    assert truncated == text
    
    # Test long text (with truncation)
    text = "A" * 1000
    truncated = TranscriptPreprocessor.truncate_text(text, max_length=100)
    assert len(truncated) > 100  # Includes truncation message
    assert "cắt ngắn" in truncated


def test_empty_text():
    """Test with empty text."""
    cleaned = TranscriptPreprocessor.clean_text("")
    assert cleaned == ""
