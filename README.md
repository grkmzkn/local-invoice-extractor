# Local Invoice Extractor 🧾

Faturalardan bilgi çıkarımı için **tamamen yerel** çalışan, gizlilik odaklı Python uygulaması. Ollama ile yerel LLM kullanarak fatura verileriniz hiçbir zaman dışarıya çıkmaz.

## ✨ Özellikler

- 🔒 **%100 Yerel**: Tüm işlemler bilgisayarınızda yapılır
- 📄 **PDF & Görüntü Desteği**: PDF, PNG, JPG, TIFF formatları
- 🤖 **Yerel LLM**: Ollama ile güçlü AI analizi
- 🇹🇷 **Türkçe Desteği**: OCR ve LLM için tam Türkçe desteği
- 📊 **Yapılandırılmış Çıktı**: JSON formatında düzenli veri
- 🔄 **Toplu İşlem**: Birden fazla faturayı tek seferde işleme

## 📋 Ön Gereksinimler

### 1. Python 3.8+
```bash
python --version
```

### 2. Tesseract OCR
**Windows için:**
- [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki) adresinden indirin
- Kurulum sırasında "Additional language data" bölümünden **Turkish** seçin
- Varsayılan yol: `C:\Program Files\Tesseract-OCR\tesseract.exe`

**Linux için:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-tur
```

### 3. Ollama
**Windows için:**
- [Ollama.ai](https://ollama.ai) adresinden indirin ve kurun
- Terminal'de şu komutu çalıştırın:
```bash
ollama pull llama3.2:3b
```

Daha iyi performans için alternatif modeller:
```bash
ollama pull qwen2.5:3b    # Türkçe için önerilir
ollama pull gemma2:2b     # Daha hızlı
```

## 🚀 Kurulum

### 1. Projeyi klonlayın
```bash
cd c:\Users\gorkemozkan\Desktop\gorkDrive\local-invoice-extractor
```

### 2. Virtual environment oluşturun (opsiyonel ama önerilir)
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. Konfigürasyonu ayarlayın
[src/config.py](src/config.py) dosyasını açın ve gerekirse düzenleyin:
- `TESSERACT_PATH`: Tesseract kurulum yolu
- `OLLAMA_MODEL`: Kullanmak istediğiniz model
- `INVOICE_FIELDS`: Çıkarılacak fatura alanları

## 📖 Kullanım

### Tek Fatura İşleme
```bash
python main.py data/fatura.pdf
```

### Toplu İşlem (Klasördeki tüm faturalar)
```bash
python main.py --batch data/
```

### Detaylı Loglama
```bash
python main.py -v data/fatura.pdf
```

### Sonucu kaydetmeden görüntüleme
```bash
python main.py --no-save data/fatura.pdf
```

## 📁 Proje Yapısı

```
local-invoice-extractor/
├── src/
│   ├── __init__.py
│   ├── config.py              # Ayarlar
│   ├── ocr_module.py          # PDF/Görüntü → Metin
│   ├── llm_module.py          # Ollama LLM işlemleri
│   └── invoice_processor.py   # Ana işlem pipeline
├── data/                       # Fatura dosyalarınız (PDF/görüntü)
├── output/                     # Çıktı JSON dosyaları
├── env/                        # Virtual environment
├── main.py                     # Ana çalıştırıcı
├── requirements.txt
└── README.md
```

## 🔍 Çıkarılan Bilgiler

Varsayılan olarak şu bilgiler çıkarılır:
- Fatura numarası
- Fatura tarihi
- Firma adı
- Vergi numarası
- Toplam tutar
- KDV tutarı
- Ürün/hizmet listesi (ad, miktar, birim fiyat)

[src/config.py](src/config.py) dosyasından `INVOICE_FIELDS` değişkenini düzenleyerek özelleştirebilirsiniz.

## 📊 Örnek Çıktı

```json
{
  "fatura_no": "FTR-2024-12345",
  "tarih": "2024-01-15",
  "firma_adi": "ABC Teknoloji A.Ş.",
  "vergi_no": "9876543210",
  "toplam_tutar": 36875.00,
  "kdv": 5625.00,
  "urunler": [
    {"ad": "Laptop", "miktar": 2, "birim_fiyat": 15000.00},
    {"ad": "Mouse", "miktar": 5, "birim_fiyat": 250.00}
  ]
}
```

## 🛠️ Geliştirme

### Modüler Yapı
Her modül bağımsız çalışabilir:

```python
# OCR modülünü test et
from src.ocr_module import OCRProcessor
ocr = OCRProcessor()
text = ocr.extract_text("fatura.pdf")

# LLM modülünü test et
from src.llm_module import LLMProcessor
llm = LLMProcessor()
result = llm.extract_invoice_data(text)
```

### Yeni Model Ekleme
```python
# src/config.py
OLLAMA_MODEL = "qwen2.5:7b"  # Daha güçlü model
```

### Yeni Alan Ekleme
```python
# src/config.py
INVOICE_FIELDS = {
    "fatura_no": "Fatura numarası",
    "iban": "IBAN numarası",  # Yeni alan
    # ... diğer alanlar
}
```

## 🐛 Sorun Giderme

### "Ollama bağlantı hatası"
```bash
# Ollama'yı başlatın
ollama serve
```

### "Model bulunamadı"
```bash
# Modeli indirin
ollama pull llama3.2:3b
```

### "Tesseract bulunamadı"
- [src/config.py](src/config.py) dosyasında `TESSERACT_PATH` yolunu kontrol edin
- Tesseract'ın doğru kurulu olduğundan emin olun

### "OCR sonucu boş"
- Görüntü kalitesini kontrol edin
- Türkçe dil paketi kurulu mu: `tesseract --list-langs`

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'e push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu proje tamamen yerel çalışır. Hiçbir veri internete gönderilmez! 🔒
