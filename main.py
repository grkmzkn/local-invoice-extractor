"""
Local Invoice Extractor - Main Entry Point
System using local LLM for invoice information extraction
"""
import json
from pathlib import Path

from src.invoice_processor import InvoiceProcessor
from src.config import OUTPUT_DIR


# ========================================
# CONFIGURATION - Edit this section
# ========================================

# Set your invoice file or folder path here
INVOICE_PATH = "data/"

# ========================================


def main():
    """Main function."""
    print("="*60)
    print("🧾 Local Invoice Extractor v0.1.0")
    print("="*60)
    
    # Check if path exists
    target_path = Path(INVOICE_PATH)
    if not target_path.exists():
        print(f"\n❌ Error: '{INVOICE_PATH}' not found")
        print("Please update INVOICE_PATH in main.py")
        return 1
    
    # Create processor
    print("\nInitializing...")
    try:
        processor = InvoiceProcessor()
    except Exception as e:
        print(f"\n❌ Error: Could not initialize processor")
        print(f"Details: {e}")
        print("\n💡 Make sure:")
        print("  1. Ollama is running: 'ollama serve'")
        print("  2. Model is installed: 'ollama pull llama3.2:3b'")
        return 1
    
    # Process
    try:
        # Batch processing (folder)
        if target_path.is_dir():
            print(f"\n📁 Processing folder: {INVOICE_PATH}\n")
            results = processor.process_batch(INVOICE_PATH)
            
            success_count = sum(1 for r in results if 'error' not in r)
            print(f"\n{'='*60}")
            print(f"✓ Completed: {success_count}/{len(results)} successful")
            
        # Single file processing
        elif target_path.is_file():
            print(f"\n📄 Processing file: {target_path.name}\n")
            result = processor.process_invoice(INVOICE_PATH)
            
            # Show extracted data
            print(f"\n{'='*60}")
            print("📊 EXTRACTED INFORMATION:")
            print(f"{'='*60}")
            
            extracted = result.get('extracted_data', {})
            print(json.dumps(extracted, indent=2, ensure_ascii=False))
        
        else:
            print(f"❌ Error: '{INVOICE_PATH}' is neither a file nor a folder")
            return 1
        
        print(f"\n✓ Done! Results saved to: {OUTPUT_DIR}\n")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    main()
