# Layer 3 Design: OpenAI Agents SDK Orchestration

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  OpenAI Agent    │───▶│   MCP Tools     │
│                 │    │                  │    │                 │
│ Natural Language│    │ Intent Recognition│    │ 5 Task Operations│
│                 │    │ Tool Selection   │    │ (add, list,      │
└─────────────────┘    │ Response Gen     │    │ update, complete,│
                       │ Context Mgmt     │    │ delete)         │
                       └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Database       │
                       │                  │
                       │ Conversation     │
                       │ History & Tasks  │
                       └──────────────────┘
```

## Core Components

### 1. OpenAI Agent Orchestrator
**File**: `backend/src/agents/task_agent.py`

```python
class TaskAgentOrchestrator:
    def __init__(self, openai_client, mcp_tools):
        self.client = openai_client
        self.tools = mcp_tools  # MCP tools from Layer 2

    async def process_conversation(self, user_id: str, user_input: str, conversation_id: str = None):
        # Retrieve conversation history
        conversation = self.get_conversation_history(user_id, conversation_id)

        # Prepare messages with history
        messages = self.build_conversation_context(conversation, user_input)

        # Create agent run with tools
        response = await self.client.beta.threads.runs.create_and_poll(
            thread=self.create_thread(messages),
            assistant_id=self.assistant_id,
            tools=self.get_available_tools()
        )

        # Process and return response
        return self.format_response(response)
```

### 2. Conversation Manager
**File**: `backend/src/agents/conversation_manager.py`

```python
class ConversationManager:
    def __init__(self, db_session):
        self.db = db_session

    def get_conversation_history(self, user_id: str, conversation_id: str = None):
        """Retrieve conversation history from database"""
        pass

    def store_interaction(self, user_id: str, conversation_id: str, user_message: str, agent_response: str):
        """Store conversation interaction in database"""
        pass

    def create_new_conversation(self, user_id: str, title: str = None):
        """Create a new conversation for the user"""
        pass
```

### 3. Tool Mapper
**File**: `backend/src/agents/tool_mapper.py`

```python
class ToolMapper:
    def __init__(self, mcp_tools):
        self.mcp_tools = mcp_tools

    def map_natural_language_to_tool(self, user_input: str):
        """Map natural language to appropriate MCP tool with parameters"""
        pass

    def extract_entities(self, user_input: str):
        """Extract entities like task titles, dates, priorities from input"""
        pass
```

## API Endpoints

### 1. Chat Endpoint
**File**: `backend/src/api/v1/chat.py`

```python
@router.post("/chat")
async def chat_with_agent(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main endpoint for chatting with the task management agent
    """
    orchestrator = TaskAgentOrchestrator(
        openai_client=openai_client,
        mcp_tools=mcp_task_tools  # From Layer 2
    )

    response = await orchestrator.process_conversation(
        user_id=current_user.id,
        user_input=request.message,
        conversation_id=request.conversation_id
    )

    return ChatResponse(
        message=response,
        conversation_id=response.conversation_id
    )
```

### 2. Conversation Management Endpoints
```python
@router.get("/conversations")
async def list_user_conversations(current_user: User = Depends(get_current_user)):
    """List all conversations for the user"""

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, current_user: User = Depends(get_current_user)):
    """Get specific conversation with history"""

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, current_user: User = Depends(get_current_user)):
    """Delete a conversation"""
```

## Security Implementation

### 1. User Isolation
- All database queries must filter by `user_id`
- MCP tool calls must include correct `user_id`
- Conversation access restricted to owning user

### 2. Authentication Integration
- Use existing JWT authentication system
- Verify user identity before processing requests
- Pass validated user_id to all downstream operations

### 3. Tool Access Control
- Validate user permissions before MCP tool execution
- Log all tool calls for audit purposes
- Implement rate limiting for tool usage

## Error Handling Strategy

### 1. Tool Call Failures
- Graceful fallback when MCP tools unavailable
- User-friendly error messages
- Preserve conversation context during errors

### 2. OpenAI API Failures
- Retry logic for API calls
- Offline mode with limited functionality
- Proper error logging and monitoring

### 3. Database Connection Issues
- Connection pooling and retry logic
- Cache recent data when possible
- Graceful degradation of functionality

## Performance Considerations

### 1. Context Window Management
- Summarize long conversation histories
- Implement sliding window for recent context
- Load only necessary conversation history

### 2. Caching Strategy
- Cache recent MCP tool responses
- Cache conversation metadata
- Cache user preferences and settings

### 3. Asynchronous Processing
- Use async/await for all I/O operations
- Parallel processing where possible
- Non-blocking database operations

## Implementation Phases

### Phase 1: Basic Agent Integration
- [ ] Set up OpenAI Assistant with MCP tools
- [ ] Basic conversation flow
- [ ] Database integration for history
- [ ] User authentication integration

### Phase 2: Enhanced Features
- [ ] Advanced NLP and intent recognition
- [ ] Conversation context management
- [ ] Error handling and recovery
- [ ] Performance optimization

### Phase 3: Production Ready
- [ ] Monitoring and logging
- [ ] Rate limiting and security
- [ ] Testing and validation
- [ ] Documentation and deployment

## Dependencies Required

### Python Packages
- `openai` - OpenAI SDK
- `fastapi` - API framework
- `sqlmodel` - Database ORM
- `pydantic` - Data validation
- `uvicorn` - ASGI server

### External Services
- OpenAI API key
- PostgreSQL database (from Layer 1)
- MCP server (from Layer 2)

## Testing Strategy

### Unit Tests
- Tool mapping functionality
- Conversation management
- Error handling paths
- Authentication integration

### Integration Tests
- Full conversation flow
- MCP tool integration
- Database operations
- API endpoint functionality

### End-to-End Tests
- Complete user interaction flow
- Multi-turn conversations
- Error recovery scenarios
- Performance under load