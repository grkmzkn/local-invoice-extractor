"""
Configuration settings for the invoice extractor
"""
import os
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:3b"  # Changeable: qwen2.5, gemma2, etc.

# OCR settings
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows path
TESSERACT_LANG = "tur+eng"  # Turkish + English

# Invoice extraction fields
INVOICE_FIELDS = {
    "invoice_number": "Invoice number",
    "date": "Invoice date",
    "company_name": "Issuing company name",
    "tax_number": "Tax identification number",
    "total_amount": "Total amount",
    "vat": "VAT amount",
    "items": "Product/service list (name, quantity, unit price)"
}