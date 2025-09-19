# Natural Language Processing Project

This project contains NLP methods and utilities for text processing, including quote extraction, chapter analysis, and sampling techniques.

## Setup

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start

1. Navigate to any notebook (e.g., `hw/week_4/hw3.ipynb`)
2. Run the cells - the `NLPMethods` class will automatically download required NLTK data on first use

## Project Structure

```
NaturalLanguageProcessing/
├── hw/
│   ├── shared/
│   │   ├── nlp_methods.py         # Main NLP methods class
│   │   └── ocr.py                 # PDF processing and OCR class
│   ├── week_2/                    # Homework assignments
│   ├── week_3/
│   └── week_4/
├── journal/                       # Research notes
├── sample_notebooks/              # Example notebooks
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Usage

### Basic Usage in Jupyter Notebook

#### Using NLPMethods for Text Analysis

```python
import sys
import importlib

# Add the shared folder to path
sys.path.append('../shared')

from nlp_methods import NLPMethods

# Create an instance with a URL (automatically downloads NLTK data)
nlp_methods = NLPMethods("https://www.gutenberg.org/cache/epub/2500/pg2500.txt")

# Extract and process text
clean_text = nlp_methods.remove_gutenberg_header()
corpus_data = nlp_methods.get_processed_text(clean_text)

# Analyze chapters
chapters = nlp_methods.get_chapters(clean_text)
chapter_data = nlp_methods.get_chapter_data(chapters, clean_text)

# Perform sampling analysis
random_sample = nlp_methods.get_random_sample_chapter_data(chapters, clean_text)
systematic_sample = nlp_methods.get_systematic_sample_chapter_data(chapters, clean_text)
comparison = nlp_methods.compare_sample_lengths(random_sample, systematic_sample)
```
## Available Classes and Methods

### NLPMethods Class

The `NLPMethods` class provides comprehensive text processing capabilities for natural language analysis.

#### Initialization
```python
nlp_methods = NLPMethods(url)
```
- `url`: URL to a Project Gutenberg text file

#### Core Text Processing Methods

- **`remove_gutenberg_header()`**: Extract clean text from the URL provided during initialization, removing Gutenberg headers and footers
- **`get_processed_text(text)`**: Process text and extract sentences, tokens, quotes, and non-quotes. Returns a dictionary with comprehensive text analysis data
- **`extract_quotes(text)`**: Extract all quoted text from content using multiple quote patterns (straight quotes, Unicode quotes)
- **`remove_quotes(text)`**: Remove all quoted text from content, leaving only narrative/non-dialogue text

#### Chapter Analysis Methods

- **`get_chapters(text, shuffle=False)`**: Find chapter titles in text using regex patterns. Returns list of chapter titles
- **`get_chapter_data(chapters, text)`**: Extract detailed chapter statistics including word count, token count, sentence count, and character count
- **`chapters_to_dataframe(chapters_data)`**: Convert chapters data to a pandas DataFrame for analysis

#### Sampling Methods

- **`get_random_sample_chapter_data(chapters, text, sample_size=10)`**: Implement random sampling to extract random chapters from the corpus
- **`get_systematic_sample_chapter_data(chapters, text, step_size=None)`**: Implement systematic sampling to extract every nth chapter
- **`compare_sample_lengths(random_sample, systematic_sample)`**: Compare average chapter length between random and systematic samples

#### Advanced Analysis Methods

- **`get_longest_dialogue(text, distance_threshold=500)`**: Find the longest dialogue exchange (consecutive quotes) in the text with comprehensive metrics

## Dependencies

- **nltk**: Natural Language Toolkit for tokenization and text processing
- **pandas**: Data manipulation and analysis
- **pymupdf**: Fast PDF processing library for text extraction and document analysis

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're running the notebook from the correct directory and the `shared` folder is in your Python path
2. **NLTK Download Issues**: The class automatically downloads required NLTK data, but you need internet access
3. **Path Issues**: If relative imports fail, use absolute paths or ensure you're in the right directory

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `pip list`
2. Verify your Python path includes the `shared` directory
3. Ensure you have internet access for NLTK downloads
