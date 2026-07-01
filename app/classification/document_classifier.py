from transformers import pipeline
from typing import Tuple, Dict
from app.classification.labels import CANDIDATE_LABELS, DocumentType
from app.core.config import settings

class DocumentClassifier:
    def __init__(self):
        # Initialize zero-shot classification pipeline
        self.classifier = pipeline(
            "zero-shot-classification",
            model=settings.classification_model_name
        )

    def classify(self, text: str) -> Tuple[str, Dict[str, float]]:
        """
        Classifies the document text into one of the candidate labels.
        Returns the top label and a dictionary of all scores.
        """
        if not text.strip():
            return "unknown", {}

        # Truncate text to avoid exceeding model max length (usually 512 for BERT variants)
        # Using first 1500 chars as a heuristic
        truncated_text = text[:1500] 
        
        result = self.classifier(truncated_text, CANDIDATE_LABELS)
        
        # Result contains 'labels' and 'scores' in sorted order
        best_label = result['labels'][0]
        
        scores = {label: score for label, score in zip(result['labels'], result['scores'])}
        
        # Keyword heuristics to correct common zero-shot misclassifications
        text_upper = text.upper()
        if "WORK EXPERIENCE" in text_upper or "EDUCATION" in text_upper or "CURRICULUM VITAE" in text_upper:
            best_label = DocumentType.RESUME.value
            scores[best_label] = 0.99
        
        return best_label, scores

# Singleton instance
classifier_instance = None

def get_classifier() -> DocumentClassifier:
    global classifier_instance
    if classifier_instance is None:
        classifier_instance = DocumentClassifier()
    return classifier_instance
