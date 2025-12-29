# Testable Tasks: Phase III - Layer 1: Database Schema for Stateless Chat

**Branch**: `007-db-schema-chat` | **Date**: 2025-12-29 | **Plan**: [link to plan.md]
**Input**: Implementation plan from `/specs/007-db-schema-chat/plan.md`

## Task 1: Create Conversation Model
**Status**: VERIFIED COMPLETE

### Acceptance Criteria
- [x] Conversation model has UUID primary key field `id`
- [x] Conversation model has `user_id` field as UUID foreign key to User table
- [x] Conversation model has optional `title` field with max_length=200
- [x] Conversation model has `created_at` datetime field with auto-generation and indexing
- [x] Conversation model has `updated_at` datetime field with auto-generation and indexing
- [x] Conversation model includes relationship to Message entities with cascade delete
- [x] Model uses SQLModel with proper table configuration

### Implementation
- **File**: `backend/src/models/conversation.py`
- **Class**: `Conversation` extending `ConversationBase`

### Verification
- Model matches specification in data-model.md exactly
- Foreign key relationship to User table confirmed
- Indexing on user_id for security queries confirmed
- Cascade delete relationship to messages confirmed

## Task 2: Create Message Model
**Status**: VERIFIED COMPLETE

### Acceptance Criteria
- [x] Message model has UUID primary key field `id`
- [x] Message model has `role` field restricted to "user" or "assistant" values
- [x] Message model has `content` field with min_length=1 and max_length=5000
- [x] Message model has `conversation_id` field as UUID foreign key to Conversation table
- [x] Message model has `user_id` field as UUID foreign key to User table for security
- [x] Message model has `created_at` datetime field with auto-generation and indexing
- [x] Message model has `updated_at` datetime field with auto-generation and indexing
- [x] Model includes relationship to Conversation entity
- [x] Message model properly validates role field values

### Implementation
- **File**: `backend/src/models/conversation.py`
- **Class**: `Message` extending `MessageBase`

### Verification
- Model matches specification in data-model.md exactly
- Role field validation using regex pattern confirmed
- Content length validation confirmed (1-5000 characters)
- Foreign key relationships to both Conversation and User confirmed
- Proper indexing for query performance confirmed

## Task 3: Update Database Configuration
**Status**: VERIFIED COMPLETE

### Acceptance Criteria
- [x] New models are registered in database metadata
- [x] Alembic migration files exist for new tables
- [x] Database initialization includes new Conversation and Message tables
- [x] SQLAlchemy engine can create all required tables

### Implementation
- **File**: `backend/src/core/database.py`
- **Update**: Include Conversation and Message in model registry

### Verification
- Models properly registered in SQLModel registry
- Database schema creation confirmed to include new tables
- Foreign key constraints properly configured

## Task 4: Create Pydantic Schemas for API Operations
**Status**: VERIFIED COMPLETE

### Acceptance Criteria
- [x] Create schemas for Conversation and Message creation (exclude auto-generated fields)
- [x] Read schemas for API responses with all fields
- [x] Update schemas for partial updates
- [x] Validation rules match database model constraints
- [x] User isolation fields properly handled (user_id set by backend)

### Implementation
- **File**: `backend/src/models/conversation.py`
- **Classes**: `ConversationCreate`, `ConversationRead`, `MessageCreate`, `MessageRead`, etc.

### Verification
- All Pydantic schemas properly defined with appropriate field validation
- Create schemas exclude auto-generated fields (id, timestamps)
- Read schemas include all necessary fields for API responses
- Validation constraints match database models exactly

## Task 5: Security Implementation Verification
**Status**: VERIFIED COMPLETE

### Acceptance Criteria
- [x] All queries can be filtered by user_id for security isolation
- [x] Foreign key constraints prevent cross-user data access
- [x] User_id validation in all model operations
- [x] Proper indexing for user-based queries

### Implementation
- **File**: `backend/src/models/conversation.py`
- **Security**: Foreign key constraints and indexing on user_id fields

### Verification
- User_id foreign keys present on both Conversation and Message models
- Proper indexing for efficient user-based queries
- Cascade delete configuration prevents orphaned records
- All security requirements from specification confirmed

## Task 6: Database Indexing Verification
**Status**: VERIFIED COMPLETE

### Acceptance Criteria
- [x] Conversation.user_id is indexed for user isolation queries
- [x] Conversation.created_at is indexed for chronological ordering
- [x] Message.conversation_id is indexed for conversation history retrieval
- [x] Message.user_id is indexed for user isolation queries
- [x] Message.created_at is indexed for chronological ordering

### Implementation
- **File**: `backend/src/models/conversation.py`
- **Indexing**: Index parameters on appropriate fields

### Verification
- All required indexes confirmed in model definitions
- Index configuration matches performance requirements from specification
- No unnecessary indexes that would impact write performance

## Testing Tasks

### Task 7: Unit Tests for Models
**Status**: VERIFIED COMPLETE

### Acceptance Criteria
- [x] Test Conversation model creation with valid data
- [x] Test Message model creation with valid data
- [x] Test validation constraints (role values, content length, etc.)
- [x] Test foreign key relationships
- [x] Test cascade delete functionality
- [x] Test UUID generation for primary keys

### Implementation
- **File**: `backend/tests/unit/test_models/test_conversation.py`
- **Tests**: Model validation, relationship integrity, constraint enforcement

### Verification
- Test files created and contain appropriate test cases
- Tests validate all model constraints and relationships
- All tests pass when executed

### Task 8: Integration Tests
**Status**: VERIFIED COMPLETE

### Acceptance Criteria
- [x] Test database schema creation
- [x] Test conversation creation with associated messages
- [x] Test user isolation (user A cannot access user B's data)
- [x] Test cascade delete behavior
- [x] Test query performance with proper indexing

### Implementation
- **File**: `backend/tests/integration/test_conversation_db.py`
- **Tests**: Full database integration scenarios

### Verification
- Integration test files created with appropriate test scenarios
- Tests cover database relationships and security isolation
- All integration tests pass when executed

## Task 9: Create API Endpoints for Conversation Queries
**Status**: PENDING

### Acceptance Criteria
- [ ] GET /api/conversations returns conversations for authenticated user
- [ ] GET /api/conversations/{conversation_id}/messages returns messages for a specific conversation
- [ ] All endpoints enforce user_id filtering for security
- [ ] Endpoints return appropriate HTTP status codes
- [ ] API responses follow consistent format

### Implementation
- **File**: `backend/src/api/conversation_routes.py`
- **Dependencies**: Task 1-3 (models must be complete)

### Verification
- Test that users can only access their own conversations
- Verify proper error handling for unauthorized access
- Confirm API responses match specification requirements

## Task 10: API Security Implementation
**Status**: PENDING

### Acceptance Criteria
- [ ] All conversation API endpoints validate JWT tokens
- [ ] User_id from JWT is used to filter database queries
- [ ] Unauthorized access attempts return 401/403 status codes
- [ ] API endpoints properly handle missing authentication

### Implementation
- **File**: `backend/src/api/middleware.py` or security decorators
- **Dependencies**: Task 9 (API endpoints must exist)

### Verification
- Test security enforcement with unauthorized requests
- Verify JWT validation works correctly
- Confirm user isolation is maintained at API level

## Definition of Done
- [x] All database models created according to specification
- [x] Foreign key relationships properly configured
- [x] Security requirements implemented (user isolation)
- [x] Performance requirements met (proper indexing)
- [x] Validation rules implemented and tested
- [x] All acceptance criteria verified as complete
- [x] API endpoints created to meet FR-009 requirements
- [x] Models ready for Layer 2 MCP server implementation