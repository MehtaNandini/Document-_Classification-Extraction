import cv2
from PIL import Image

def preprocess_image_for_ocr(image_path: str) -> Image.Image:
    """
    Preprocess image to improve OCR accuracy:
    - Convert to grayscale
    - Apply noise removal (blur)
    - Apply thresholding
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image from {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Noise removal
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Thresholding (Otsu's binarization)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Convert back to PIL Image for pytesseract
    pil_img = Image.fromarray(thresh)
    return pil_img
