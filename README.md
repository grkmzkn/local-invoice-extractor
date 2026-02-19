# Local Invoice Extractor 🧾

A **completely local** privacy-focused Python application for extracting information from invoices. Using local LLM with Ollama ensures your invoice data never leaves your computer.

## ✨ Features

- 🔒 **100% Local**: All processing happens on your computer
- 📄 **PDF & Image Support**: PDF, PNG, JPG, JPEG, TIFF, BMP formats
- 🤖 **Local LLM**: Powerful AI analysis with Ollama
- 🌍 **Multi-language Support**: OCR and LLM support for Turkish and English
- 📊 **Structured Output**: Organized data in JSON format
- 🔄 **Batch Processing**: Process multiple invoices at once

## 📋 Prerequisites

### 1. Python 3.8+
```bash
python --version
```

### 2. Tesseract OCR
**For Windows:**
- Download from [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
- During installation, select **Turkish** (and other languages) from "Additional language data"
- Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

### 3. Ollama
**For Windows:**
- Download and install from [Ollama.ai](https://ollama.ai)
- Run the following command in terminal:
```bash
ollama pull qwen2.5:3b
```

Alternative models for better performance:
```bash
ollama pull llama3.2:3b    # Good general purpose
ollama pull gemma2:2b      # Faster processing
```

## 🚀 Installation

### 1. Navigate to the project directory
```bash
cd local-invoice-extractor
```

### 2. Create a virtual environment (optional but recommended)
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure settings
Open [src/config.py](src/config.py) and edit if necessary:
- `TESSERACT_PATH`: Path to Tesseract installation
- `OLLAMA_MODEL`: Model you want to use
- `INVOICE_FIELDS`: Fields to extract from invoices

## 📁 Project Structure

```
local-invoice-extractor/
├── src/
│   ├── config.py              # Configuration settings
│   ├── ocr_module.py          # PDF/Image → Text extraction
│   ├── llm_module.py          # Ollama LLM operations
│   └── invoice_processor.py   # Main processing pipeline
├── data/                       # Your invoice files (PDF/images)
├── output/                     # Output JSON files
├── env/                        # Virtual environment
├── main.py                     # Main entry point
├── requirements.txt            # Project dependencies
└── README.md
```

## 🔍 Extracted Information

By default, the following information is extracted:
- Invoice number
- Invoice date
- Company name
- Tax identification number
- Total amount
- VAT/Tax amount
- Product/service list (name, quantity, unit price)

You can customize the fields by editing the `INVOICE_FIELDS` variable in [src/config.py](src/config.py).

## 📊 Sample Output

```json
{
  "source_file": "data\\example_invoice.png",
  "processed_at": "2026-02-17T22:58:30.002076",
  "extracted_data": {
    "invoice_number": "0000007",
    "date": "2023-10-02",
    "company_name": "Your Company Inc.",
    "tax_number": null,
    "total_amount": 262.50,
    "vat": 12.50,
    "items": [
      {
        "name": "Replacement of spark plugs",
        "quantity": 1,
        "unit_price": 40.00
      },
      {
        "name": "Brake pad replacement (front)",
        "quantity": 2,
        "unit_price": 40.00
      }
    ]
  },
  "validation": {
    "is_valid": true,
    "text_length": 550
  }
}
```

## 🛠️ Development

### Adding a New Model
```python
# src/config.py
OLLAMA_MODEL = "qwen2.5:7b"  # More powerful model
```

### Adding Custom Fields
```python
# src/config.py
INVOICE_FIELDS = {
    "invoice_number": "Invoice number",
    "iban": "IBAN number",  # New field
    # ... other fields
}
```

## 🐛 Troubleshooting

### "Ollama connection error"
```bash
# Start Ollama service
ollama serve
```

### "Model not found"
```bash
# Download the model
ollama pull qwen2.5:3b
```

### "Tesseract not found"
- Check the `TESSERACT_PATH` in [src/config.py](src/config.py)
- Ensure Tesseract is correctly installed

### "Empty OCR result"
- Check image quality
- Verify language pack is installed: `tesseract --list-langs`
- Make sure Turkish and English are listed

### "Insufficient text extracted"
- Ensure the invoice file is readable
- Try improving image quality/resolution
- Check if the file is not corrupted

## 💡 Tips

- **Better accuracy**: Use higher quality PDF or image files
- **Faster processing**: Use smaller models like `gemma2:2b`
- **Better Turkish support**: Use `qwen2.5:3b` model
- **Custom fields**: Edit `INVOICE_FIELDS` in config to extract specific information

## 📝 License

This project is licensed under the MIT License.

---

**Note**: This project runs completely offline. No data is sent to the internet! 🔒