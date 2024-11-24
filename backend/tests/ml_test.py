import pytest , asyncio
from app.services.ml_service import ContentModerationService, moderation_service

# Test service initialization
def test_service_initialization():
    service = ContentModerationService()
    assert service.model is not None
    assert service.tokenizer is not None
    print("Model and tokenizer initialized")

@pytest.mark.asyncio
async def test_content_moderation():
    # Test innocent content
    assert await moderation_service.is_content_allowed("Hello world") == True
    
    # Test offensive content
    assert await moderation_service.is_content_allowed("I hate everything") == False
    
    # Test edge cases
    assert await moderation_service.is_content_allowed("") == True
    assert await moderation_service.is_content_allowed(None) == True
    
    # Test more examples
    safe_texts = [
        "Good morning everyone!",
        "I love this beautiful day",
        "The weather is nice today",
    ]
    
    offensive_texts = [
        "You are all idiots",
        "I hate everyone here",
        "This is the worst thing ever, kill yourself",
    ]
    
    for text in safe_texts:
        assert await moderation_service.is_content_allowed(text) == True
        print(f"{text} is allowed")
        
    for text in offensive_texts:
        assert await moderation_service.is_content_allowed(text) == False
        print(f"{text} is not allowed")
