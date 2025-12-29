# Implementation Tasks: Phase II: Core - Neon DB Schema & Better Auth JWT Integration

## Feature Overview
Implement secure task management with JWT-based authentication using Better Auth system and Neon PostgreSQL database. The system will validate JWT tokens, associate tasks with users, and enforce data isolation between users.

## Phase 1: Setup
Initialize project structure and dependencies for authentication and database integration.

- [X] T001 Create backend directory structure per implementation plan in backend/src/
- [X] T002 [P] Set up Python dependencies with uv including fastapi, sqlmodel, pyjwt, better-auth, psycopg2-binary
- [X] T003 [P] Create configuration module for BETTER_AUTH_SECRET and database settings in backend/src/core/config.py
- [X] T004 [P] Set up environment variables documentation in .env.example
- [X] T005 [P] Configure shared BETTER_AUTH_SECRET environment variable for both frontend and backend consistency in backend/src/core/config.py

## Phase 2: Foundational Components
Implement core infrastructure components that all user stories depend on.

- [X] T006 [P] Create JWT utility functions for token encoding/decoding in backend/src/core/security.py
- [X] T007 [P] Implement JWT authentication middleware in backend/src/core/security.py
- [X] T008 [P] Create database models for User entity using SQLModel in backend/src/models/user.py
- [X] T009 [P] Create database models for Task entity with user_id association using SQLModel in backend/src/models/task.py
- [X] T010 [P] Set up database connection and session management in backend/src/core/database.py
- [X] T011 [P] Create abstract repository interface in backend/src/storage/base_repository.py
- [X] T012 [P] Implement SQL repository for Task operations with user filtering in backend/src/storage/task_repository.py
- [X] T013 [P] Implement SQL repository for User operations in backend/src/storage/user_repository.py

## Phase 3: User Story 1 - Secure Task Access with Authentication (Priority: P1)
Users must authenticate before they can access their tasks. When a user logs in, they should be able to view, create, update, and delete only their own tasks.

- [X] T015 [US1] Create authentication service for user registration and login in backend/src/services/auth_service.py
- [X] T016 [P] [US1] Implement auth registration endpoint POST /auth/register in backend/src/api/auth.py
- [X] T017 [P] [US1] Implement auth login endpoint POST /auth/login in backend/src/api/auth.py
- [X] T018 [P] [US1] Implement auth me endpoint GET /auth/me in backend/src/api/auth.py
- [X] T019 [P] [US1] Implement auth logout endpoint POST /auth/logout in backend/src/api/auth.py
- [X] T020 [P] [US1] Create task service with user validation in backend/src/services/task_service.py
- [X] T021 [P] [US1] Implement get tasks endpoint GET /tasks with user filtering in backend/src/api/tasks.py
- [X] T022 [P] [US1] Implement create task endpoint POST /tasks with user association in backend/src/api/tasks.py
- [X] T023 [P] [US1] Implement get task by ID endpoint GET /tasks/{id} with user validation in backend/src/api/tasks.py
- [X] T024 [P] [US1] Implement update task endpoint PUT /tasks/{id} with user validation in backend/src/api/tasks.py
- [X] T025 [P] [US1] Implement delete task endpoint DELETE /tasks/{id} with user validation in backend/src/api/tasks.py
- [X] T026 [US1] Integrate authentication middleware with FastAPI app in backend/src/main.py
- [ ] T027 [US1] Test user registration and login flow with JWT token generation
- [ ] T028 [US1] Test task creation with proper user_id association
- [ ] T029 [US1] Test task access restrictions (users can only access their own tasks)

## Phase 4: User Story 2 - JWT Token Validation (Priority: P2)
The system must validate JWT tokens using the BETTER_AUTH_SECRET to ensure tokens are authentic and haven't been tampered with. Tokens must be properly decoded from the Authorization: Bearer <token> header format.

- [ ] T030 [US2] Enhance JWT validation to check token expiration and signature in backend/src/core/security.py
- [ ] T031 [P] [US2] Add validation for Authorization header format in JWT middleware
- [ ] T032 [P] [US2] Implement proper error responses for invalid/expired tokens in backend/src/core/security.py
- [ ] T033 [US2] Test JWT validation with valid tokens
- [ ] T034 [US2] Test JWT validation with invalid/expired tokens
- [ ] T035 [US2] Test JWT validation with malformed Authorization headers

## Phase 5: User Story 3 - Task Data Association (Priority: P3)
The system must properly associate tasks with users using a user_id column in the Task table. This enables proper data isolation between users.

- [ ] T036 [US3] Enhance task repository to enforce user_id filtering in queries in backend/src/storage/task_repository.py
- [ ] T037 [P] [US3] Add user_id validation in task service to prevent unauthorized access in backend/src/services/task_service.py
- [ ] T038 [US3] Test task creation ensuring user_id is properly set to authenticated user
- [ ] T039 [US3] Test data isolation between different users' tasks
- [ ] T040 [US3] Test cross-user access prevention for tasks

## Phase 6: Testing and Validation
Implement comprehensive tests to ensure all functionality works as expected.

- [X] T041 [P] Create unit tests for authentication service in backend/tests/unit/test_auth.py
- [X] T042 [P] Create unit tests for task service in backend/tests/unit/test_tasks.py
- [X] T043 [P] Create integration tests for authentication API in backend/tests/integration/test_auth_api.py
- [X] T044 [P] Create integration tests for task API with authentication in backend/tests/integration/test_tasks_api.py
- [X] T045 [P] Create contract tests for JWT validation in backend/tests/contract/test_auth_contracts.py
- [X] T046 Run all tests to verify complete functionality

## Phase 7: Polish & Cross-Cutting Concerns
Final implementation details and cross-cutting concerns.

- [ ] T046 Implement proper error response format with message and error_code for all endpoints
- [ ] T047 Add password validation according to security requirements (8+ chars, mixed case, numbers, special chars)
- [ ] T048 Set JWT token expiration to 24 hours as specified in requirements
- [ ] T049 Add comprehensive logging for authentication events
- [ ] T050 Update API documentation with authentication requirements
- [ ] T051 Perform security review of JWT implementation and data isolation
- [ ] T052 Handle database connection failures during authentication with appropriate error responses
- [ ] T053 Implement token validation when user account is deleted but JWT token is still valid
- [ ] T054 Test concurrent requests with the same JWT token for thread safety
- [ ] T055 Handle malformed JWT tokens with appropriate error responses

## Dependencies
- User Story 2 (JWT Validation) depends on foundational JWT utilities (T008)
- User Story 3 (Task Data Association) depends on Task model with user_id (T010)
- All authenticated endpoints depend on authentication middleware (T007)
- Configuration of shared secret (T005) is foundational for both frontend and backend

## Parallel Execution Opportunities
- Tasks T002-T005 can be executed in parallel as they handle different setup concerns
- Authentication endpoints (T016-T019) can be developed in parallel with task endpoints (T021-T025)
- Repository implementations (T013-T014) can be developed in parallel
- Unit tests (T041-T042) and integration tests (T043-T044) can be developed in parallel

## Implementation Strategy
- MVP Scope: Implement User Story 1 (T015-T029) for basic authenticated task management
- Incremental Delivery: Add JWT validation (User Story 2) and data association (User Story 3) in subsequent iterations
- Each phase is independently testable with clear acceptance criteria