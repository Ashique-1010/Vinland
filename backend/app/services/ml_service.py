from transformers import AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from scipy.special import softmax
from typing import Optional

class ContentModerationService():
    def __init__(self):
        """Initialize the offensive content detection model."""
        self.MODEL = "cardiffnlp/twitter-roberta-base-offensive"
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL)
            self.labels = self._load_labels()  # Load label mapping
            print("Content moderation model loaded successfully")

        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def _load_labels(self):
        """Load label mapping for the model."""
        import csv
        import urllib.request
        labels = []
        mapping_link = "https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/offensive/mapping.txt"
        try:
            with urllib.request.urlopen(mapping_link) as f:
                html = f.read().decode('utf-8').split("\n")
                csvreader = csv.reader(html, delimiter='\t')
                labels = [row[1] for row in csvreader if len(row) > 1]
        except Exception as e:
            print(f"Error loading label mapping: {e}")
        return labels        

    def _preprocess(self, text: str) -> str:
        """Handle usernames and links in text."""
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)
    
    async def is_content_allowed(self, text: Optional[str])-> str:
        """
        Check if content is safe to post.
        Returns True if content is safe, False if offensive or error occurs.
        """
        if not text:
            return True
        try:
            # Preprocess and encode
            processed_text = self._preprocess(text)
            encoded_input = self.tokenizer(processed_text, return_tensors='pt')

            # Get model prediction
            output = self.model(**encoded_input)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            offensive_index = self.labels.index("offensive") if "offensive" in self.labels else 1
            offensive_score = scores[offensive_index]
            print("offensive score = ", offensive_score)
            return offensive_score <= 0.8
        
        except Exception as e:
            print(f"Error in content moderation: {e}")
            return False  # Fail closed for safety

moderation_service = ContentModerationService()