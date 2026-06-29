import os
from .ocr_engine import OCREngine
from .classifier import DocumentClassifier

class DocumentPipeline:
    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        """
        Initializes the full document processing pipeline.
        """
        self.ocr_engine = OCREngine()
        self.classifier = DocumentClassifier(model_name=model_name)

    def process_document(self, file_path: str, candidate_labels: list) -> dict:
        """
        Processes a document: Extracts text via OCR and classifies it.
        
        Args:
            file_path (str): Path to the image or PDF document.
            candidate_labels (list): List of possible document categories.
            
        Returns:
            dict: The classification results along with a snippet of extracted text.
        """
        print(f"Processing document: {file_path}")
        
        # Step 1: Extract Text
        print("Extracting text via OCR...")
        extracted_text = self.ocr_engine.extract_text(file_path)
        
        if not extracted_text:
            return {
                "error": "Failed to extract text or document is empty.",
                "file_path": file_path
            }
            
        print(f"Extracted {len(extracted_text)} characters.")
        
        # Step 2: Classify Text
        print("Classifying text...")
        classification_results = self.classifier.classify(extracted_text, candidate_labels)
        
        # Append some helpful metadata to the result
        if "error" not in classification_results:
            classification_results["file_path"] = file_path
            classification_results["text_snippet"] = extracted_text[:200] + ("..." if len(extracted_text) > 200 else "")
            
        return classification_results
