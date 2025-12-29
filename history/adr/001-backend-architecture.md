# ADR-1: Backend Technology Stack and Architecture for Todo App

## Status
Accepted

## Date
2025-12-28

## Context
The project requires building a secure todo application with user authentication and task management capabilities. The backend needs to handle user registration/login, secure task CRUD operations with user isolation, and provide a robust API for frontend integration. Key concerns include security, scalability, maintainability, and proper separation of concerns.

## Decision
We have decided to use the following backend architecture:

- **Framework**: FastAPI for its type safety, automatic API documentation, and async support
- **ORM**: SQLModel for combining Pydantic and SQLAlchemy benefits
- **Authentication**: JWT tokens with custom implementation (instead of Better Auth) for direct control over token lifecycle
- **Database**: PostgreSQL with UUID primary keys for security and scalability
- **Architecture Pattern**: Clean architecture with Repository pattern, Service layer, and API layer separation
- **Security**: User isolation through JWT validation and user ID matching in API endpoints
- **API Design**: RESTful endpoints with user ID in URL path for access control enforcement

## Alternatives Considered
- **Framework alternatives**: Flask (less modern, less type safety), Django (heavier, overkill for API)
- **Authentication alternatives**: Session-based (requires shared session store), OAuth-only (doesn't support email/password), Better Auth (less control over implementation)
- **Database alternatives**: MongoDB (less structured), SQLite (less scalable), in-memory (not persistent)
- **Architecture alternatives**: Monolithic (tighter coupling), GraphQL (more complex for simple CRUD)

## Consequences
### Positive
- Type safety through Pydantic models reduces runtime errors
- Automatic API documentation with FastAPI
- JWT tokens provide stateless authentication
- Repository pattern enables easy testing and database switching
- User isolation prevents unauthorized data access
- RESTful design is familiar and well-supported

### Negative
- Learning curve for team members unfamiliar with FastAPI
- JWT token management requires careful implementation to prevent security issues
- Additional complexity from multi-layer architecture

## References
- plan.md: Technical Context and Project Structure sections
- research.md: Technology Stack and Authentication Approach decisions
- data-model.md: Entity relationships and security requirements