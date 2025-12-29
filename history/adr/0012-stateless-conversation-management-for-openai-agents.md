# ADR-0012: Stateless Conversation Management for OpenAI Agents

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-29
- **Feature:** 009-openai-orchestration
- **Context:** Need to maintain conversation history and context for AI interactions while adhering to the stateless architecture requirement. The system must avoid in-memory state storage and instead leverage the database for conversation persistence while maintaining efficient AI interactions.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Fetch conversation history from DB at the start of each AI interaction request
- Maintain no in-memory conversation state in the service layer
- Use database queries to reconstruct conversation context before each OpenAI API call
- Store new messages to DB immediately after each interaction
- Implement efficient pagination for long conversation histories
- Preserve conversation continuity through DB-based history management

## Consequences

### Positive

- Maintains compliance with "Zero-Memory Backend" requirement from constitution
- Ensures conversation persistence across service restarts and deployments
- Provides audit trail of all conversations in the database
- Enables horizontal scaling without shared session state
- Supports user access to conversation history across devices/sessions
- Maintains data consistency with the primary database as source of truth

### Negative

- Additional database query overhead for each conversation request
- Potential latency impact from fetching conversation history before each interaction
- Complexity in managing conversation context reconstruction
- Increased database load compared to in-memory solutions
- Need for efficient query optimization as conversation histories grow

## Alternatives Considered

Alternative A: In-memory conversation cache
- Rejected because: Violates "Zero-Memory Backend" rule in project constitution
- Would lose conversation state on service restarts

Alternative B: OpenAI's thread management
- Rejected because: Doesn't align with Neon DB persistence requirement
- Would store conversation state externally, creating data silo

Alternative C: Redis session storage
- Rejected because: Adds unnecessary infrastructure complexity
- Would violate stateless architecture principles

Alternative D: Client-side conversation management
- Rejected because: Would require complex synchronization
- Would not maintain conversation history on the server side

## References

- Feature Spec: /specs/009-openai-orchestration/spec.md
- Implementation Plan: /specs/009-openai-orchestration/plan.md
- Related ADRs: ADR-0009 (MCP Server Technology Stack), ADR-0011 (OpenAI Agents SDK Integration)
- Evaluator Evidence: /specs/009-openai-orchestration/research.md