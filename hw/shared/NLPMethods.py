import urllib.request
import nltk
from nltk.tokenize import RegexpTokenizer
import re
import pandas as pd
import random
from pprint import pprint

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
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK Punkt tokenizer...")
            nltk.download('punkt', quiet=True)
    
    def remove_gutenberg_header(self, url):
        """
        Extract text between Gutenberg start and end markers.
        Returns only the actual book content, removing headers and footers.
        """
        response = urllib.request.urlopen(url)
        text = response.read().decode('utf-8')
        
        start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK SIDDHARTHA ***"
        end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK SIDDHARTHA ***"
        
        start_index = text.find(start_marker)
        end_index = text.find(end_marker)
        
        if start_index != -1 and end_index != -1:
            start_index += len(start_marker)
            extracted_text = text[start_index:end_index].strip()
            return extracted_text
        else:
            print("Warning: Gutenberg markers not found, returning original text")
            return text

    def get_processed_text(self, text):
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
        print("Longest dialogue:")
        pprint(self.get_longest_dialogue(content))

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
        lines = text.split('\n')
        chapters_data = []
        chapter_headers = ['FIRST PART', 'SECOND PART']
        
        for i, chapter_title in enumerate(chapters):
            chapter_start = -1
            for j, line in enumerate(lines):
                if line.strip() == chapter_title:
                    content_found = False
                    for k in range(j + 1, min(j + 11, len(lines))):
                        next_line = lines[k].strip()
                        if next_line and not re.match(r'^[A-Z\s]+$', next_line) and len(next_line) > 20:
                            content_found = True
                            break
                    
                    if content_found:
                        chapter_start = j
                        break
            
            if chapter_start == -1:
                continue
            
            chapter_end = len(lines)
            for j in range(chapter_start + 1, len(lines)):
                next_line = lines[j].strip()
                if re.match(r'^[A-Z\s]+$', next_line) and len(next_line) > 2:
                    if next_line not in chapter_headers and next_line in chapters:
                        chapter_end = j
                        break
            
            chapter_lines = lines[chapter_start:chapter_end]
            content_lines = chapter_lines[1:]  # Skip the title line
            content = '\n'.join(content_lines).strip()
            
            if len(content) > 100:
                sentences = re.split(r'[.!?]+', content)
                sentences = [s.strip() for s in sentences if s.strip()]
                
                words = content.split()
                word_count = len(words)
                
                tokenizer = RegexpTokenizer(r'\w+[\'\"]*|\'|\"')
                tokens = tokenizer.tokenize(content)
                token_count = len(tokens)
                
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
        lines = text.split('\n')
        found_chapters = []
        chapter_headers = ['FIRST PART', 'SECOND PART']
        
        for line in lines:
            line = line.strip()
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

    def get_longest_dialogue(self, text, distance_threshold=500):
        """
        Find the longest dialogue exchange (consecutive quotes) in the text.
        Returns the exchange with the most quotes and its metrics.
        """
        # Find all quote positions and content
        quote_positions = []
        for pattern in self.QUOTE_EXTRACTION_PATTERNS:
            for match in re.finditer(pattern, text, re.DOTALL):
                quote_positions.append({
                    'start': match.start(),
                    'end': match.end(),
                    'content': match.group(1).strip()
                })
        
        # Sort by position
        quote_positions.sort(key=lambda x: x['start'])
        
        # Group consecutive quotes into exchanges
        exchanges = []
        current_exchange = []
        
        for quote in quote_positions:
            if not current_exchange:
                current_exchange = [quote]
            else:
                # TODO: distance_threshold should be average length of chars in sentence
                last_quote = current_exchange[-1]
                if quote['start'] - last_quote['end'] < distance_threshold:
                    current_exchange.append(quote)
                else:
                    # Start new exchange
                    exchanges.append(current_exchange)
                    current_exchange = [quote]
    
        # Don't forget the last exchange
        if current_exchange:
            exchanges.append(current_exchange)
        
        # Find exchange with most quotes
        if not exchanges:
            return None
            
        longest_exchange = max(exchanges, key=len)
        
        # Calculate metrics for the entire exchange
        all_content = ' '.join([quote['content'] for quote in longest_exchange])
        
        return {
            'exchange': longest_exchange,
            'quote_count': len(longest_exchange),
            'total_character_count': len(all_content),
            'total_word_count': len(all_content.split()),
            'total_sentence_count': len(re.split(r'[.!?]+', all_content)),
            'exchange_content': all_content
        }

    def get_random_sample_chapter_data(self, chapters, text, sample_size=10):
        """
        Implement random sampling to extract random chapters from the corpus.
        Returns a list of chapter data dictionaries for the randomly selected chapters.
        """
        if len(chapters) < sample_size:
            print(f"Warning: Only {len(chapters)} chapters available, returning all chapters")
            return self.get_chapter_data(chapters, text)
        
        random_chapters = self.get_chapters(text, True)
        
        all_chapter_data = self.get_chapter_data(chapters, text)
        
        random_chapter_data = [chapter for chapter in all_chapter_data 
                             if chapter['chapter_title'] in random_chapters]
        
        return random_chapter_data

    def get_systematic_sample_chapter_data(self, chapters, text, step_size=None):
        """
        Implement systematic sampling to extract every nth chapter.
        If step_size is None, it will be calculated to get approximately 10 chapters.
        Returns a list of chapter data dictionaries for the systematically selected chapters.
        """
        if step_size is None:
            step_size = max(1, len(chapters) // 10)
        
        systematic_chapters = chapters[::step_size]
        
        all_chapter_data = self.get_chapter_data(chapters, text)
        
        systematic_chapter_data = [chapter for chapter in all_chapter_data 
                                 if chapter['chapter_title'] in systematic_chapters]
        
        return systematic_chapter_data

    def compare_sample_lengths(self, random_sample, systematic_sample):
        """
        Compare the average chapter length between random sample and systematic sample.
        Returns a dictionary with comparison statistics.
        """
        random_avg_tokens = sum(chapter['token_count'] for chapter in random_sample) / len(random_sample)
        random_avg_words = sum(chapter['word_count'] for chapter in random_sample) / len(random_sample)
        random_avg_chars = sum(chapter['character_count'] for chapter in random_sample) / len(random_sample)
        random_avg_sentences = sum(chapter['sentence_count'] for chapter in random_sample) / len(random_sample)
        
        systematic_avg_tokens = sum(chapter['token_count'] for chapter in systematic_sample) / len(systematic_sample)
        systematic_avg_words = sum(chapter['word_count'] for chapter in systematic_sample) / len(systematic_sample)
        systematic_avg_chars = sum(chapter['character_count'] for chapter in systematic_sample) / len(systematic_sample)
        systematic_avg_sentences = sum(chapter['sentence_count'] for chapter in systematic_sample) / len(systematic_sample)
        
        return {
            'random_sample': {
                'count': len(random_sample),
                'avg_tokens': random_avg_tokens,
                'avg_words': random_avg_words,
                'avg_chars': random_avg_chars,
                'avg_sentences': random_avg_sentences
            },
            'systematic_sample': {
                'count': len(systematic_sample),
                'avg_tokens': systematic_avg_tokens,
                'avg_words': systematic_avg_words,
                'avg_chars': systematic_avg_chars,
                'avg_sentences': systematic_avg_sentences
            },
            'differences': {
                'token_diff': random_avg_tokens - systematic_avg_tokens,
                'word_diff': random_avg_words - systematic_avg_words,
                'char_diff': random_avg_chars - systematic_avg_chars,
                'sentence_diff': random_avg_sentences - systematic_avg_sentences
            }
        }