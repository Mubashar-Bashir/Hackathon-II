# ADR-0007: Backend Technology Stack Selection

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-27
- **Feature:** Todo App with Authentication and Task Management
- **Context:** Need to select appropriate backend technologies for a modern web application that will handle authentication, task management, and database operations. The stack must support RESTful API development, secure authentication, and efficient database operations while aligning with the overall architecture.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We will use the following backend technology stack:
- **Framework**: FastAPI (Python 3.13+)
- **Database ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens with PyJWT and bcrypt for password hashing
- **Security**: Passlib for password hashing, python-jose for JWT handling
- **Testing**: pytest for unit and integration testing

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- FastAPI provides excellent performance with async support and automatic API documentation
- SQLModel offers compatibility with both SQLAlchemy and Pydantic, enabling type safety
- Neon Serverless PostgreSQL provides automatic scaling and reduced operational overhead
- Pydantic integration ensures automatic request/response validation
- Built-in security features and middleware support for authentication
- Strong type hints and IDE support for better developer experience
- Active community and extensive documentation

### Negative

- Learning curve for developers not familiar with Python/async programming
- Potential performance overhead compared to compiled languages
- Dependency on external packages for authentication and security
- Need to manage Python environment and dependencies
- Potential async/await complexity for simple operations

## Alternatives Considered

- **Django**: Full-featured but heavier than needed for simple todo app - Rejected for unnecessary complexity
- **Flask**: More minimal but lacks built-in async support and automatic documentation - Rejected for less modern features
- **Node.js/Express**: Would create inconsistency with the microservice architecture decision - Rejected to maintain technology separation
- **Go with Gin**: Excellent performance but steeper learning curve and less Pydantic-like validation - Rejected for team familiarity concerns
- **Java with Spring Boot**: Robust but heavy for this use case - Rejected for complexity and longer development time
- **Ruby on Rails**: Good for rapid development but doesn't align with the Python ecosystem requirement - Rejected for consistency with overall architecture

## References

- Feature Spec: /specs/005-todo-auth/spec.md
- Implementation Plan: /specs/005-todo-auth/plan.md
- Related ADRs: ADR-0006 (Full-Stack Architecture), ADR-0008 (Frontend Technology Stack)
- Evaluator Evidence: /specs/005-todo-auth/research.md <!-- link to eval notes/PHR showing graders and outcomes -->
