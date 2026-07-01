from pydantic import BaseModel
from typing import Any, Dict

class ClassificationResponse(BaseModel):
    document_type: str
    scores: Dict[str, float]

class FieldExtractionResponse(BaseModel):
    document_type: str
    extracted_fields: Dict[str, Any]

class ProcessDocumentResponse(BaseModel):
    filename: str
    extracted_text: str
    classification: ClassificationResponse
    fields: FieldExtractionResponse
