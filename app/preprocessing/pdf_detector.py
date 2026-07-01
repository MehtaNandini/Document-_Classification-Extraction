import pdfplumber

def is_digital_pdf(file_path: str) -> bool:
    """
    Heuristic to determine if a PDF is digital (text-based) or scanned (image-based).
    Returns True if significant text is found, False otherwise.
    """
    if not file_path.lower().endswith(".pdf"):
        return False
        
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            # Check up to first 3 pages
            for i, page in enumerate(pdf.pages):
                if i >= 3:
                    break
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            
            # If we extract more than 50 characters, we assume it's digital text
            return len(text.strip()) > 50
    except Exception:
        return False
