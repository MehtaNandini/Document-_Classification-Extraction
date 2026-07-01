from app.utils.text_cleaning import clean_extracted_text

def test_clean_extracted_text_multiple_spaces():
    raw_text = "This    is   a      test"
    cleaned = clean_extracted_text(raw_text)
    assert cleaned == "This is a test"

def test_clean_extracted_text_multiple_newlines():
    raw_text = "Line 1\n\n\n\nLine 2\n\n\n\n\nLine 3"
    cleaned = clean_extracted_text(raw_text)
    assert cleaned == "Line 1\n\nLine 2\n\nLine 3"

def test_clean_extracted_text_strip():
    raw_text = "   Hello World   "
    cleaned = clean_extracted_text(raw_text)
    assert cleaned == "Hello World"
