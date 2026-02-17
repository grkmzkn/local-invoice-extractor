"""
Invoice Processing Module - Main pipeline combining OCR and LLM
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Add parent directory to path for standalone execution
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ocr_module import OCRProcessor
from src.llm_module import LLMProcessor
from src.config import OUTPUT_DIR


class InvoiceProcessor:
    """Invoice processing pipeline."""
    
    def __init__(self, 
                 ocr_processor: OCRProcessor = None,
                 llm_processor: LLMProcessor = None):
        """
        Initialize invoice processor.
        
        Args:
            ocr_processor: OCR processor instance (optional)
            llm_processor: LLM processor instance (optional)
        """
        self.ocr = ocr_processor or OCRProcessor()
        self.llm = llm_processor or LLMProcessor()
        
        print("Invoice Processor ready")
    
    def process_invoice(self, file_path: str, save_output: bool = True) -> Dict[str, Any]:
        """
        Process invoice and extract information.
        
        Args:
            file_path: Path to invoice file (PDF or image)
            save_output: Whether to save output as JSON
            
        Returns:
            Extracted invoice information
        """
        file_path = Path(file_path)
        print(f"Processing invoice: {file_path.name}")
        
        try:
            # Step 1: Text extraction with OCR
            print("Step 1/3: Text extraction...")
            invoice_text = self.ocr.extract_text(file_path)
            
            if not invoice_text or len(invoice_text) < 50:
                raise ValueError("Insufficient text extracted")
            
            # Step 2: Structured data extraction with LLM
            print("Step 2/3: LLM analysis...")
            extracted_data = self.llm.extract_invoice_data(invoice_text)
            
            # Step 3: Prepare results
            print("Step 3/3: Preparing results...")
            result = {
                "source_file": str(file_path),
                "processed_at": datetime.now().isoformat(),
                "raw_text": invoice_text,
                "extracted_data": extracted_data,
                "validation": {
                    "is_valid": self.llm.validate_extraction(extracted_data),
                    "text_length": len(invoice_text)
                }
            }
            
            # Save output
            if save_output:
                self._save_result(file_path.stem, result)
            
            print(f"✓ Invoice processed successfully: {file_path.name}")
            return result
            
        except Exception as e:
            print(f"Error: Invoice processing error: {e}")
            raise
    
    def _save_result(self, filename: str, result: Dict[str, Any]):
        """
        Save result as JSON.
        
        Args:
            filename: Filename (without extension)
            result: Result dictionary
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"{filename}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"Result saved: {output_file}")
    
    def process_batch(self, folder_path: str) -> list:
        """
        Process all invoices in a folder.
        
        Args:
            folder_path: Folder path
            
        Returns:
            List of all results
        """
        folder = Path(folder_path)
        results = []
        
        # Find supported files
        supported_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        files = [f for f in folder.iterdir() 
                if f.suffix.lower() in supported_extensions]
        
        print(f"{len(files)} invoices found")
        
        for i, file in enumerate(files, 1):
            print(f"[{i}/{len(files)}] Processing...")
            try:
                result = self.process_invoice(file)
                results.append(result)
            except Exception as e:
                print(f"Error: {file.name} - {e}")
                results.append({
                    "source_file": str(file),
                    "error": str(e)
                })
        
        return results


if __name__ == "__main__":
    # Test
    processor = InvoiceProcessor()
    # processor.process_invoice("data/test_invoice.pdf")
