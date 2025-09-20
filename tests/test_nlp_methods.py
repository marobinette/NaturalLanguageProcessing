"""
Unit tests for NLPMethods class.

This module contains tests for the NLP methods and utilities.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import hw.shared.nlp_methods
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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
        text = 'He said "Hello" and then \'Goodbye\' to everyone.'
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
        text = 'He said "She told me \'Hello there\' yesterday" to the group.'
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
