import pytest
from datetime import datetime, timezone
import uuid
from src.models.conversation import Conversation, Message, ConversationCreate, MessageCreate
from pydantic import ValidationError

def test_conversation_model_creation():
    """Test creating a conversation model with valid data"""
    user_id = uuid.uuid4()
    conversation = Conversation(
        id=uuid.uuid4(),
        user_id=user_id,
        title="Test Conversation",
    )

    assert conversation.user_id == user_id
    assert conversation.title == "Test Conversation"
    assert isinstance(conversation.created_at, datetime)

def test_message_model_creation():
    """Test creating a message model with valid data"""
    conversation_id = uuid.uuid4()
    user_id = uuid.uuid4()

    message = Message(
        id=uuid.uuid4(),
        role="user",
        content="Test message content",
        conversation_id=conversation_id,
        user_id=user_id
    )

    assert message.role in ["user", "assistant"]
    assert len(message.content) > 0
    assert message.conversation_id == conversation_id

def test_message_role_validation():
    """Test that message role field only accepts valid values"""
    invalid_data = {
        'id': uuid.uuid4(),
        'role': "invalid_role",
        'content': "Test message",
        'conversation_id': uuid.uuid4(),
        'user_id': uuid.uuid4()
    }
    with pytest.raises(ValueError):
        Message.model_validate(invalid_data)

def test_message_content_length_validation():
    """Test that message content is within required length limits"""
    # Test minimum length
    empty_content_data = {
        'id': uuid.uuid4(),
        'role': "user",
        'content': "",  # Empty content should fail
        'conversation_id': uuid.uuid4(),
        'user_id': uuid.uuid4()
    }
    with pytest.raises(ValueError):
        Message.model_validate(empty_content_data)

    # Test maximum length
    long_content = "a" * 5001  # Exceeds 5000 character limit
    long_content_data = {
        'id': uuid.uuid4(),
        'role': "user",
        'content': long_content,
        'conversation_id': uuid.uuid4(),
        'user_id': uuid.uuid4()
    }
    with pytest.raises(ValueError):
        Message.model_validate(long_content_data)