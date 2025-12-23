---
description: "Task list for Task Organization & Usability feature implementation"
---

# Tasks: Task Organization & Usability

**Input**: Design documents from `/specs/001-task-organization/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Update pyproject.toml with any new dependencies for date parsing if needed

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 [P] Update Task model with new fields (priority, tags, due_date) in todo-app/src/models/todo.py
- [x] T003 [P] Create Priority enum in todo-app/src/models/todo.py
- [x] T004 [P] Create TaskFilter model in todo-app/src/models/todo.py
- [x] T005 [P] Create SortField and SortOrder enums in todo-app/src/models/todo.py
- [x] T006 [P] Create SortCriteria model in todo-app/src/models/todo.py
- [x] T007 Update InMemoryTaskRepository to handle new fields in todo-app/src/storage/in_memory_storage.py
- [x] T008 Update repository interface if needed in todo-app/src/storage/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Enhanced Task Creation with Organization (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with priority levels, tags, and optional due dates to better organize their work.

**Independent Test**: Users can create tasks with priority (Low, Medium, High with Medium as default), multiple tags (e.g., "work", "personal", "urgent"), and optional due dates. The system should store and display this information correctly.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Unit test for enhanced add_task method in todo-app/tests/unit/test_todo_service.py
- [ ] T010 [P] [US1] Test Task model with new fields in todo-app/tests/unit/test_models.py

### Implementation for User Story 1

- [x] T011 [US1] Implement enhanced add_task method in todo-app/src/core/todo_service.py
- [x] T012 [P] [US1] Update CLI add command with new options in todo-app/src/ui/cli.py
- [x] T013 [P] [US1] Update task display table to show new fields in todo-app/src/ui/cli.py
- [x] T014 [US1] Add validation for tags and due_date in todo-app/src/models/todo.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Filtering and Search (Priority: P2)

**Goal**: Users can filter their tasks by priority, status, or keyword search to quickly find relevant tasks among potentially many items.

**Independent Test**: Users can run commands like `list --filter priority=high` or `list --search "keyword"` and see only the matching tasks displayed.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T015 [P] [US2] Unit test for filter_tasks method in todo-app/tests/unit/test_todo_service.py
- [ ] T016 [P] [US2] Test keyword search functionality in todo-app/tests/unit/test_todo_service.py

### Implementation for User Story 2

- [x] T017 [US2] Implement filter_tasks method in todo-app/src/core/todo_service.py
- [x] T018 [US2] Implement keyword search functionality in todo-app/src/core/todo_service.py
- [x] T019 [P] [US2] Update CLI list command with filtering options in todo-app/src/ui/cli.py
- [x] T020 [P] [US2] Update CLI list command with search options in todo-app/src/ui/cli.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Advanced Task Sorting (Priority: P3)

**Goal**: Users can sort their tasks by different criteria (due date, priority, title) to better organize their workflow and focus on important items.

**Independent Test**: Users can run commands like `list --sort-by due_date` or `list --sort-by priority` and see tasks ordered according to their preference.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T021 [P] [US3] Unit test for sort_tasks method in todo-app/tests/unit/test_todo_service.py
- [ ] T022 [P] [US3] Test due_date sorting with null values in todo-app/tests/unit/test_todo_service.py

### Implementation for User Story 3

- [x] T023 [US3] Implement sort_tasks method in todo-app/src/core/todo_service.py
- [x] T024 [US3] Update list_tasks method to support sorting in todo-app/src/core/todo_service.py
- [x] T025 [P] [US3] Update CLI list command with sorting options in todo-app/src/ui/cli.py
- [x] T026 [P] [US3] Update task display to show priority with color coding in todo-app/src/ui/cli.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T027 [P] Update README with new CLI options in todo-app/README.md
- [x] T028 Update documentation for new features in todo-app/docs/
- [x] T029 Code cleanup and refactoring
- [x] T030 [P] Additional unit tests (if requested) in todo-app/tests/unit/
- [x] T031 Run quickstart validation
- [x] T032 Test backward compatibility with existing tasks

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May depend on US1 models
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May depend on US1/US2 models but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
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
Task: "Unit test for enhanced add_task method in todo-app/tests/unit/test_todo_service.py"
Task: "Test Task model with new fields in todo-app/tests/unit/test_models.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Update CLI add command with new options in todo-app/src/ui/cli.py"
Task: "Update task display table to show new fields in todo-app/src/ui/cli.py"
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