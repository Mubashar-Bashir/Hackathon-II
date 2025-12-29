---
name: sqlmodel-db-expert
description: Expert in creating and managing SQLModel database models with proper relationships, validation, and security patterns. Can help with database schema design, model creation, and relationship management for any layer that requires database models. Use when working with database models, schema design, relationship management, or security scoping requirements.
---

# SQLModel Database Model Expert

## Use Cases
- Creating SQLModel database tables with proper relationships
- Implementing validation rules and constraints
- Setting up foreign key relationships and cascade operations
- Designing secure models with user isolation patterns
- Creating Pydantic schemas for API operations

## Capabilities
- Create SQLModel classes with proper inheritance patterns
- Implement proper indexing for performance
- Set up foreign key relationships with security in mind
- Design validation patterns using Pydantic v2
- Create base models for inheritance patterns

## Common Issues and Solutions

### Issue 1: Context Manager Missing Decorator
**Problem**: The `get_session_context()` function was defined as a generator but used as a context manager with `with` statements without the `@contextmanager` decorator.
**Solution**: Add the `@contextmanager` decorator from `contextlib` to the function.
**Error**: `TypeError: 'generator' object does not support the context manager protocol`

### Issue 2: Model Validation Error
**Problem**: The `Task` model requires a `user_id` field, but when using `Task.model_validate(task_create.model_dump())`, the `user_id` was not included in the validation data.
**Solution**: Create the `Task` instance directly with all required fields instead of using model validation from `TaskCreate`.
**Error**: `pydantic_core._pydantic_core.ValidationError: 1 validation error for Task user_id Field required`

### Issue 3: Session Management and Refresh
**Problem**: After adding an object to the session, calling `session.refresh()` before the transaction was committed resulted in an error.
**Solution**: Use `session.flush()` to assign IDs without committing, then use separate sessions for different operations since the context manager commits and closes the session.
**Error**: `sqlalchemy.exc.InvalidRequestError: Instance is not persistent within this Session`

### Issue 4: Database Connection
**Problem**: Tests failed due to missing PostgreSQL database connection.
**Solution**: For testing purposes, use mocking to verify logic without requiring a running database, or ensure the database is properly configured and running.
**Error**: `psycopg2.OperationalError: connection to server at "localhost" failed: Connection refused`

### Issue 5: Duplicate Import Statement
**Problem**: The `contextlib` import was duplicated in the file.
**Solution**: Remove the duplicate import and ensure imports are at the top of the file.

## Best Practices

1. **Always use `@contextmanager` decorator** when creating generator functions intended for `with` statements.
2. **Understand model relationships** - `TaskCreate` vs `Task` models have different required fields.
3. **Proper session management** - Use `flush()` for ID assignment, separate sessions for different operations when using context managers.
4. **Database setup** - Ensure the database is running before executing database-dependent tests.
5. **Model validation** - Be aware of which fields are required vs optional in different model classes.
6. **Error handling** - Always consider database connection failures and implement proper error handling.