# Research: OpenAI Agents Orchestration

## Decision: OpenAI Agents SDK with MCP Integration
**Rationale**: Following OpenAI's official guidance for MCP (Model Context Protocol) integration, the OpenAI Agents SDK provides proper patterns for integrating external tools. This aligns with the architecture that requires MCP tools from Layer 2 to be accessible to the AI agent.

**Alternatives considered**:
- OpenAI Assistants API: Provides built-in conversation memory but violates stateless architecture requirement
- OpenAI Batch API: Not suitable for real-time chat interactions
- Direct Chat Completions API: Would require custom MCP protocol implementation

## Decision: MCP Tool Integration via Agents SDK
**Rationale**: MCP tools from Layer 2 (add_task, list_tasks, update_task, complete_task, delete_task) will be integrated through the OpenAI Agents SDK's MCP connector patterns, following official integration guidelines.

**Alternatives considered**:
- REST API gateway: Would add unnecessary complexity
- Service layer: Would create additional failure points
- Custom MCP implementation: Would not follow official patterns

## Decision: JWT Token Propagation
**Rationale**: User authentication and isolation maintained by extracting JWT user_id from request and passing it to each MCP tool call, ensuring proper user scoping.

**Alternatives considered**:
- Session-based context: Violates stateless architecture
- Conversation metadata: Could be bypassed if not properly validated

## Decision: Stateless Conversation Management
**Rationale**: Conversation history fetched from DB at start of each request to maintain stateless architecture per constitution requirements, following OpenAI's session storage patterns.

**Alternatives considered**:
- In-memory cache: Violates "Zero-Memory Backend" rule
- OpenAI thread memory: Doesn't align with Neon DB persistence requirement
- SQLite session storage: Would add unnecessary complexity for this use case

## Decision: Natural Language Error Handling
**Rationale**: Technical errors transformed to user-friendly natural language responses to maintain conversational UX while being transparent about issues, following OpenAI's recommended error handling patterns.

**Alternatives considered**:
- Silent retries: Could cause confusion if operations fail
- Technical error messages: Would break conversational UX