"""
Unit tests for NLPMethods class.

This module contains tests for the NLP methods and utilities.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import hw.shared.nlp_methods
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hw.shared.nlp_methods import NLPMethods


class TestNLPMethods:
    """Test cases for NLPMethods class."""

    @pytest.fixture
    def nlp_instance(self):
        """Create an NLPMethods instance for testing."""
        # Use a dummy URL since we're only testing extract_quotes
        return NLPMethods("http://example.com")

    def test_extract_quotes_basic_double_quotes(self, nlp_instance):
        """
        Test extract_quotes with basic double quotes.

        This test verifies that the function correctly extracts text
        between standard double quotes.
        """
        text = 'He said "Hello world" and then "Goodbye" to everyone.'
        result = nlp_instance.extract_quotes(text)

        assert result == ["Hello world", "Goodbye"]
        assert len(result) == 2

    def test_extract_quotes_unicode_quotes(self, nlp_instance):
        """
        Test extract_quotes with Unicode quotes.

        This test verifies that the function correctly extracts text
        between Unicode left/right double quotes.
        """
        text = 'She said "Welcome" and then "Farewell" to the guests.'
        result = nlp_instance.extract_quotes(text)

        assert result == ["Welcome", "Farewell"]
        assert len(result) == 2

    def test_extract_quotes_single_quotes(self, nlp_instance):
        """
        Test extract_quotes with single quotes.

        This test verifies that the function correctly extracts text
        between single quotes.
        """
        text = "He said 'Hello there' and then 'See you later' to his friend."
        result = nlp_instance.extract_quotes(text)

        assert result == ["Hello there", "See you later"]
        assert len(result) == 2

    def test_extract_quotes_mixed_quote_types(self, nlp_instance):
        """
        Test extract_quotes with mixed quote types.

        This test verifies that the function correctly extracts text
        when multiple quote types are present in the same text.
        """
        text = "He said \"Hello\" and then 'Goodbye' to everyone."
        result = nlp_instance.extract_quotes(text)

        assert "Hello" in result
        assert "Goodbye" in result
        assert len(result) == 2

    def test_extract_quotes_empty_string(self, nlp_instance):
        """
        Test extract_quotes with empty string.

        This test verifies that the function returns an empty list
        when given an empty string.
        """
        text = ""
        result = nlp_instance.extract_quotes(text)

        assert result == []

    def test_extract_quotes_no_quotes(self, nlp_instance):
        """
        Test extract_quotes with text containing no quotes.

        This test verifies that the function returns an empty list
        when no quotes are present in the text.
        """
        text = "This is just plain text with no quotes at all."
        result = nlp_instance.extract_quotes(text)

        assert result == []

    def test_extract_quotes_nested_quotes(self, nlp_instance):
        """
        Test extract_quotes with nested quotes.

        This test verifies that the function correctly handles
        nested quote patterns.
        """
        text = "He said \"She told me 'Hello there' yesterday\" to the group."
        result = nlp_instance.extract_quotes(text)

        # Should extract both the outer double quote content and the inner single quote
        assert len(result) >= 1
        assert any("She told me" in quote for quote in result)

    def test_extract_quotes_whitespace_handling(self, nlp_instance):
        """
        Test extract_quotes with whitespace handling.

        This test verifies that the function correctly strips whitespace
        from extracted quotes.
        """
        text = 'He said "  Hello world  " and then "  Goodbye  " to everyone.'
        result = nlp_instance.extract_quotes(text)

        assert result == ["Hello world", "Goodbye"]
        assert len(result) == 2

    def test_remove_quotes_basic_double_quotes(self, nlp_instance):
        """
        Test remove_quotes with basic double quotes.

        This test verifies that the function correctly removes text
        between double quotes.
        """
        text = 'He said "Hello world" and then "Goodbye" to everyone.'
        result = nlp_instance.remove_quotes(text)

        assert result == "He said and then to everyone."
        assert isinstance(result, str)

    def test_remove_quotes_unicode_quotes(self, nlp_instance):
        """
        Test remove_quotes with Unicode quotes.

        This test verifies that the function correctly removes text
        between Unicode left/right double quotes.
        """
        text = 'She said "Welcome" and then "Farewell" to the guests.'
        result = nlp_instance.remove_quotes(text)

        assert result == "She said and then to the guests."
        assert isinstance(result, str)

    def test_get_chapter_data_basic_functionality(self, nlp_instance):
        """
        Test get_chapter_data with basic chapter extraction.

        This test verifies that the function correctly extracts chapter data
        including content, metrics, and handles the dedication marker removal.
        """
        # Create test text with dedication marker and chapters
        test_text = """Some preamble text here.

To Romain Rolland, my dear friend

CHAPTER I: THE BEGINNING
This is the content of the first chapter. It contains multiple sentences. 
The chapter discusses various topics and provides detailed information.
It has enough content to meet the minimum length requirement.

CHAPTER II: THE MIDDLE
This is the content of the second chapter. It also contains multiple sentences.
The chapter continues the narrative and provides more detailed information.
It meets the minimum content length requirement as well.

CHAPTER III: THE END
This is the final chapter content. It concludes the narrative.
It provides a satisfying ending to the story.
"""

        chapters = [
            "CHAPTER I: THE BEGINNING",
            "CHAPTER II: THE MIDDLE",
            "CHAPTER III: THE END",
        ]

        result = nlp_instance.get_chapter_data(chapters, test_text)

        # Verify we got results for all chapters
        assert len(result) == 3

        # Test first chapter
        first_chapter = result[0]
        assert first_chapter["chapter_title"] == "CHAPTER I: THE BEGINNING"
        assert first_chapter["chapter_number"] == 1
        assert first_chapter["sentence_count"] > 0
        assert first_chapter["word_count"] > 0
        assert first_chapter["token_count"] > 0
        assert first_chapter["character_count"] > 100
        assert "This is the content of the first chapter" in first_chapter["content"]

        # Test second chapter
        second_chapter = result[1]
        assert second_chapter["chapter_title"] == "CHAPTER II: THE MIDDLE"
        assert second_chapter["chapter_number"] == 2
        assert second_chapter["sentence_count"] > 0
        assert second_chapter["word_count"] > 0
        assert "This is the content of the second chapter" in second_chapter["content"]

        # Test third chapter
        third_chapter = result[2]
        assert third_chapter["chapter_title"] == "CHAPTER III: THE END"
        assert third_chapter["chapter_number"] == 3
        assert third_chapter["sentence_count"] > 0
        assert third_chapter["word_count"] > 0
        assert "This is the final chapter content" in third_chapter["content"]

        # Verify that dedication marker was removed from content
        for chapter in result:
            assert "To Romain Rolland, my dear friend" not in chapter["content"]
            assert "Some preamble text here" not in chapter["content"]
