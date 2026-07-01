from pydantic import BaseModel

class ClassifyRequest(BaseModel):
    text: str

class ExtractFieldsRequest(BaseModel):
    text: str
    document_type: str
