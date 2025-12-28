# ADR-0006: Full-Stack Web Application with Microservice Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-27
- **Feature:** Todo App with Authentication and Task Management
- **Context:** Need to build a modern full-stack todo application with secure user authentication and comprehensive task management. The application requires a scalable architecture that separates concerns between frontend and backend services while maintaining secure communication and user data isolation.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We will implement a microservice architecture with separate frontend and backend services:
- **Frontend**: Next.js 16+ with App Router
- **Backend**: Python FastAPI API service
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens for secure communication between services
- **Communication**: RESTful API with JWT token-based authentication and user ID validation for data isolation

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Clear separation of concerns between frontend and backend services
- Independent scaling capabilities for frontend and backend
- Technology flexibility - can update services independently
- Proper security isolation with JWT-based authentication
- User data isolation through backend validation of user IDs
- Modern development experience with established frameworks
- Efficient database operations with SQLModel ORM

### Negative

- Increased complexity with multiple services to manage
- Additional network latency between services
- More complex deployment and monitoring requirements
- Need for shared secrets management (JWT secret)
- Potential for service versioning conflicts

## Alternatives Considered

- **Monolithic Architecture**: Single application serving both frontend and backend - Rejected because it would mix concerns, limit scalability, and make technology updates harder
- **Full Python Stack (FastAPI + Jinja2)**: Server-side rendering with Python - Rejected because it provides less modern UI experience and limits frontend flexibility
- **Full JavaScript Stack (Express + Next.js)**: Would require managing multiple JavaScript runtimes - Rejected for complexity and resource usage concerns
- **GraphQL API**: More complex for basic todo functionality - Rejected as overkill for simple task management requirements
- **Server-side rendering with unified deployment**: Less flexible scaling - Rejected for scalability limitations

## References

- Feature Spec: /specs/005-todo-auth/spec.md
- Implementation Plan: /specs/005-todo-auth/plan.md
- Related ADRs: ADR-0007 (Backend Technology Stack), ADR-0008 (Frontend Technology Stack)
- Evaluator Evidence: /specs/005-todo-auth/research.md <!-- link to eval notes/PHR showing graders and outcomes -->
