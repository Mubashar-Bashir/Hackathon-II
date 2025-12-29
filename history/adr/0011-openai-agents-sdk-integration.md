# ADR-0011: OpenAI Agents SDK Integration

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-29
- **Feature:** 009-openai-orchestration
- **Context:** Need to integrate AI orchestration capabilities that allow natural language processing of user requests and execution of MCP tools for task management. The system must follow official OpenAI patterns while maintaining stateless architecture and user isolation requirements.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Use OpenAI Agents SDK as the primary integration method for AI orchestration
- Implement MCP connector patterns following OpenAI's official guidance
- Register MCP tools (add_task, list_tasks, update_task, complete_task, delete_task) as external functions via the SDK
- Maintain stateless architecture by fetching conversation history from DB before each interaction
- Propagate JWT user_id through to all MCP tool calls for user isolation
- Transform technical errors to natural language responses for conversational UX

## Consequences

### Positive

- Follows official OpenAI integration patterns ensuring compatibility and support
- Enables natural language processing for task operations improving user experience
- Maintains compatibility with Layer 2 MCP tools while adding AI orchestration layer
- Proper user isolation maintained through JWT token propagation
- Stateless execution pattern preserves scalability requirements
- Leverages OpenAI's built-in tool calling capabilities for reliable function execution

### Negative

- Additional dependency complexity with OpenAI Agents SDK
- Potential latency overhead from conversation history DB queries
- Learning curve for developers unfamiliar with Agents SDK patterns
- Possible version compatibility issues with evolving OpenAI SDK
- Complexity in error handling when bridging natural language and technical operations

## Alternatives Considered

Alternative A: OpenAI Assistants API with built-in conversation memory
- Rejected because: Violates stateless architecture requirement per constitution
- Would store conversation state in OpenAI's system rather than local DB

Alternative B: Direct Chat Completions API with custom MCP protocol
- Rejected because: Would require custom implementation instead of following official patterns
- Would not leverage OpenAI's official MCP integration patterns

Alternative C: OpenAI Batch API for processing
- Rejected because: Not suitable for real-time chat interactions required by the feature
- Would not support conversational UX patterns

## References

- Feature Spec: /specs/009-openai-orchestration/spec.md
- Implementation Plan: /specs/009-openai-orchestration/plan.md
- Related ADRs: ADR-0009 (MCP Server Technology Stack), ADR-0010 (MCP Server Security Architecture)
- Evaluator Evidence: /specs/009-openai-orchestration/research.md