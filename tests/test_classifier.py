from app.classification.document_classifier import get_classifier

def test_classifier_returns_valid_label():
    classifier = get_classifier()
    # Mock text that strongly resembles an invoice
    text = "Invoice # 5000\nTotal Amount: $500.00\nPlease pay within 30 days."
    
    label, scores = classifier.classify(text)
    
    # Check that a label is returned
    assert label is not None
    # Check that scores are populated
    assert len(scores) > 0
