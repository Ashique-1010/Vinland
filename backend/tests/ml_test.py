import pytest, asyncio
from app.services.ml_service import ContentModerationService, moderation_service

# Test service initialization
def test_service_initialization():
    try:
        service = ContentModerationService()
        assert service.model is not None, "Model failed to initialize"
        assert service.tokenizer is not None, "Tokenizer failed to initialize"
        print("Model and tokenizer initialized successfully")
    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

@pytest.mark.asyncio
async def test_content_moderation():
    try:
        # Test innocent content
        assert await moderation_service.is_content_allowed("Hello world") == True, "'Hello world' should be allowed"
        
        # Test offensive content
        assert await moderation_service.is_content_allowed("I hate all niggas") == False, "I hate all niggas should not be allowed"
        
        # Test edge cases
        assert await moderation_service.is_content_allowed("") == True, "Empty string should be allowed"
        assert await moderation_service.is_content_allowed(None) == True, "None should be allowed"
        
        # Test more examples
        safe_texts = [
            "Good morning everyone!",
            "I love this beautiful day",
            "The weather is nice today",
        ]
        
        offensive_texts = [
            "You are all idiots",
            "I fucking hate everyone here",
            "This is the worst thing ever, kill yourself",
        ]
        
        for text in safe_texts:
            try:
                assert await moderation_service.is_content_allowed(text) == True, f"'{text}' should be allowed"
                print(f"{text} is allowed")
            except AssertionError as ae:
                print(f"Assertion Error for text '{text}': {ae}")
                raise
            except Exception as e:
                print(f"An unexpected error occurred for text '{text}': {e}")
                raise
                
        for text in offensive_texts:
            try:
                assert await moderation_service.is_content_allowed(text) == False, f"'{text}' should not be allowed"
                print(f"{text} is not allowed")
            except AssertionError as ae:
                print(f"Assertion Error for text '{text}': {ae}")
                raise
            except Exception as e:
                print(f"An unexpected error occurred for text '{text}': {e}")
                raise
                
    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred in test_content_moderation: {e}")
        raise