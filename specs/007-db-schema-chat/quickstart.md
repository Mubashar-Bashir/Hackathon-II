# Quickstart: Phase III - Layer 1 Database Schema for Stateless Chat

## Overview
This guide provides the essential steps to implement the Conversation and Message database models for the stateless AI chat system.

## Prerequisites
- Python 3.13+
- SQLModel installed
- Neon PostgreSQL database configured
- Existing user and task models in place

## Implementation Steps

### 1. Create the Conversation and Message Models
Create `backend/src/models/conversation.py` with:
- Conversation model with user_id foreign key
- Message model with role, content, and security constraints
- Proper relationships and cascading deletes

### 2. Update Database Configuration
Update `backend/src/core/database.py` to include the new models in the metadata:
- Import Conversation and Message models
- Ensure they're registered with SQLModel.metadata

### 3. Generate Database Migration
Create Alembic migration for the new tables:
- Generate migration script for Conversation and Message tables
- Include proper foreign key constraints
- Add necessary indexes for performance

### 4. Apply Database Migration
Run the migration to create the tables in the database:
- Execute migration against Neon PostgreSQL
- Verify table creation and constraints

### 5. Test Model Relationships
Verify the models work correctly:
- Create conversation and message records
- Test cascading delete functionality
- Verify user isolation constraints

## Key Files to Modify
- `backend/src/models/conversation.py` - New models
- `backend/src/core/database.py` - Model registration
- Database migration files - Schema updates

## Validation Steps
1. Verify Conversation model creates properly with user_id
2. Verify Message model creates with role and content constraints
3. Test relationship between Conversation and Message
4. Verify cascading delete functionality
5. Confirm user isolation works properly
6. Test with multiple users to ensure data separation

## Common Issues
- Foreign key constraint violations: Ensure user_id exists before creating records
- UUID generation issues: Use uuid.uuid4() for primary keys
- Index performance: Verify proper indexes are created for query patterns
- User isolation: Always filter queries by user_id