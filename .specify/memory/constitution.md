<!--
Sync Impact Report:
Version change: 1.1.0 → 1.2.0
Added sections: Todo CLI app specific requirements and constraints
Removed sections: General references not specific to Phase I
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ updated to align with new principles
- .specify/templates/spec-template.md: ✅ updated to align with new principles
- .specify/templates/tasks-template.md: ✅ updated to align with new principles
- All command files in .claude/commands/: ✅ updated to align with new principles
Follow-up TODOs: None
-->
# Hackathon-II Constitution: Todo CLI App (Phase I)
<!-- From CLI to Distributed Cloud-Native AI Systems - Evolution of Todo -->

## Core Principles

### I. Evolutionary Strategy (The "Branch & Layer" Rule)
Single Core, Multiple Adapters: We do not create separate folders for phases. We evolve a single codebase with hexagonal architecture boundary where business logic resides in todo-app/src/core/ and must be "headless" (UI-agnostic). Git Snapshots: Every phase completion must be marked with a Git Tag (e.g., v1-cli, v2-web). Modular Expansion: New phases add new directories (e.g., todo-app/src/api/ for Phase II, todo-app/src/infra/ for Phase IV) rather than overwriting existing ones. For Phase I, this means implementing the Basic Level features in the todo-app directory structure.

### II. Architectural DNA
Logic Separation: todo-app/src/models/: Shared Pydantic V2 schemas. todo-app/src/core/: Domain logic (Todo Managers, Services). todo-app/src/ui/: CLI interfaces (Phase I). todo-app/src/storage/: Abstract Repository Pattern (In-Memory for Phase I). Strict Type Safety: Python 3.13+ with mandatory Type Hints. Package Management: Absolute enforcement of uv for all dependency operations. Phase I Requirements: Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete).

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. Verification Mandate: Every task generated in /sp.tasks MUST have a [ ] Verification sub-task (manual test or pytest). For Phase I, all Basic Level features must have comprehensive test coverage with minimum 80% test coverage.

### IV. SDD Execution Quality Gates
The Cascade Requirement: Follow Constitution ➡️ Spec ➡️ Plan ➡️ Tasks ➡️ Implementation. Reusable Intelligence: Always invoke @systems-architect for plan reviews and @code-reviewer for code audits. For Phase I, ensure all 5 Basic Level features are implemented before moving to Intermediate or Advanced features.

### V. Todo CLI Feature Requirements
Basic Level Implementation: Implement core functionality first - Add Task (with title and description), Delete Task (by ID), Update Task (by ID), View Task List (with status indicators), Mark as Complete (toggle status). These 5 features form the MVP of Phase I. Each feature must be CLI-accessible with proper error handling and user feedback.

### VI. Success Criteria and Phase I Deliverables
Phase I Success: Complete implementation of all 5 Basic Level features with proper CLI interface using Typer. Deliverables: GitHub repository with constitution, specs/todo-app/spec.md, specs/todo-app/plan.md, specs/todo-app/tasks.md, todo-app/src/ folder with Python source code, pyproject.toml, README.md with setup instructions, CLAUDE.md with Claude Code instructions, and working console application. Traceability: ADRs exist for every major architectural decision. Professionalism: Code passes ruff linting and includes Google-style docstrings.

## Development Standards
Technology Stack: UV, Python 3.13+, Pydantic V2, Typer, Rich, Claude Code, Spec-Kit Plus. Components must be compatible with Claude Code environment. Deployment must support dynamic loading of RI components. Strict enforcement of Python 3.13+, Pydantic V2, Typer, Rich, and uv package management. All code must be agent-generated with no manual syntax.

## Development Workflow
All RI components require specification before implementation; Code reviews must verify adherence to SDD-RI principles and invoke @code-reviewer agent; Testing gates require minimum coverage for all intelligence components with pytest; Deployment approval for new RI components follows standard process; All plans must be reviewed by @systems-architect agent. For Phase I, focus on CLI interface with in-memory storage, following the spec-driven development approach.

## Governance
All PRs/reviews must verify compliance with SDD-RI principles and Evolutionary Strategy; Complexity must be justified with intelligence reuse potential and architectural alignment; Use this constitution for runtime development guidance. All changes must follow the Cascade Requirement: Constitution ➡️ Spec ➡️ Plan ➡️ Tasks ➡️ Implementation. Phase I deliverables must include GitHub repository with constitution, specs history, todo-app/src folder, README.md, CLAUDE.md, and working console application demonstrating all 5 Basic Level features.

**Version**: 1.2.0 | **Ratified**: 2025-12-23 | **Last Amended**: 2025-12-23
