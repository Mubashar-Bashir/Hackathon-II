# ADR 007: JWT Authentication and Data Isolation Pattern

## Context

The system requires secure multi-user functionality where users authenticate via JWT tokens and can only access their own tasks. We need to implement a robust authentication mechanism that validates JWT tokens and enforces data isolation between users at the service and repository layers to prevent unauthorized cross-user data access.

## Decision

We will implement a layered security approach with:

1. **JWT Token Validation**: Using PyJWT library with HS256 algorithm and a shared BETTER_AUTH_SECRET for token encoding/decoding
2. **Authentication Middleware**: FastAPI dependency that extracts and validates JWT tokens from Authorization headers
3. **Service Layer Validation**: All service methods require user_id validation to ensure operations are performed on user-owned data
4. **Repository Level Enforcement**: Repository methods include user_id in queries to prevent unauthorized access at the database level
5. **Token Expiration**: 24-hour token lifetime as specified in requirements
6. **User Isolation Pattern**: All task operations include user_id filtering to ensure data isolation

## Status

Accepted

## Consequences

### Positive
- Strong security with multiple validation layers (middleware, service, repository)
- Proper data isolation preventing cross-user data access
- Industry-standard JWT authentication approach
- Clear separation of concerns with validation at appropriate layers
- Consistent user experience with token-based authentication
- Scalable to thousands of users with proper isolation

### Negative
- Additional complexity in implementation with multiple validation layers
- Performance overhead from JWT validation on each request
- Need for proper secret management for JWT signing
- More complex error handling for authentication failures
- Additional database query overhead for user_id validation

## Alternatives

### Alternative 1: Session-based Authentication
- Store session data server-side instead of JWT tokens
- Rejected because: Feature requirements specifically called for JWT-based authentication

### Alternative 2: Client-side Only Validation
- Only validate JWT tokens at the middleware level without additional service/repository validation
- Rejected because: Would create security vulnerability allowing bypass if service layer is accessed directly

### Alternative 3: Database-Level Row Level Security
- Use PostgreSQL row-level security instead of application-level filtering
- Rejected because: Adds database complexity and reduces application control over access logic

## References

- specs/004-auth-db-schema/plan.md
- specs/004-auth-db-schema/data-model.md
- specs/004-auth-db-schema/research.md
- src/core/security.py
- src/services/task_service.py
- src/storage/task_repository.py