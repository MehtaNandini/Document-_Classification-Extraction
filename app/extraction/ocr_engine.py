import pytesseract
from PIL import Image
from app.preprocessing.image_preprocessor import preprocess_image_for_ocr

def extract_text_from_image(image_path: str, preprocess: bool = True) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """
    if preprocess:
        img = preprocess_image_for_ocr(image_path)
    else:
        img = Image.open(image_path)
        
    text = pytesseract.image_to_string(img)
    return text
