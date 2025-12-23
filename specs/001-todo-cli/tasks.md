---
description: "Task list for Modular In-Memory Todo CLI System"
---

# Tasks: Modular In-Memory Todo CLI System

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `todo-app/src/`, `todo-app/tests/` at repository root
- Paths shown below follow the hexagonal architecture structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with todo-app/ directory
- [X] T002 Initialize Python 3.13+ project with uv and pyproject.toml
- [X] T003 [P] Install and configure Typer dependency for CLI
- [X] T004 [P] Install and configure Rich dependency for formatting
- [X] T005 [P] Install and configure Pydantic V2 dependency for data validation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create directory structure: todo-app/src/models/, todo-app/src/core/, todo-app/src/ui/, todo-app/src/storage/
- [X] T007 [P] Create __init__.py files in all directories
- [X] T008 Create base Task model in todo-app/src/models/todo.py based on data-model.md
- [X] T009 Create TaskStatus enum in todo-app/src/models/todo.py
- [X] T010 Create TaskRepository protocol in todo-app/src/storage/__init__.py
- [X] T011 Create abstract repository pattern structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new todo tasks with a title and optional description

**Independent Test**: Can run the CLI command to add a task and verify that the task appears in the system

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Unit test for Task creation in todo-app/tests/test_models.py
- [ ] T013 [P] [US1] Integration test for add task functionality in todo-app/tests/test_cli.py

### Implementation for User Story 1

- [X] T014 [P] [US1] Implement Task model with validation in todo-app/src/models/todo.py
- [X] T015 [US1] Create InMemoryTaskRepository in todo-app/src/storage/in_memory_storage.py
- [X] T016 [US1] Create TodoService in todo-app/src/core/todo_service.py with add_task method
- [X] T017 [US1] Implement add command in todo-app/src/ui/cli.py
- [X] T018 [US1] Add CLI help text for add command
- [X] T019 [US1] Connect add command to service and repository layers

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to see a list of all their tasks in a clear, tabular format

**Independent Test**: Can add some tasks and run the list command to display them in tabular format

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T020 [P] [US2] Unit test for list tasks functionality in todo-app/tests/test_models.py
- [X] T021 [P] [US2] Integration test for list command in todo-app/tests/test_cli.py

### Implementation for User Story 2

- [X] T022 [P] [US2] Add list_tasks method to TodoService in todo-app/src/core/todo_service.py
- [X] T023 [US2] Add list_tasks method to InMemoryTaskRepository in todo-app/src/storage/in_memory_storage.py
- [X] T024 [US2] Implement list command in todo-app/src/ui/cli.py
- [X] T025 [US2] Format output as table using Rich in the list command
- [X] T026 [US2] Connect list command to service and repository layers

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable users to mark tasks as complete/incomplete with toggle functionality

**Independent Test**: Can add a task, mark it complete, and verify the status changed

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T027 [P] [US3] Unit test for toggle task status in todo-app/tests/test_models.py
- [X] T028 [P] [US3] Integration test for complete command in todo-app/tests/test_cli.py

### Implementation for User Story 3

- [X] T029 [P] [US3] Add update_task method to TodoService in todo-app/src/core/todo_service.py
- [X] T030 [US3] Add update_task method to InMemoryTaskRepository in todo-app/src/storage/in_memory_storage.py
- [X] T031 [US3] Implement complete command in todo-app/src/ui/cli.py
- [X] T032 [US3] Add status toggle logic in the service layer
- [X] T033 [US3] Connect complete command to service and repository layers

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Update Task Details (Priority: P2)

**Goal**: Enable users to edit the title or description of existing tasks

**Independent Test**: Can add a task, update its details, and verify the changes were saved

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T034 [P] [US4] Unit test for update task functionality in todo-app/tests/test_models.py
- [X] T035 [P] [US4] Integration test for update command in todo-app/tests/test_cli.py

### Implementation for User Story 4

- [X] T036 [P] [US4] Add update_task method with specific fields in TodoService in todo-app/src/core/todo_service.py
- [X] T037 [US4] Enhance InMemoryTaskRepository to support partial updates in todo-app/src/storage/in_memory_storage.py
- [X] T038 [US4] Implement update command in todo-app/src/ui/cli.py
- [X] T039 [US4] Add validation for update parameters in the service layer
- [X] T040 [US4] Connect update command to service and repository layers

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Enable users to remove tasks from their list by ID

**Independent Test**: Can add a task, delete it, and verify it's no longer in the system

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T041 [P] [US5] Unit test for delete task functionality in todo-app/tests/test_models.py
- [X] T042 [P] [US5] Integration test for delete command in todo-app/tests/test_cli.py

### Implementation for User Story 5

- [X] T043 [P] [US5] Add delete_task method to TodoService in todo-app/src/core/todo_service.py
- [X] T044 [US5] Add delete_task method to InMemoryTaskRepository in todo-app/src/storage/in_memory_storage.py
- [X] T045 [US5] Implement delete command in todo-app/src/ui/cli.py
- [X] T046 [US5] Add error handling for invalid task IDs in the service layer
- [X] T047 [US5] Connect delete command to service and repository layers

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T048 [P] Add comprehensive error handling throughout the application
- [X] T049 Add input validation across all CLI commands
- [X] T050 [P] Create main application entry point in todo-app/src/main.py
- [X] T051 Add comprehensive docstrings to all functions and classes
- [X] T052 [P] Add logging throughout the application
- [X] T053 Create README.md with setup and usage instructions
- [X] T054 Run all implemented functionality through quickstart validation
- [X] T055 [P] Run code through @code-reviewer audit

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints/UI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task creation in todo-app/tests/test_models.py"
Task: "Integration test for add task functionality in todo-app/tests/test_cli.py"

# Launch all models for User Story 1 together:
Task: "Implement Task model with validation in todo-app/src/models/todo.py"
Task: "Create InMemoryTaskRepository in todo-app/src/storage/in_memory_storage.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence