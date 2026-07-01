from app.extraction.field_extractor import extract_fields
from app.classification.labels import DocumentType

def test_extract_invoice_fields():
    text = "Invoice Number: INV-12345\nDate: 2026-07-01\nTotal: $1,250.00"
    fields = extract_fields(text, DocumentType.INVOICE)
    assert fields.get("invoice_number") == "INV-12345"
    assert fields.get("date") == "2026-07-01"
    assert fields.get("total_amount") == "1,250.00"

def test_extract_resume_fields():
    text = "John Doe\njohn.doe@email.com\n(555) 123-4567"
    fields = extract_fields(text, DocumentType.RESUME)
    assert fields.get("email") == "john.doe@email.com"
    assert fields.get("phone") == "(555) 123-4567"

def test_extract_bank_statement_fields():
    text = "Your statement for Account Number 1234567890\nClosing balance"
    fields = extract_fields(text, DocumentType.BANK_STATEMENT)
    assert fields.get("account_number") == "1234567890"

def test_extract_id_document_fields():
    text = "Date of Birth: 01/15/1990"
    fields = extract_fields(text, DocumentType.ID_DOCUMENT)
    assert fields.get("date_of_birth") == "01/15/1990"
