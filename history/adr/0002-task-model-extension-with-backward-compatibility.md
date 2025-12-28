---
status: Accepted
date: 2025-12-23
decision: Task Model Extension with Backward Compatibility
deciders:
consulted:
informed:
links:
  - specs/001-task-organization/plan.md
  - specs/001-task-organization/data-model.md
  - specs/001-task-organization/contracts/api-contracts.md
---

# ADR-002: Task Model Extension with Backward Compatibility

## Context

The existing Task model in the todo-app needs to be extended with new fields (priority, tags, due_date) to support task organization features while maintaining compatibility with existing tasks that don't have these fields. The system currently has a basic Task model with only id, title, description, and status fields.

## Decision

We will extend the existing Task model with three new fields:
- `priority`: Enum with Low, Medium, High values (default: Medium)
- `tags`: List of strings (default: empty list)
- `due_date`: Optional datetime field (default: None)

All new fields will have default values to ensure backward compatibility with existing tasks. When existing tasks are loaded, they will automatically receive the default values for new fields.

## Consequences

### Positive
- Existing tasks remain functional without modification
- New features can be implemented without breaking changes
- Consistent data model across old and new tasks
- Smooth migration path for existing users

### Negative
- Increased model complexity
- Storage overhead for existing tasks (though minimal with defaults)
- Potential confusion for users about default values

## Alternatives

### Alternative 1: Separate EnhancedTask model
Create a new EnhancedTask model while keeping the original Task model. This would require complex mapping logic and would fragment the data model.

### Alternative 2: Metadata field approach
Store all new organization data in a single metadata JSON field. This would sacrifice type safety and validation benefits of Pydantic models.

### Alternative 3: Database migration
Perform a formal migration to add fields. With in-memory storage, this is unnecessary complexity for the current phase.

## Rationale

The chosen approach maintains the simplicity of a single Task model while ensuring complete backward compatibility. Default values ensure that existing tasks behave predictably with new features without requiring explicit migration.
