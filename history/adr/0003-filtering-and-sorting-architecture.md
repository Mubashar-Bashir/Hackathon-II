---
status: Accepted
date: 2025-12-23
decision: Filtering and Sorting Architecture
deciders:
consulted:
informed:
links:
  - specs/001-task-organization/plan.md
  - specs/001-task-organization/data-model.md
  - specs/001-task-organization/contracts/api-contracts.md
---

# ADR-003: Filtering and Sorting Architecture

## Context

The system needs to support filtering and sorting of tasks by multiple criteria (priority, status, tags, due_date, etc.) while maintaining the hexagonal architecture pattern. The business logic must remain in the core service layer, with the UI layer only calling service methods.

## Decision

We will implement filtering and sorting in the TodoService layer with dedicated methods:
- `filter_tasks()`: Applies multiple filter criteria to a task list
- `sort_tasks()`: Sorts tasks by specified field and order
- `list_tasks()`: Enhanced to support optional filtering and sorting parameters

The CLI layer will expose these capabilities through command-line options like `--priority`, `--search`, `--sort-by`, etc.

## Consequences

### Positive
- Business logic remains centralized in the service layer
- Consistent filtering/sorting behavior across all UIs
- Flexible combination of filtering and sorting operations
- Clear separation of concerns per hexagonal architecture

### Negative
- Increased complexity in the service layer
- Need to handle complex parameter combinations
- Performance considerations for large datasets

## Alternatives

### Alternative 1: Database-level filtering/sorting
Implement filtering/sorting at the repository level. This would be premature optimization for in-memory storage and would complicate the repository interface.

### Alternative 2: UI-layer filtering/sorting
Handle filtering/sorting in the UI layer. This would violate the hexagonal architecture principle of keeping business logic in the core.

### Alternative 3: Separate filter/sort services
Create dedicated FilterService and SortService. This would add unnecessary complexity for the current scope.

## Rationale

The chosen approach maintains the hexagonal architecture while providing flexible filtering and sorting capabilities. The service layer is the appropriate place for this business logic, and the enhanced list_tasks method provides a clean interface for the UI layer.
