import urllib.request
import nltk
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import re
import pandas as pd
import random

class NLPMethods:
    """
    A class containing various NLP methods and utilities.
    """
    # Quote patterns for extraction and removal
    QUOTE_EXTRACTION_PATTERNS = [
        r'"([^"]*)"',      # Straight double quotes
        r"“([^“”]*)”",      # Unicode left/right double quotes (8220, 8221) - multiline
        r"'([^']*)'",      # Unicode left/right single quotes (8216, 8217) - multiline
        r"'([^']*)'",      # Straight single quotes
    ]
    
    QUOTE_REMOVAL_PATTERNS = [
        r'"[^"]*"',        # Straight double quotes
        r"“[^“”]*”",        # Unicode left/right double quotes (8220, 8221) - multiline
        r"'[^']*'",        # Unicode left/right single quotes (8216, 8217) - multiline
        r"'[^']*'",        # Straight single quotes
    ]
    
    def __init__(self):
        """
        Initialize the NLPMethods class.
        """
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK Punkt tokenizer...")
            nltk.download('punkt', quiet=True)
    
    def hello_from_class(self):
        """
        A simple method that prints a greeting message.
        """
        print("hello from class")

    def remove_gutenberg_header(self, url):
        """
        Extract text between Gutenberg start and end markers.
        Returns only the actual book content, removing headers and footers.
        """
        response = urllib.request.urlopen(url)
        text = response.read().decode('utf-8')
        
        # Find the start marker
        start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK SIDDHARTHA ***"
        end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK SIDDHARTHA ***"
        
        start_index = text.find(start_marker)
        end_index = text.find(end_marker)
        
        if start_index != -1 and end_index != -1:
            # Extract text between the markers
            start_index += len(start_marker)
            extracted_text = text[start_index:end_index].strip()
            return extracted_text
        else:
            # If markers not found, return original text
            print("Warning: Gutenberg markers not found, returning original text")
            return text

    def fetch_corpus(self, text):
        """
        Process text and return sentences, tokens, quotes, and non-quotes.
        """
        content = text
        quotes = self.extract_quotes(content)
        content = ' '.join(content.split()) 
        non_quote_content = self.remove_quotes(content)
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        quote_sentences = []
        non_quote_sentences = []
        
        for sentence in sentences:
            has_quotes = False
            for pattern in self.QUOTE_EXTRACTION_PATTERNS:
                if re.search(pattern, sentence):
                    has_quotes = True
                    break
 
            if has_quotes:
                quote_sentences.append(sentence)
            else:
                non_quote_sentences.append(sentence)

        tokenizer = RegexpTokenizer(r'\w+[\'\"]*|\'|\"')
        tokenized_sentences = [tokenizer.tokenize(sentence) for sentence in sentences]

        all_tokens = [token for sentence in tokenized_sentences for token in sentence]
        quote_tokens = []
        non_quote_tokens = []
        for token in all_tokens:
            is_quote_token = False
            for pattern in self.QUOTE_EXTRACTION_PATTERNS:
                if re.search(pattern, token):
                    is_quote_token = True
                    break

            if is_quote_token:
                quote_tokens.append(token)
            else:
                non_quote_tokens.append(token)

        print(f"Number of sentences: {len(sentences)}")
        print(f"Number of quotes found: {len(quotes)}")
        print(f"Quote sentences: {len(quote_sentences)}")
        print(f"Non-quote sentences: {len(non_quote_sentences)}")
        print(f"Quote tokens: {len(quote_tokens)}")
        print(f"Non-quote tokens: {len(non_quote_tokens)}")

        return {
            'sentences': sentences,
            'tokenized_sentences': tokenized_sentences,
            'all_tokens': all_tokens,
            'quotes': quotes,
            'non_quotes': non_quote_content,
            'quote_sentences': quote_sentences,
            'non_quote_sentences': non_quote_sentences,
            'quote_tokens': quote_tokens,
            'non_quote_tokens': non_quote_tokens
        }

    def extract_quotes(self, text):
        """
        Naive approach: Extract anything between double quotes.
        Returns list of quoted text (without the quote marks).
        """
        all_quotes = []
        for pattern in self.QUOTE_EXTRACTION_PATTERNS:
            quotes = re.findall(pattern, text, re.DOTALL)
            all_quotes.extend([quote.strip() for quote in quotes if quote.strip()])

        return all_quotes

    def remove_quotes(self, text):
        """
        Remove all quoted text from the content, leaving only narrative/non-dialogue.
        """
        non_quote_text = text
        for pattern in self.QUOTE_REMOVAL_PATTERNS:
            non_quote_text = re.sub(pattern, '', non_quote_text, flags=re.DOTALL)

        non_quote_text = ' '.join(non_quote_text.split())

        return non_quote_text
    
    def get_chapter_data(self, chapters, text):    
        """
        Extract chapter data from text using a list of chapter titles.
        Returns a list of dictionaries containing chapter content and length metrics.
        """
        # Split text into lines for easier processing
        lines = text.split('\n')
        chapters_data = []
        chapter_headers = ['FIRST PART', 'SECOND PART']
        
        for i, chapter_title in enumerate(chapters):
            # Find the chapter title in the text
            chapter_start = -1
            for j, line in enumerate(lines):
                if line.strip() == chapter_title:
                    chapter_start = j
                    break
            
            if chapter_start == -1:
                continue  # Skip if chapter not found
            
            # Find the end of this chapter (next chapter title or end of text)
            chapter_end = len(lines)
            for j in range(chapter_start + 1, len(lines)):
                next_line = lines[j].strip()
                # Check if next line is another chapter title
                if re.match(r'^[A-Z\s]+$', next_line) and len(next_line) > 2:
                    if next_line not in chapter_headers and next_line in chapters:
                        chapter_end = j
                        break
            
            # Extract chapter content
            chapter_lines = lines[chapter_start:chapter_end]
            # Clean up the content (remove the title line and extra whitespace)
            content_lines = chapter_lines[1:]  # Skip the title line
            content = '\n'.join(content_lines).strip()
            
            # Only add if there's substantial content (more than just the title)
            if len(content) > 100:  # Minimum content length threshold
                # Count sentences
                sentences = re.split(r'[.!?]+', content)
                sentences = [s.strip() for s in sentences if s.strip()]
                
                # Count words (simple word count)
                words = content.split()
                word_count = len(words)
                
                # Count tokens using the same tokenizer as in fetch_corpus
                tokenizer = RegexpTokenizer(r'\w+[\'\"]*|\'|\"')
                tokens = tokenizer.tokenize(content)
                token_count = len(tokens)
                
                # Calculate character count
                char_count = len(content)
                
                chapters_data.append({
                    'chapter_title': chapter_title,
                    'chapter_number': i + 1,
                    'start_line': chapter_start + 1,  # 1-indexed
                    'end_line': chapter_end,
                    'sentence_count': len(sentences),
                    'word_count': word_count,
                    'token_count': token_count,
                    'character_count': char_count,
                    'content': content
                })
        
        return chapters_data

    def get_chapters(self, text, shuffle=False):
        """
        Extract chapters from text using regex to find all-caps chapter titles.
        Returns a list containing the chapter titles.
        """
        # Split text into lines for easier processing
        lines = text.split('\n')
        found_chapters = []
        chapter_headers = ['FIRST PART', 'SECOND PART']
        
        for line in lines:
            line = line.strip()
            # Match complete lines that are all-caps (not just individual words)
            if re.match(r'^[A-Z\s]+$', line) and len(line) > 2:
                if line not in chapter_headers and line not in found_chapters:
                    found_chapters.append(line)
        if shuffle:
            shuffled = found_chapters.copy()
            random.shuffle(shuffled)
            random_sample = shuffled[:10]
            return random_sample
        return found_chapters
    
    def chapters_to_dataframe(self, chapters_data):
        """
        Convert chapters data to a pandas DataFrame.
        Returns a DataFrame with chapter information.
        """
        return pd.DataFrame(chapters_data)