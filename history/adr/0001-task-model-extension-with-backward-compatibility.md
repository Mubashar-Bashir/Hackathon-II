# ADR-0001: Task Model Extension with Backward Compatibility

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-23
- **Feature:** 001-task-organization
- **Context:** The Task Organization & Usability feature requires extending the existing Task model with new fields (priority, tags, due_date) while maintaining full backward compatibility with existing tasks. The system must support both new tasks with organization features and legacy tasks without these fields without requiring a migration process.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Extend the existing Task model with optional fields that have sensible defaults:
- Add `priority: Priority = Priority.MEDIUM` field with enum values (LOW, MEDIUM, HIGH)
- Add `tags: List[str] = Field(default_factory=list)` field with empty list as default
- Add `due_date: Optional[datetime] = None` field with None as default
- Maintain all existing fields unchanged to preserve compatibility
- Implement proper validation for new fields (tag format, date format, etc.)

## Consequences

### Positive

- Maintains complete backward compatibility with existing tasks
- No migration required for existing data
- New features can be added incrementally without disrupting current functionality
- Existing CLI commands continue to work exactly as before
- Clean and consistent data model that supports both legacy and new tasks
- Default values ensure new functionality works seamlessly with old data

### Negative

- New fields add complexity to the Task model even when not used
- Optional fields may require additional null checks in some operations
- Storage overhead for existing tasks that don't use new features
- Potential confusion for users about default values behavior

## Alternatives Considered

Alternative A: Separate models for different feature levels (legacy vs enhanced)
- Rejected because: Would require complex type handling, make the codebase more complex, and create unnecessary fragmentation

Alternative B: Inheritance approach (BaseTask, EnhancedTask)
- Rejected because: Would complicate the repository layer, add complexity to storage, and make the API inconsistent

Alternative C: Migration process to update all existing tasks
- Rejected because: Would add complexity, risk of data loss, and require downtime during migration

Alternative D: Require all fields for all tasks
- Rejected because: Would break backward compatibility and require all existing tasks to be updated

## References

- Feature Spec: /specs/001-task-organization/spec.md
- Implementation Plan: /specs/001-task-organization/plan.md
- Related ADRs: None
- Evaluator Evidence: /history/prompts/001-task-organization/0005-solid-plan-for-task-organization.plan.prompt.md
