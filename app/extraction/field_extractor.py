import re
from typing import Dict, Any
from app.classification.labels import DocumentType

def extract_invoice_fields(text: str) -> Dict[str, Any]:
    fields = {}
    # Basic regex patterns (can be improved with NER models)
    
    # Invoice number
    inv_match = re.search(r'(?i)invoice\s*(?:no|number|#)?\s*[:\-]?\s*([a-z0-9\-]+)', text)
    fields['invoice_number'] = inv_match.group(1) if inv_match else None
    
    # Date (simple MM/DD/YYYY or YYYY-MM-DD)
    date_match = re.search(r'(?i)date\s*[:\-]?\s*(\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4})', text)
    fields['date'] = date_match.group(1) if date_match else None
    
    # Total amount
    total_match = re.search(r'(?i)total\s*[:\-]?\s*[$€£]?\s*([\d,]+\.\d{2})', text)
    fields['total_amount'] = total_match.group(1) if total_match else None
    
    return fields

def extract_resume_fields(text: str) -> Dict[str, Any]:
    fields = {}
    
    # Name (heuristic: first non-empty line)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    fields['name'] = lines[0] if lines else None

    # Email
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    fields['email'] = email_match.group(0) if email_match else None
    
    # Phone
    phone_match = re.search(r'(?i)(?:phone|tel|mobile|cell)\s*[:\-]?\s*(\+?[\d\s\-\(\)]{7,20})', text)
    if phone_match:
        fields['phone'] = phone_match.group(1).strip()
    else:
        # Fallback generic pattern
        fallback_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        fields['phone'] = fallback_match.group(0) if fallback_match else None
        
    # LinkedIn
    linkedin_match = re.search(r'(?i)(?:linkedin\.com/in/)[a-zA-Z0-9_-]+/?', text)
    fields['linkedin'] = linkedin_match.group(0) if linkedin_match else None
    
    return fields

def extract_bank_statement_fields(text: str) -> Dict[str, Any]:
    fields = {}
    # Account Number / IBAN
    account_match = re.search(r'(?i)(?:account\s*number|iban)\s*[:\-]?\s*([a-z0-9 ]{8,34})', text)
    fields['account_number'] = account_match.group(1).strip() if account_match else None
    
    return fields

def extract_id_document_fields(text: str) -> Dict[str, Any]:
    fields = {}
    # Date of birth
    dob_match = re.search(r'(?i)dob|date\s*of\s*birth\s*[:\-]?\s*(\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4})', text)
    fields['date_of_birth'] = dob_match.group(1) if dob_match else None
    
    return fields

def extract_generic_fields(text: str) -> Dict[str, Any]:
    fields = {}
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    fields['emails'] = [email_match.group(0)] if email_match else []
    return fields

def extract_fields(text: str, document_type: str) -> Dict[str, Any]:
    """
    Routes the text to the appropriate field extractor based on document type.
    """
    if document_type == DocumentType.INVOICE:
        return extract_invoice_fields(text)
    elif document_type == DocumentType.RESUME:
        return extract_resume_fields(text)
    elif document_type == DocumentType.BANK_STATEMENT:
        return extract_bank_statement_fields(text)
    elif document_type == DocumentType.ID_DOCUMENT:
        return extract_id_document_fields(text)
    else:
        return extract_generic_fields(text)
