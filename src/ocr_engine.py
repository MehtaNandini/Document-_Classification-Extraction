import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

class OCREngine:
    def __init__(self):
        """
        Initializes the OCR Engine.
        Ensure that Tesseract OCR and poppler are installed on your system.
        """
        pass

    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extracts text from a single image using Tesseract OCR.
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from image {image_path}: {e}")
            return ""

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extracts text from a PDF file by converting its pages to images
        and then applying OCR on each page.
        """
        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_path)
            full_text = ""
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image)
                full_text += f"\n--- Page {i + 1} ---\n"
                full_text += page_text
            
            return full_text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF {pdf_path}: {e}")
            return ""

    def extract_text(self, file_path: str) -> str:
        """
        Determines the file type based on extension and extracts text accordingly.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self.extract_text_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats are PDF and common images.")

if __name__ == "__main__":
    # Simple manual test
    engine = OCREngine()
    # text = engine.extract_text("sample.png")
    # print(text)
