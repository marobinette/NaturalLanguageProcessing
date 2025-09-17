import urllib.request
import nltk
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import re

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

    def fetch_corpus(self, url):
        """
        Fetch a corpus from a given URL and return sentences, tokens, quotes, and non-quotes.
        """
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        quotes = self.extract_quotes_naive(content)
        content = ' '.join(content.split()) 
        non_quote_content = self.remove_quotes_naive(content)
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

    def extract_quotes_naive(self, text):
        """
        Naive approach: Extract anything between double quotes.
        Returns list of quoted text (without the quote marks).
        """
        all_quotes = []
        for pattern in self.QUOTE_EXTRACTION_PATTERNS:
            quotes = re.findall(pattern, text, re.DOTALL)
            all_quotes.extend([quote.strip() for quote in quotes if quote.strip()])

        return all_quotes

    def remove_quotes_naive(self, text):
        """
        Remove all quoted text from the content, leaving only narrative/non-dialogue.
        """
        non_quote_text = text
        for pattern in self.QUOTE_REMOVAL_PATTERNS:
            non_quote_text = re.sub(pattern, '', non_quote_text, flags=re.DOTALL)

        non_quote_text = ' '.join(non_quote_text.split())

        return non_quote_text
    