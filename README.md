# Natural Language Processing Project

This project contains NLP methods and utilities for text processing, including quote extraction, chapter analysis, and sampling techniques.

## Setup

### Prerequisites
- Python 3.7 or higher
- Internet connection (for downloading NLTK data and Project Gutenberg texts)

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

#### Using OCR for PDF Processing

```python
import sys
sys.path.append('../shared')

from ocr import OCR

# Create OCR instance
ocr = OCR()

# Process a PDF file completely
results = ocr.process_pdf_complete("path/to/your/document.pdf")

# Or use individual methods for more control
pages_data = ocr.extract_text_from_pdf("path/to/your/document.pdf")
if pages_data:
    full_text = "\n".join([page['text'] for page in pages_data])
    
    # Detect document type and clean accordingly
    doc_type = ocr.detect_document_type(full_text)
    if doc_type == "academic":
        cleaned_text = ocr.clean_academic_document(full_text)
    elif doc_type == "legal":
        cleaned_text = ocr.clean_legal_document(full_text)
    else:
        cleaned_text = full_text
    
    # Fix OCR errors
    fixed_text = ocr.fix_ocr_errors(cleaned_text)
    
    # Analyze extraction quality
    issues, issues_content = ocr.analyze_extraction_quality(fixed_text, "Document")
```

#### Combined Usage Example

```python
import sys
sys.path.append('../shared')

from nlp_methods import NLPMethods
from ocr import OCR

# Process a PDF first
ocr = OCR()
pdf_results = ocr.process_pdf_complete("academic_paper.pdf")

if pdf_results['method'] != 'failed':
    # Then analyze the extracted text with NLP methods
    nlp_methods = NLPMethods("dummy_url")  # URL not needed for text analysis
    
    # Analyze the processed text
    corpus_data = nlp_methods.get_processed_text(pdf_results['fixed_text'])
    
    # Extract quotes and analyze dialogue
    quotes = nlp_methods.extract_quotes(pdf_results['fixed_text'])
    longest_dialogue = nlp_methods.get_longest_dialogue(pdf_results['fixed_text'])
    
    print(f"Found {len(quotes)} quotes in the document")
    print(f"Longest dialogue has {longest_dialogue['quote_count']} quotes")
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

### OCR Class

The `OCR` class provides comprehensive PDF processing functionality using PyMuPDF for text extraction, cleaning, and analysis.

#### Initialization
```python
ocr = OCR()
```

#### PDF Text Extraction Methods

- **`extract_text_from_pdf(pdf_path)`**: Extract text from PDF using PyMuPDF. Returns list of page data dictionaries
- **`extract_with_layout(pdf_path, page_num=0)`**: Extract text with detailed formatting information including font, size, and positioning data
- **`check_pdf_text_extractable(pdf_path)`**: Check if PDF has extractable text (vs. scanned/image-based)

#### Document Analysis Methods

- **`analyze_document_structure(elements)`**: Analyze document structure based on formatting elements (headers, font sizes, etc.)
- **`detect_document_type(text)`**: Detect document type (academic, legal, or general) based on content analysis
- **`analyze_extraction_quality(text, doc_name)`**: Analyze quality of extracted text and identify potential issues

#### Text Cleaning Methods

- **`clean_academic_document(text)`**: Clean academic documents by removing headers, footers, and standardizing format
- **`clean_legal_document(text)`**: Clean legal documents by standardizing formatting and structure
- **`fix_ocr_errors(text)`**: Fix common OCR errors like character substitutions and broken words

#### Error Detection and Correction

- **`find_ocr_errors(text)`**: Find common OCR errors including character substitutions, broken words, and suspicious patterns
- **`compare_versions(original, cleaned, fixed, doc_name)`**: Compare different versions of processed text with statistics

#### Complete Processing Pipeline

- **`process_pdf_complete(pdf_path, output_dir="processed_pdfs")`**: Complete PDF processing pipeline that extracts, cleans, fixes errors, and saves processed text

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
