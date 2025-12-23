# ADR-001: Hexagonal Architecture with Repository Pattern

## Status
Accepted

## Date
2025-12-23

## Context
The todo-cli application needed a clean, modular architecture that separates business logic from external concerns like CLI interfaces and storage implementations. The requirements included:
- Clear separation of concerns
- Testability of business logic without UI or storage dependencies
- Ability to swap storage implementations (in-memory for Phase I, persistent for Phase II)
- Maintainable and extensible codebase

## Decision
We adopted a hexagonal architecture (also known as ports and adapters) with the following components:

- **Models**: Pydantic data models for task validation and serialization
- **Core**: Business logic layer (TodoService) that depends only on abstractions
- **Storage**: Abstract repository interface with concrete implementations
- **UI**: CLI interface using Typer, depending on the core layer

The repository pattern provides an abstraction layer over data storage with:
- TaskRepository interface defining the contract
- InMemoryTaskRepository as the initial implementation
- Dependency injection allowing the service to work with any repository implementation

## Alternatives Considered
- **Monolithic approach**: Single files containing all logic - rejected due to poor testability and maintainability
- **MVC pattern**: Traditional Model-View-Controller - rejected as it doesn't provide the same level of separation from external concerns
- **Layered architecture**: Simple layered approach without explicit ports/adapters - rejected as it's less explicit about dependencies

## Consequences

### Positive
- Business logic is isolated and testable without external dependencies
- Storage implementation can be swapped without affecting business logic
- Clear boundaries between different concerns
- Easier to write unit tests for business logic
- Supports the open/closed principle (open for extension, closed for modification)

### Negative
- More complex initial setup with additional abstraction layers
- Slight overhead from interfaces and dependency injection
- Steeper learning curve for new team members

## References
- src/models/todo.py - Task model with Pydantic validation
- src/core/todo_service.py - Business logic layer
- src/storage/in_memory_storage.py - Repository implementation
- src/storage/__init__.py - Repository interface