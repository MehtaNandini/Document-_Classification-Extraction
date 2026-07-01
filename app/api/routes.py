import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.requests import ClassifyRequest, ExtractFieldsRequest
from app.schemas.responses import ClassificationResponse, FieldExtractionResponse, ProcessDocumentResponse
from app.utils.file_utils import save_upload_file_tmp
from app.utils.text_cleaning import clean_extracted_text
from app.extraction.text_extractor import process_document
from app.extraction.field_extractor import extract_fields
from app.classification.document_classifier import get_classifier

router = APIRouter()

@router.post("/process-document", response_model=ProcessDocumentResponse)
async def process_document_endpoint(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    tmp_path = await save_upload_file_tmp(file)
    
    try:
        # 1. Extract text
        raw_text = process_document(tmp_path)
        clean_text = clean_extracted_text(raw_text)
        
        # 2. Classify document
        classifier = get_classifier()
        doc_type, scores = classifier.classify(clean_text)
        
        # 3. Extract fields
        fields = extract_fields(clean_text, doc_type)
        
        return ProcessDocumentResponse(
            filename=file.filename,
            extracted_text=clean_text,
            classification=ClassificationResponse(document_type=doc_type, scores=scores),
            fields=FieldExtractionResponse(document_type=doc_type, extracted_fields=fields)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@router.post("/classify-document", response_model=ClassificationResponse)
def classify_document_endpoint(request: ClassifyRequest):
    clean_text = clean_extracted_text(request.text)
    classifier = get_classifier()
    doc_type, scores = classifier.classify(clean_text)
    return ClassificationResponse(document_type=doc_type, scores=scores)

@router.post("/extract-fields", response_model=FieldExtractionResponse)
def extract_fields_endpoint(request: ExtractFieldsRequest):
    clean_text = clean_extracted_text(request.text)
    fields = extract_fields(clean_text, request.document_type)
    return FieldExtractionResponse(document_type=request.document_type, extracted_fields=fields)
