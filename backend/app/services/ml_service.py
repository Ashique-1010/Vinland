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
            print("Content moderation model loaded successfully")

        except Exception as e:
            print(f"Error loading model: {e}")
            raise

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

            offensive_score = scores[1]
            return offensive_score <= 0.5
        
        except Exception as e:
            print(f"Error in content moderation: {e}")
            return False  # Fail closed for safety

moderation_service = ContentModerationService()