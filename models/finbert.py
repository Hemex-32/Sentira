import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class FinBERT:
    _instance = None
    _pipeline = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FinBERT, cls).__new__(cls)
            cls._initialize_pipeline()
        return cls._instance

    @classmethod
    def _initialize_pipeline(cls):
        model_name = "ProsusAI/finbert"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Use GPU if available
        device = 0 if torch.cuda.is_available() else -1
        cls._pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

    def score_headlines(self, headlines: list[str]) -> list[dict]:
        """
        Score a list of headlines using FinBERT.
        Returns a list of dicts with 'label' and 'score' (confidence).
        """
        if not headlines:
            return []
        
        # Truncate headlines to 512 tokens to avoid errors
        truncated_headlines = [h[:512] for h in headlines]
        
        results = self._pipeline(truncated_headlines)
        return results

# Singleton instance for easy access
finbert_model = FinBERT()

if __name__ == "__main__":
    # Quick manual test
    test_headlines = [
        "Apple shares rise on strong iPhone sales",
        "Tesla stock plunges after disappointing earnings",
        "Microsoft to acquire small AI startup"
    ]
    scores = finbert_model.score_headlines(test_headlines)
    for h, s in zip(test_headlines, scores):
        print(f"Headline: {h} | Result: {s}")
