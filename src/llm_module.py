"""
LLM Module - Local LLM operations using Ollama
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import ollama

# Add parent directory to path for standalone execution
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL, INVOICE_FIELDS


class LLMProcessor:
    """Class for analyzing invoice texts using Ollama."""
    
    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = OLLAMA_BASE_URL):
        """
        Initialize LLM processor.
        
        Args:
            model: Ollama model name to use
            base_url: Ollama server address
        """
        self.model = model
        self.base_url = base_url
        
        try:
            self.client = ollama.Client(host=base_url)
            print(f"LLM Processor initialized - Model: {model}")
        except Exception as e:
            print(f"Error: Could not connect to Ollama at {base_url}")
            print(f"Details: {e}")
            print("Make sure Ollama is running: 'ollama serve'")
            raise
    
    def extract_invoice_data(self, invoice_text: str) -> Dict[str, Any]:
        """
        Extract structured data from invoice text.
        
        Args:
            invoice_text: Invoice text extracted by OCR
            
        Returns:
            Extracted invoice information (dict)
        """
        print("Starting invoice analysis with LLM...")
        
        prompt = self._create_extraction_prompt(invoice_text)
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False
            )
            
            # Parse response
            result = self._parse_response(response['response'])
            print("Invoice analysis completed")
            return result
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if "model" in error_msg and "not found" in error_msg:
                print(f"Error: Model '{self.model}' not found")
                print(f"Install it with: ollama pull {self.model}")
            elif "connection" in error_msg or "connect" in error_msg:
                print(f"Error: Cannot connect to Ollama")
                print("Make sure Ollama is running: 'ollama serve'")
            else:
                print(f"Error: {e}")
                
            raise
    
    def _create_extraction_prompt(self, invoice_text: str) -> str:
        """
        Create prompt for invoice information extraction.
        
        Args:
            invoice_text: Invoice text
            
        Returns:
            Prepared prompt
        """
        fields_description = "\n".join([
            f"- {key}: {desc}" 
            for key, desc in INVOICE_FIELDS.items()
        ])
        
        prompt = f"""You are an invoice analysis assistant. Extract the specified information from the following invoice text and return it in JSON format.

INVOICE TEXT:
{invoice_text}

INFORMATION TO EXTRACT:
{fields_description}

RULES:
1. Respond only in JSON format, no other explanations
2. If information is not found, use null as the value
3. Provide dates in "YYYY-MM-DD" format
4. Provide amounts as numeric values (without currency symbols)
5. Provide product list as an array

EXAMPLE OUTPUT FORMAT:
{{
    "invoice_number": "INV-2024-001",
    "date": "2024-01-15",
    "company_name": "Example Company Inc.",
    "tax_number": "1234567890",
    "total_amount": 1500.00,
    "vat": 270.00,
    "items": [
        {{"name": "Product 1", "quantity": 2, "unit_price": 500.00}},
        {{"name": "Product 2", "quantity": 1, "unit_price": 230.00}}
    ]
}}

Now analyze the invoice text above and provide the JSON output:"""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse LLM response.
        
        Args:
            response_text: Response from LLM
            
        Returns:
            Parsed dictionary
        """
        try:
            # Find JSON block
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                print("Warning: JSON not found, returning raw response")
                return {"raw_response": response_text}
            
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            print(f"Error: JSON parse error: {e}")
            return {"error": "JSON parse error", "raw_response": response_text}
    
    def validate_extraction(self, extracted_data: Dict[str, Any]) -> bool:
        """
        Validate the extracted data.
        
        Args:
            extracted_data: Extracted data
            
        Returns:
            True if valid
        """
        required_fields = ["invoice_number", "date", "company_name", "total_amount"]
        
        for field in required_fields:
            if field not in extracted_data or extracted_data[field] is None:
                print(f"Warning: Missing required field: {field}")
                return False
        
        return True


if __name__ == "__main__":
    # Test
    llm = LLMProcessor()
    test_text = """
    FATURA
    No: FTR-2024-12345
    Tarih: 15.01.2024
    ABC Teknoloji A.Ş.
    Vergi No: 9876543210
    
    Ürün        Miktar  Birim Fiyat
    Laptop      2       15000.00
    Mouse       5       250.00
    
    Ara Toplam: 31250.00
    KDV (%18):  5625.00
    TOPLAM:     36875.00
    """
    # result = llm.extract_invoice_data(test_text)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
