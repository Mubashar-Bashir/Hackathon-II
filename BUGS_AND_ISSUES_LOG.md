# Bug Issues and Solutions Log

## Issue 1: Context Manager Missing Decorator
**Problem**: The `get_session_context()` function was defined as a generator but used as a context manager with `with` statements without the `@contextmanager` decorator.

**Error**:
```
TypeError: 'generator' object does not support the context manager protocol
```

**Solution**: Added the `@contextmanager` decorator from `contextlib` to the function.

**File**: `backend/src/core/database.py`
```python
from contextlib import contextmanager

@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    # function implementation
```

**Impact**: Without this fix, any code using `with get_session_context() as session:` would fail.

---

## Issue 2: Model Validation Error
**Problem**: The `Task` model requires a `user_id` field, but when using `Task.model_validate(task_create.model_dump())`, the `user_id` was not included in the validation data.

**Error**:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Task
user_id
  Field required [type=missing, input_value={...}, input_type=dict]
```

**Solution**: Create the `Task` instance directly with all required fields instead of using model validation from `TaskCreate`.

**Code Fix**:
```python
# Instead of:
task = Task.model_validate(task_create.model_dump())
task.user_id = test_user_id

# Use:
task = Task(
    title=task_create.title,
    description=task_create.description,
    status=task_create.status or "pending",
    priority=task_create.priority or "medium",
    due_date=task_create.due_date,
    user_id=test_user_id
)
```

**Impact**: The `TaskCreate` model excludes `user_id` (as noted in comments "does not include user_id (set by backend)"), but the `Task` model requires it.

---

## Issue 3: Session Management and Refresh
**Problem**: After adding an object to the session, calling `session.refresh()` before the transaction was committed resulted in an error.

**Error**:
```
sqlalchemy.exc.InvalidRequestError: Instance '<Task at 0x...>' is not persistent within this Session
```

**Solution**: Use `session.flush()` to assign IDs without committing, then use separate sessions for different operations since the context manager commits and closes the session.

**Code Fix**:
```python
session.add(task)
session.flush()  # This assigns the ID without committing
task_id = task.id

# For subsequent operations, use new sessions:
with get_session_context() as new_session:
    retrieved_task = new_session.get(Task, task_id)
```

**Impact**: Proper session lifecycle management is critical for database operations.

---

## Issue 4: Database Connection
**Problem**: Tests failed due to missing PostgreSQL database connection.

**Error**:
```
psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
```

**Solution**: For testing purposes, use mocking to verify logic without requiring a running database, or ensure the database is properly configured and running.

**Impact**: Tests requiring database connectivity will fail without a properly configured database.

---

## Issue 5: Duplicate Import Statement
**Problem**: The `contextlib` import was duplicated in the file.

**Solution**: Removed the duplicate import and ensured imports are at the top of the file.

**Impact**: Code cleanliness and avoiding potential import conflicts.

---

## Best Practices Learned

1. **Always use `@contextmanager` decorator** when creating generator functions intended for `with` statements.

2. **Understand model relationships** - `TaskCreate` vs `Task` models have different required fields.

3. **Proper session management** - Use `flush()` for ID assignment, separate sessions for different operations when using context managers.

4. **Database setup** - Ensure the database is running before executing database-dependent tests.

5. **Model validation** - Be aware of which fields are required vs optional in different model classes.

6. **Error handling** - Always consider database connection failures and implement proper error handling.

These issues provide valuable learning for future development with SQLModel, database sessions, and context managers.