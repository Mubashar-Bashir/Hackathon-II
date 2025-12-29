---
status: Accepted
date: 2025-12-23
decision: CLI Command Enhancement Strategy
deciders:
consulted:
informed:
links:
  - specs/001-task-organization/plan.md
  - specs/001-task-organization/contracts/api-contracts.md
---

# ADR-0004: CLI Command Enhancement Strategy

## Context

The existing CLI commands need to be enhanced with new options to support task organization features (priority, tags, due dates, filtering, sorting) while maintaining backward compatibility with existing command syntax and user workflows.

## Decision

We will enhance the existing CLI commands with optional parameters rather than creating new separate commands:
- Enhance `add` command with `--priority`, `--tags`, and `--due-date` options
- Enhance `list` command with `--priority`, `--tag`, `--search`, `--sort-by`, and `--sort-order` options
- Maintain all existing command syntax and behavior for backward compatibility

## Consequences

### Positive
- Maintains familiarity for existing users
- Consistent command structure
- No breaking changes to existing workflows
- Single command for each operation with enhanced capabilities

### Negative
- Commands become more complex with many options
- Potential parameter conflicts need to be handled
- More complex validation logic in CLI layer

## Alternatives

### Alternative 1: Separate new commands
Create new commands like `add-organized`, `list-filtered`, etc. This would fragment the user experience and create unnecessary complexity.

### Alternative 2: Subcommand approach
Use subcommands like `todo task add --priority high`. This would require more significant changes to the CLI structure.

### Alternative 3: Configuration files
Allow users to specify options in configuration files. This adds complexity for simple filtering operations.

## Rationale

The chosen approach maintains backward compatibility while extending functionality. Optional parameters allow existing users to continue using commands as before while providing new capabilities for users who need task organization features. This follows the principle of progressive disclosure where advanced features are available but don't complicate basic usage.
