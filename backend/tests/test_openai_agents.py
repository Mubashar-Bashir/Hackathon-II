"""
Test suite for OpenAI Agents Orchestration
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import sys
import os

# Set environment variable before imports
os.environ['OPENAI_API_KEY'] = 'test-key'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.task_agent import TaskAgent


def test_task_agent_initialization():
    """Test that TaskAgent can be initialized"""
    # Mock the OpenAI client
    with patch('src.core.openai_config.get_openai_client') as mock_client:
        agent = TaskAgent()
        assert agent is not None
        assert agent.model == "gpt-4-turbo"  # default model


@pytest.mark.asyncio
async def test_conversation_manager():
    """Test basic conversation manager functionality"""
    from src.agents.conversation_manager import ConversationManager
    from sqlmodel import Session

    # Mock the database session
    mock_session = Mock(spec=Session)
    manager = ConversationManager(mock_session)

    # Test that we can create a manager instance
    assert manager is not None


@pytest.mark.asyncio
async def test_tool_mapper():
    """Test basic tool mapper functionality"""
    from src.agents.tool_mapper import ToolMapper
    from src.services.mcp_client import MCPClient

    # Create a mock MCP client
    mock_mcp_client = Mock(spec=MCPClient)
    mock_mcp_client.add_task = AsyncMock(return_value={"success": True, "task_id": "test"})

    mapper = ToolMapper(mock_mcp_client)

    # Test that we can create a mapper instance
    assert mapper is not None


if __name__ == "__main__":
    pytest.main([__file__])