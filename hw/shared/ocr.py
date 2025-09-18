"""
PDF Processing Class using PyMuPDF

This class provides comprehensive PDF processing functionality using PyMuPDF exclusively.
PyMuPDF is fast, reliable, and preserves formatting while handling most PDF types effectively.

Approach: PyMuPDF only (fast, reliable, preserves formatting, handles most PDFs)
"""

import pymupdf
import re
from pathlib import Path
from collections import Counter
from typing import Dict, List, Optional, Tuple, Any


class OCR:
    """
    A streamlined PDF processing class using PyMuPDF exclusively.
    
    This class handles:
    - Direct PDF text extraction (PyMuPDF)
    - Text cleaning and structure preservation
    - Error detection and correction
    - Quality assessment and validation
    - Document structure analysis
    """
    
    def __init__(self):
        """
        Initialize the PDF processor.
        """
        pass
        
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[List[Dict[str, Any]]]:
        """
        Extract text from PDF using PyMuPDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing page data, or None if extraction fails
        """
        print(f"Opening PDF: {pdf_path}")
        
        try:
            doc = pymupdf.open(pdf_path)
            pages_data = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                page_data = {
                    'page': page_num + 1,
                    'text': text,
                    'char_count': len(text),
                    'word_count': len(text.split())
                }
                pages_data.append(page_data)
                
                print(f"   Page {page_num + 1}: {len(text)} characters, {len(text.split())} words")
            
            doc.close()
            print(f"✓ Successfully extracted {len(pages_data)} pages")
            return pages_data
            
        except FileNotFoundError:
            print(f"✗ Error: PDF file not found at path: {pdf_path}")
            return None
        except PermissionError:
            print(f"✗ Error: Permission denied when trying to read: {pdf_path}")
            return None
        except Exception as e:
            print(f"✗ Error reading PDF: {e}")
            return None
    
    def extract_with_layout(self, pdf_path: str, page_num: int = 0) -> Optional[List[Dict[str, Any]]]:
        """
        Extract text with detailed formatting information.
        
        Args:
            pdf_path: Path to the PDF file
            page_num: Page number to extract (0-indexed)
            
        Returns:
            List of formatted elements with metadata, or None if extraction fails
        """
        try:
            doc = pymupdf.open(pdf_path)
            page = doc.load_page(page_num)
            
            blocks = page.get_text("dict")
            formatted_elements = []
            
            for block in blocks["blocks"]:
                if "lines" in block:  # Skip image blocks
                    for line in block["lines"]:
                        for span in line["spans"]:
                            element = {
                                'text': span['text'],
                                'bbox': span['bbox'],
                                'font': span['font'],
                                'size': span['size'],
                                'flags': span['flags']
                            }
                            formatted_elements.append(element)
            
            doc.close()
            return formatted_elements
            
        except Exception as e:
            print(f"✗ Error extracting layout: {e}")
            return None
    
    def analyze_document_structure(self, elements: List[Dict[str, Any]]) -> None:
        """
        Analyze document structure based on formatting elements.
        
        Args:
            elements: List of formatted elements from extract_with_layout
        """
        if not elements:
            return
        
        # Group by font size to identify headers
        font_sizes = [elem['size'] for elem in elements]
        size_counts = Counter(font_sizes)
        
        print("📊 Font size distribution:")
        for size, count in sorted(size_counts.items(), reverse=True):
            print(f"   Size {size:.1f}: {count} elements")
        
        # Find likely headers (larger font sizes)
        avg_size = sum(font_sizes) / len(font_sizes)
        headers = [elem for elem in elements if elem['size'] > avg_size * 1.2]
        
        print(f"\n📋 Likely headers ({len(headers)} found):")
        for header in headers[:5]:  # Show first 5
            text_preview = header['text'][:50].replace('\n', ' ')
            print(f"   '{text_preview}' (size: {header['size']:.1f})")
        
        # Identify fonts used
        fonts = set(elem['font'] for elem in elements)
        print(f"\n🔤 Fonts detected: {len(fonts)}")
        for font in sorted(fonts)[:5]:  # Show first 5
            print(f"   {font}")
    
    def detect_document_type(self, text: str) -> str:
        """
        Detect document type based on content.
        
        Args:
            text: Document text to analyze
            
        Returns:
            Document type: 'academic', 'legal', or 'general'
        """
        if not text:
            return "unknown"
        
        text_lower = text.lower()
        
        # Academic document indicators
        academic_keywords = ['university', 'course', 'credit', 'prerequisite', 'professor', 'department']
        academic_score = sum(1 for keyword in academic_keywords if keyword in text_lower)
        
        # Legal document indicators
        legal_keywords = ['county', 'state of', 'notary', 'acknowledged', 'sworn', 'witness']
        legal_score = sum(1 for keyword in legal_keywords if keyword in text_lower)
        
        if academic_score > legal_score:
            return "academic"
        elif legal_score > academic_score:
            return "legal"
        else:
            return "general"
    
    def clean_academic_document(self, text: str) -> str:
        """
        Clean academic documents by removing headers, footers, and standardizing format.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        print("🧹 Applying academic document cleaning...")
        
        # Remove URLs
        text = re.sub(r'http[s]?://[^\s]+', '[URL]', text)
        
        # Standardize course codes (CMPE 5220. -> CMPE 5220:)
        text = re.sub(r'([A-Z]{2,4}\s+\d{4})\.\s*', r'\1: ', text)
        
        # Clean up credit formatting
        text = re.sub(r'(\d+)\s+Credits?\.\s*', r'\1 Credits. ', text)
        
        # Fix broken faculty names (often split across lines)
        text = re.sub(r'([A-Z][a-z]+),\s*([A-Z][a-z]+);\s*', r'\1, \2; ', text)
        
        # Remove excessive whitespace but preserve structure
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def clean_legal_document(self, text: str) -> str:
        """
        Clean legal documents by standardizing formatting.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        print("🧹 Applying legal document cleaning...")
        
        # Standardize legal formatting
        text = re.sub(r'STATE\s+OF\s+([A-Z]+)\s*\)', r'STATE OF \1)', text)
        text = re.sub(r'\)\s*\n\s*\)\s*ss:', r')\n) ss:', text)
        
        # Fix date formatting
        text = re.sub(r'(\d{1,2})\w*\s+day\s+of\s+([A-Z][a-z]+)\s*,?\s*(\d{4})',
                      r'\1 day of \2, \3', text)
        
        # Clean up signature formatting
        text = re.sub(r'\[Signature\]', '[SIGNATURE]', text)
        
        # Fix page references
        text = re.sub(r'Page\s+(\d+)\s+of\s+(\d+)', r'Page \1 of \2', text)
        
        return text.strip()
    
    def find_ocr_errors(self, text: str) -> Tuple[Dict[str, int], List[str], List[str], List[str]]:
        """
        Find common OCR errors in text.
        
        Args:
            text: Text to analyze for errors
            
        Returns:
            Tuple of (error_counts, char_errors, broken_words, suspicious_numbers)
        """
        errors = {}
        
        # Common OCR character confusions
        char_errors = []
        char_errors.extend(re.findall(r'\bl[A-Z]', text))  # l instead of I
        char_errors.extend(re.findall(r'\b0[A-Za-z]', text))  # 0 instead of O
        char_errors.extend(re.findall(r'rn([a-z])', text))  # rn instead of m
        errors['character_substitutions'] = len(char_errors)
        
        # Broken words (space in middle)
        broken_words = re.findall(r'\b[A-Za-z]{1,2}\s+[a-z]{2,}\b', text)
        errors['broken_words'] = len(broken_words)
        
        # Numbers in words where they shouldn't be
        number_in_words = re.findall(r'[A-Za-z]+\d+[A-Za-z]*|\d+[A-Za-z]+', text)
        # Filter out valid cases like "5220" or "2011"
        suspicious_numbers = [w for w in number_in_words if not w.isdigit()]
        errors['numbers_in_words'] = len(suspicious_numbers)
        
        return errors, char_errors, broken_words, suspicious_numbers
    
    def fix_ocr_errors(self, text: str) -> str:
        """
        Fix common OCR errors in text.
        
        Args:
            text: Text to fix
            
        Returns:
            Fixed text
        """
        print("🔧 Fixing OCR errors...")
        
        # Character substitution fixes
        fixes = [
            # Protect common abbreviations first
            (r'\bPHD\b', 'PhD'),
            (r'\bDSC\b', 'DSc'),
            
            # Fix l/I confusion (careful with word boundaries)
            (r'\bl([A-Z][a-z])', r'I\1'),
            
            # Fix 0/O confusion
            (r'\b0([A-Za-z])', r'O\1'),
            (r'([a-z])0\b', r'\1o'),
            
            # Fix rn/m confusion
            (r'rn([a-z])', r'm\1'),
            (r'([a-z])rn\b', r'\1m'),
            
            # Fix obvious broken words
            (r'\bU niversity\b', 'University'),
            (r'\bE ngineering\b', 'Engineering'),
            (r'\bD epartment\b', 'Department'),
        ]
        
        for pattern, replacement in fixes:
            before_count = len(re.findall(pattern, text))
            text = re.sub(pattern, replacement, text)
            if before_count > 0:
                print(f"   Fixed {before_count} instances of '{pattern}' pattern")
        
        return text
    
    def check_pdf_text_extractable(self, pdf_path: str) -> bool:
        """
        Check if PDF has extractable text.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            True if PDF has extractable text, False otherwise
        """
        try:
            doc = pymupdf.open(pdf_path)
            page = doc.load_page(0)  # Check first page
            text = page.get_text().strip()
            doc.close()
            
            if len(text) > 50:  # Arbitrary threshold
                print(f"✓ PDF has extractable text ({len(text)} characters)")
                print(f"   Preview: '{text[:100]}...'")
                return True
            else:
                print(f"✗ PDF has little/no extractable text ({len(text)} characters)")
                return False
                
        except Exception as e:
            print(f"✗ Error checking PDF: {e}")
            return False
    
    def analyze_extraction_quality(self, text: str, doc_name: str) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
        """
        Analyze quality of extracted text.
        
        Args:
            text: Extracted text to analyze
            doc_name: Name of document for reporting
            
        Returns:
            Tuple of (issues_dict, issues_with_content)
        """
        if not text:
            print(f"✗ No text to analyze for {doc_name}")
            return {}, {}
        
        issues = {}
        lines = text.split('\n')
        
        # Issue 1: Empty or very short lines
        empty_lines = [line for line in lines if len(line.strip()) == 0]
        short_lines = [line for line in lines if 0 < len(line.strip()) < 3]
        issues['empty_lines'] = len(empty_lines)
        issues['short_lines'] = len(short_lines)
        
        # Issue 2: Lines that are all uppercase (likely headers)
        uppercase_lines = [line for line in lines if line.isupper() and len(line.strip()) > 3]
        issues['uppercase_lines'] = len(uppercase_lines)
        
        # Issue 3: Lines with mostly numbers
        number_heavy_lines = [line for line in lines if
                             len(re.findall(r'\d', line)) / max(len(line), 1) > 0.3
                             and len(line.strip()) > 2]
        issues['number_heavy_lines'] = len(number_heavy_lines)
        
        # Issue 4: Potential OCR errors
        mixed_chars = re.findall(r'\w*\d[A-Za-z]\w*|\w*[A-Za-z]\d\w*', text)
        issues['mixed_chars'] = len(set(mixed_chars))
        
        # Issue 5: Very long lines
        long_lines = [line for line in lines if len(line) > 200]
        issues['very_long_lines'] = len(long_lines)
        
        print(f"\n📊 {doc_name} Extraction Analysis:")
        for issue, count in issues.items():
            print(f"   • {issue.replace('_', ' ').title()}: {count}")
        
        # Store actual problematic content
        issues_with_content = {
            'empty_lines': empty_lines,
            'short_lines': short_lines,
            'uppercase_lines': uppercase_lines,
            'number_heavy_lines': number_heavy_lines,
            'mixed_chars': mixed_chars,
            'long_lines': long_lines
        }
        
        return issues, issues_with_content
    
    def compare_versions(self, original: str, cleaned: str, fixed: str, doc_name: str) -> Dict[str, Any]:
        """
        Compare different versions of processed text.
        
        Args:
            original: Original text
            cleaned: Cleaned text
            fixed: OCR-fixed text
            doc_name: Document name for reporting
            
        Returns:
            Dictionary with comparison statistics
        """
        print(f"\n📈 {doc_name} Processing Results:")
        print(f"   Original length: {len(original)} characters")
        print(f"   After cleaning:  {len(cleaned)} characters ({len(cleaned)-len(original):+d})")
        print(f"   After OCR fixes: {len(fixed)} characters ({len(fixed)-len(cleaned):+d})")
        
        # Count remaining potential issues
        remaining_errors, _, _, _ = self.find_ocr_errors(fixed)
        total_remaining = sum(remaining_errors.values())
        print(f"   Remaining potential errors: {total_remaining}")
        
        return {
            'original_len': len(original),
            'cleaned_len': len(cleaned),
            'fixed_len': len(fixed),
            'remaining_errors': total_remaining
        }
    
    def process_pdf_complete(self, pdf_path: str, output_dir: str = "processed_pdfs") -> Dict[str, Any]:
        """
        Complete PDF processing pipeline using PyMuPDF exclusively.
        
        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save processed files
            
        Returns:
            Dictionary with processing results
        """
        print(f"🚀 Starting PDF processing for: {pdf_path}")
        print("📋 Using PyMuPDF for text extraction and processing")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = {}
        
        # Step 1: Extract text using PyMuPDF
        print("\n🔍 Step 1: Extracting text with PyMuPDF...")
        pages_data = self.extract_text_from_pdf(pdf_path)
        
        if pages_data and any(page['text'].strip() for page in pages_data):
            # PyMuPDF extraction successful
            print("✅ PyMuPDF extraction successful!")
            
            full_text = "\n".join([page['text'] for page in pages_data])
            
            # Analyze document structure
            print("\n📊 Step 2: Analyzing document structure...")
            layout_elements = self.extract_with_layout(pdf_path, 0)
            if layout_elements:
                self.analyze_document_structure(layout_elements)
            
            # Detect document type and clean
            print("\n🧹 Step 3: Cleaning and processing text...")
            doc_type = self.detect_document_type(full_text)
            print(f"📄 Document detected as: {doc_type}")
            
            if doc_type == "academic":
                cleaned_text = self.clean_academic_document(full_text)
            elif doc_type == "legal":
                cleaned_text = self.clean_legal_document(full_text)
            else:
                cleaned_text = full_text
            
            # Find and fix potential errors
            print("\n🔧 Step 4: Error detection and correction...")
            errors, _, _, _ = self.find_ocr_errors(cleaned_text)
            print("🔍 Potential issues found:")
            for error_type, count in errors.items():
                print(f"   • {error_type.replace('_', ' ').title()}: {count}")
            
            fixed_text = self.fix_ocr_errors(cleaned_text)
            
            # Compare versions
            print("\n📈 Step 5: Quality assessment...")
            comparison = self.compare_versions(full_text, cleaned_text, fixed_text, "PDF Document")
            
            # Save processed text
            output_file = output_path / f"{Path(pdf_path).stem}_processed.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(fixed_text)
            print(f"💾 Saved: {output_file}")
            
            results = {
                'method': 'pymupdf_extraction',
                'original_text': full_text,
                'cleaned_text': cleaned_text,
                'fixed_text': fixed_text,
                'comparison': comparison,
                'output_file': str(output_file),
                'pages_processed': len(pages_data)
            }
            
        else:
            # PyMuPDF extraction failed or returned empty text
            print("❌ PyMuPDF extraction failed or returned empty text")
            print("💡 This might be a scanned PDF or image-based document.")
            print("   Consider using a different PDF or checking if the file is corrupted.")
            
            results = {
                'method': 'failed', 
                'error': 'PyMuPDF extraction failed - possibly a scanned/image-based PDF'
            }
        
        print("\n✅ PDF processing complete!")
        return results
