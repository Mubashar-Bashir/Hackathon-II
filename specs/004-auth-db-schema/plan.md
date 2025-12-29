# Implementation Plan: Phase II: Core - Neon DB Schema & Better Auth JWT Integration

**Branch**: `004-auth-db-schema` | **Date**: 2025-12-26 | **Spec**: @specs/004-auth-db-schema/spec.md
**Input**: Feature specification from `/specs/004-auth-db-schema/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement secure task management with JWT-based authentication using Better Auth system and Neon PostgreSQL database. The system will validate JWT tokens, associate tasks with users, and enforce data isolation between users. This enables multi-user functionality with proper security controls.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, Pydantic V2, SQLModel, Better Auth, PyJWT, Neon PostgreSQL driver
**Storage**: Neon PostgreSQL database with SQLModel for ORM
**Testing**: pytest with unit and integration tests for authentication and data isolation
**Target Platform**: Linux server (backend API)
**Project Type**: web (backend API with authentication middleware)
**Performance Goals**: JWT token validation completes within 100ms for 95% of requests, support 1000 concurrent authenticated users
**Constraints**: <200ms p95 for authenticated requests, data isolation between users 100% of the time, JWT tokens expire in 24 hours
**Scale/Scope**: 10k users with proper data isolation, secure token validation

## Required Skills and Agents

**Decision Point**: Determine required skills and agents for implementation during planning phase

- **Core Development Skills**: Python development, FastAPI development, JWT authentication, SQLModel/PostgreSQL, Better Auth integration
- **Specialized Agents/Tools**: code generation agent for authentication middleware, database schema design agent, security validation agent, API contract generation agent
- **Integration Tools**: dependency management with uv, database migration tools, JWT validation libraries
- **Verification Agents**: security auditor for JWT implementation, database schema validator, integration testing agent

**Rationale**: Skills and agents should be decided during the planning phase when architectural decisions are made, rather than during specification phase which should focus on user requirements and success criteria.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Spec-Driven Development**: Following `/sp.plan` workflow as required by constitution
- ✅ **Python 3.13+**: Using Python 3.13+ as required by constitution
- ✅ **CLI-First**: Maintaining CLI interface while adding API layer
- ✅ **Dependency Management**: Using uv as required by constitution
- ✅ **Type Safety**: Using Pydantic V2 for data validation as required
- ✅ **Development Process**: Following Specification → Plan → Tasks → Implement workflow
- ✅ **Testing**: Planning for unit tests with >80% coverage
- ✅ **Error Handling**: Planning for explicit error handling for authentication failures

## Project Structure

### Documentation (this feature)

```text
specs/004-auth-db-schema/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model with Better Auth integration
│   │   └── task.py          # Task model with user_id association
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # JWT validation and user authentication
│   │   └── task_service.py  # Task operations with user validation
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   └── tasks.py         # Task endpoints with JWT middleware
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration including BETTER_AUTH_SECRET
│   │   └── security.py      # JWT middleware and security utilities
│   └── main.py              # FastAPI app entry point
└── tests/
    ├── unit/
    │   ├── test_auth.py     # Authentication unit tests
    │   └── test_tasks.py    # Task service unit tests
    ├── integration/
    │   ├── test_auth_api.py # Authentication API integration tests
    │   └── test_tasks_api.py # Task API integration tests
    └── contract/
        └── test_auth_contracts.py # JWT validation contract tests
```

**Structure Decision**: Backend API structure chosen to implement JWT authentication middleware and Neon PostgreSQL integration with proper separation of concerns between models, services, and API endpoints.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Repository pattern | Data isolation between users required | Direct DB access insufficient for user permission checks |
