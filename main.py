import argparse
import json
from src.pipeline import DocumentPipeline

def main():
    parser = argparse.ArgumentParser(description="Document Classification & Extraction Pipeline")
    parser.add_argument(
        "--file", 
        type=str, 
        required=True, 
        help="Path to the document file (PDF, PNG, JPG, etc.)"
    )
    parser.add_argument(
        "--labels", 
        type=str, 
        required=True, 
        help="Comma-separated list of candidate labels (e.g., 'invoice, receipt, contract')"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="facebook/bart-large-mnli", 
        help="Hugging Face zero-shot classification model name"
    )

    args = parser.parse_args()

    # Parse labels
    candidate_labels = [label.strip() for label in args.labels.split(",") if label.strip()]
    if not candidate_labels:
        print("Error: No valid labels provided.")
        return

    # Initialize and run pipeline
    pipeline = DocumentPipeline(model_name=args.model)
    results = pipeline.process_document(args.file, candidate_labels)

    print("\n--- Classification Results ---")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
