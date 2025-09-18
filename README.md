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
│   │   └── NLPMethods.py          # Main NLP methods class
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

```python
import sys
import importlib

# Add the shared folder to path
sys.path.append('../shared')

from NLPMethods import NLPMethods

# Create an instance with a URL (automatically downloads NLTK data)
nlp_methods = NLPMethods("https://www.gutenberg.org/cache/epub/2500/pg2500.txt")

# Use the methods
clean_text = nlp_methods.remove_gutenberg_header()
corpus_data = nlp_methods.get_processed_text(clean_text)
```

## Available Methods

- `remove_gutenberg_header()`: Extract clean text from the URL provided during initialization
- `get_processed_text(text)`: Process text and extract sentences, tokens, quotes
- `extract_quotes(text)`: Extract quoted text from content
- `remove_quotes(text)`: Remove quotes, leaving narrative text
- `get_chapters(text)`: Find chapter titles in text
- `get_chapter_data(chapters, text)`: Extract detailed chapter statistics
- `get_random_sample_chapter_data()`: Random sampling of chapters
- `get_systematic_sample_chapter_data()`: Systematic sampling of chapters

## Dependencies

- **nltk**: Natural Language Toolkit for tokenization
- **pandas**: Data manipulation and analysis
- **flake8**: Python code linting and style checking

## Code Quality

### Linting with Flake8

This project uses flake8 for code quality and style checking. Flake8 is configured in `.flake8` with sensible defaults.

**Basic usage:**
```bash
# Check all Python files in your project
flake8 .

# Check a specific file
flake8 hw/shared/NLPMethods.py

# Check with more verbose output
flake8 --show-source hw/shared/NLPMethods.py

# Check and show statistics
flake8 --statistics .
```

**Common flake8 error codes:**
- **E501**: Line too long (over 88 characters)
- **E302**: Expected 2 blank lines before class/function definition
- **W293**: Blank line contains whitespace
- **W291**: Trailing whitespace
- **W292**: No newline at end of file

**Configuration:**
The `.flake8` file configures:
- Max line length: 88 characters
- Excludes common directories (`.git`, `__pycache__`, etc.)
- Ignores certain style rules for better compatibility

### Additional Code Quality Tools

Consider these complementary tools:
- **black**: Auto-formats your code (complements flake8)
- **isort**: Sorts and organizes imports
- **pylint**: More comprehensive but also more opinionated

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
