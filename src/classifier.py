from transformers import pipeline
import logging

# Set up logging to avoid noisy output from transformers
logging.getLogger("transformers").setLevel(logging.ERROR)

class DocumentClassifier:
    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        """
        Initializes the zero-shot classifier pipeline.
        This allows us to classify text without needing to train a model on specific labels.
        """
        print(f"Loading NLP model '{model_name}'... (This might take a moment if downloading for the first time)")
        self.classifier = pipeline("zero-shot-classification", model=model_name)

    def classify(self, text: str, candidate_labels: list, multi_label: bool = False) -> dict:
        """
        Classifies the given text against the candidate labels.
        
        Args:
            text (str): The text to classify.
            candidate_labels (list): A list of strings representing the possible categories.
            multi_label (bool): If True, multiple labels can be true. If False, the scores sum to 1.
            
        Returns:
            dict: The classification result containing 'labels' and 'scores'.
        """
        if not text or not text.strip():
            return {"error": "Input text is empty. Cannot classify."}
            
        # Truncate text if it's too long for the model (BART has a max length, typically 1024 tokens)
        # A rough heuristic: truncate to the first ~3000 characters which usually fits within limits.
        # For a more robust solution, you'd use the tokenizer directly.
        truncated_text = text[:3000] 
            
        result = self.classifier(truncated_text, candidate_labels, multi_label=multi_label)
        
        return {
            "predicted_label": result['labels'][0],
            "confidence": result['scores'][0],
            "all_labels": result['labels'],
            "all_scores": result['scores']
        }

if __name__ == "__main__":
    # Simple manual test
    clf = DocumentClassifier()
    res = clf.classify("Please find the attached invoice for your recent purchase of software licenses.", ["invoice", "resume", "legal contract"])
    print(res)
