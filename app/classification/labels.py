from enum import Enum

class DocumentType(str, Enum):
    INVOICE = "invoice"
    RESUME = "resume/cv"
    BANK_STATEMENT = "bank statement"
    ID_DOCUMENT = "id document"
    GENERIC = "generic document"

# Labels used for zero-shot classification
CANDIDATE_LABELS = [
    DocumentType.INVOICE.value,
    DocumentType.RESUME.value,
    DocumentType.BANK_STATEMENT.value,
    DocumentType.ID_DOCUMENT.value,
    DocumentType.GENERIC.value
]
