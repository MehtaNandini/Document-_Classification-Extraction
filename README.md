# Document Classification & Extraction (NLP/OCR)

This project provides a Python pipeline for document extraction and classification. It uses Optical Character Recognition (OCR) via Tesseract to extract text from documents (PDFs and images) and Natural Language Processing (NLP) with Hugging Face Transformers to classify the extracted text into predefined categories using zero-shot classification.

## Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR:** 
   - **macOS:** `brew install tesseract`
   - **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
   - **Windows:** Download the installer from the [official repository](https://github.com/UB-Mannheim/tesseract/wiki)
3. **Poppler (for PDF support):**
   - **macOS:** `brew install poppler`
   - **Ubuntu/Debian:** `sudo apt-get install poppler-utils`
   - **Windows:** Download the latest poppler package and add the `bin` folder to your PATH.

## Installation

Clone this repository, create a virtual environment, and install the required dependencies:

```bash
git clone <repository_url>
cd Document_Classification_Extraction
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Usage

You can run the pipeline from the command line using `main.py`.

```bash
python main.py --file path/to/your/document.pdf --labels "invoice, receipt, contract, resume, other"
```

### Example
```bash
python main.py --file data/sample_invoice.png --labels "invoice, medical record, legal contract"
```

## How It Works

1. **Document Ingestion**: The system takes an image (PNG/JPG) or a PDF file. If it's a PDF, `pdf2image` converts it into images.
2. **Text Extraction (OCR)**: `pytesseract` extracts the raw text from the images.
3. **Classification (NLP)**: The extracted text is passed to a Hugging Face Transformers model (`facebook/bart-large-mnli` by default) for zero-shot classification against the labels you provide.
