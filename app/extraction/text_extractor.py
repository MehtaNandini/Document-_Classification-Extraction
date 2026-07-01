import os
import pdfplumber
import tempfile
from pdf2image import convert_from_path
from app.preprocessing.pdf_detector import is_digital_pdf
from app.extraction.ocr_engine import extract_text_from_image

def extract_text_from_pdf_digital(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_pdf_scanned(file_path: str) -> str:
    text = ""
    # Convert PDF pages to images
    # Note: Requires poppler to be installed on the system
    images = convert_from_path(file_path)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        for i, image in enumerate(images):
            tmp_img_path = os.path.join(tmp_dir, f"page_{i}.png")
            image.save(tmp_img_path, "PNG")
            page_text = extract_text_from_image(tmp_img_path, preprocess=True)
            text += page_text + "\n"
            
    return text

def process_document(file_path: str) -> str:
    """
    Given a file path (PDF, PNG, JPG), extract its text content.
    Automatically handles digital vs. scanned PDFs and images.
    """
    ext = file_path.lower().split(".")[-1]
    
    if ext == "pdf":
        if is_digital_pdf(file_path):
            return extract_text_from_pdf_digital(file_path)
        else:
            return extract_text_from_pdf_scanned(file_path)
    elif ext in ["png", "jpg", "jpeg"]:
        return extract_text_from_image(file_path, preprocess=True)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
