import re

def clean_extracted_text(text: str) -> str:
    """
    Cleans OCR or PDF extracted text by removing excessive whitespace
    and standardizing newlines.
    """
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Replace multiple newlines with a double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
