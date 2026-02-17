"""
OCR Module - Text extraction from PDFs and images
"""
import os
import sys
from pathlib import Path
from typing import Optional
import pytesseract
from PIL import Image
import pdfplumber
from pdf2image import convert_from_path

# Add parent directory to path for standalone execution
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import TESSERACT_PATH, TESSERACT_LANG


class OCRProcessor:
    """Class for text extraction from PDFs and images."""
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Initialize OCR processor.
        
        Args:
            tesseract_path: Path to Tesseract executable (optional)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        elif TESSERACT_PATH and os.path.exists(TESSERACT_PATH):
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        
        print("OCR Processor initialized")
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from file based on file type.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = file_path.suffix.lower()
        
        print(f"Starting text extraction: {file_path.name}")
        
        if extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self._extract_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def _extract_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from PDF (direct extraction first, then OCR fallback).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text = ""
        
        # Method 1: Direct text extraction with pdfplumber
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                print(f"Text extracted directly from PDF ({len(text)} characters)")
                return text.strip()
        except Exception as e:
            print(f"Warning: pdfplumber error: {e}")
        
        # Method 2: OCR extraction (for scanned PDFs)
        print("Processing PDF with OCR...")
        try:
            images = convert_from_path(pdf_path)
            for i, image in enumerate(images):
                print(f"Processing page {i+1}/{len(images)} with OCR...")
                page_text = pytesseract.image_to_string(
                    image, 
                    lang=TESSERACT_LANG
                )
                text += page_text + "\n"
            
            print(f"OCR completed ({len(text)} characters)")
            return text.strip()
        except Exception as e:
            print(f"Error: OCR error: {e}")
            raise
    
    def _extract_from_image(self, image_path: Path) -> str:
        """
        Extract text from image using OCR.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=TESSERACT_LANG)
            print(f"Text extracted from image ({len(text)} characters)")
            return text.strip()
        except Exception as e:
            print(f"Error: Image OCR error: {e}")
            raise


if __name__ == "__main__":
    # Test
    ocr = OCRProcessor()
    # ocr.extract_text("test.pdf")
