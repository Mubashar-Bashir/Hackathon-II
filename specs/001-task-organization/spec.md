# Feature Specification: Task Organization & Usability

**Feature Branch**: `001-task-organization`
**Created**: 2025-12-23
**Status**: Draft
**Input**: User description: "Phase I.2: Intermediate Evolution - Organization & Usability
Context: * Project Root: ~/code/Hackathon-II/todo-app

Current State: Basic CRUD is functional in src/.

Goal: Evolve the system to support task organization, search, and sorting while maintaining Hexagonal Architecture.

🎯 1. Functional Requirements (Intermediate)
Priorities & Tags:

Add priority (Enum: Low, Medium, High).

Add tags (List of strings) to the Todo data structure.

Add an optional due_date (ISO format string or datetime).

Search & Filter:

Keyword Search: Filter tasks by substring match in title or description.

Status/Priority Filter: View only \"Completed\" tasks or only \"High\" priority tasks.

Advanced Sorting:

Enable sorting by due_date, priority (High to Low), or alphabetically by title.

🏗️ 2. Architectural DNA (Structural Evolution)
src/models/: Update Pydantic models to include new fields with default values to maintain backward compatibility with Phase I data.

src/core/: Update the TodoManager logic to include filter() and sort() methods. Rule: All logic must stay here; the UI should only call these methods.

src/ui/: Update the CLI to support new flags (e.g., --priority, --tag, --sort-by).

src/storage/: Ensure the InMemoryRepository can handle the updated model attributes.

🎨 3. UX/UI Standards
Use the Rich library to color-code priorities in the table (e.g., High = Bold Red, Medium = Yellow, Low = Green).

Add a \"Tags\" column to the display table.

✅ 4. Acceptance Criteria (Definition of Done)
[ ] I can add a task with a priority and multiple tags.

[ ] I can run a command like list --filter priority=high and see only high-priority tasks.

[ ] All Phase I features (Add/Delete/Complete) still work perfectly.

[ ] Code passes @code-reviewer audit for Type Hinting and clean separation of concerns."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enhanced Task Creation with Organization (Priority: P1)

Users need to add tasks with priority levels, tags, and optional due dates to better organize their work. This allows them to categorize and prioritize their tasks effectively.

**Why this priority**: This is the foundation for all other organization features. Without the ability to add organized tasks, filtering and sorting features would have no data to work with.

**Independent Test**: Users can create tasks with priority (Low, Medium, High with Medium as default), multiple tags (e.g., "work", "personal", "urgent"), and optional due dates. The system should store and display this information correctly.

**Acceptance Scenarios**:

1. **Given** a user wants to create a new task, **When** they use the add command with priority, tags, and due date parameters, **Then** the task is created with all specified organization attributes
2. **Given** a user creates a task without priority/tags/due date, **When** they save the task, **Then** the task is created with default values that maintain backward compatibility (Medium priority, empty tags list)

---

### User Story 2 - Task Filtering and Search (Priority: P2)

Users need to filter their tasks by priority, status, or keyword search to quickly find relevant tasks among potentially many items.

**Why this priority**: This significantly improves usability by allowing users to focus on specific subsets of their tasks without manually scanning through all items.

**Independent Test**: Users can run commands like `list --filter priority=high` or `list --search "keyword"` and see only the matching tasks displayed.

**Acceptance Scenarios**:

1. **Given** a user has multiple tasks with different priorities, **When** they run `list --filter priority=high`, **Then** only high-priority tasks are displayed
2. **Given** a user has tasks with various titles and descriptions, **When** they run `list --search "keyword"`, **Then** only tasks containing that keyword in title or description are shown

---

### User Story 3 - Advanced Task Sorting (Priority: P3)

Users need to sort their tasks by different criteria (due date, priority, title) to better organize their workflow and focus on important items.

**Why this priority**: This enhances the user experience by allowing them to view tasks in the most relevant order for their current needs.

**Independent Test**: Users can run commands like `list --sort-by due_date` or `list --sort-by priority` and see tasks ordered according to their preference.

**Acceptance Scenarios**:

1. **Given** a user has tasks with various due dates, **When** they run `list --sort-by due_date`, **Then** tasks are displayed in chronological order (earliest first) with tasks having null due dates appearing last
2. **Given** a user has tasks with different priorities, **When** they run `list --sort-by priority`, **Then** tasks are displayed with highest priority first

---

### Edge Cases

- What happens when a task has an invalid date format for due_date?
- How does the system handle empty tags list or null priority values?
- What occurs when searching for a keyword that matches both title and description?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add tasks with priority levels (Low, Medium, High) with Medium as the default
- **FR-002**: System MUST allow users to add tags (list of strings with length and character restrictions) to tasks: max length of 50 chars, alphanumeric + hyphens/underscores only, max 10 tags per task
- **FR-003**: System MUST allow users to add optional due dates to tasks in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ) with strict validation
- **FR-004**: System MUST provide keyword search functionality that matches title and description fields (OR logic)
- **FR-005**: System MUST provide filtering capabilities by priority, status, and tags
- **FR-006**: System MUST provide sorting functionality by due_date, priority, and title; when sorting by due_date, tasks with null due dates appear last; when sorting by priority, order is High > Medium > Low
- **FR-007**: System MUST maintain backward compatibility with existing tasks that don't have the new fields
- **FR-008**: System MUST display priority levels with color coding (High=Red, Medium=Yellow, Low=Green)
- **FR-009**: System MUST display tags in a dedicated column in the task list
- **FR-010**: System MUST ensure all business logic remains in the core service layer

### Key Entities

- **Task**: Represents a todo item with title, description, status, priority (Low/Medium/High with Medium as default), tags (list of strings: max length 50 chars, alphanumeric + hyphens/underscores only, max 10 tags per task), and optional due_date
- **Priority**: Enum with values Low, Medium, High that determines task importance level (default: Medium); when sorting, order is High > Medium > Low
- **Tag**: String identifier that can be associated with tasks for categorization and filtering (max length 50 chars, alphanumeric + hyphens/underscores only, max 10 tags per task)
- **DueDate**: Optional ISO 8601 format date string (YYYY-MM-DDTHH:MM:SS.sssZ) with strict validation that represents when the task should be completed; when sorting, tasks with null due dates appear last

## Clarifications

### Session 2025-12-23

- Q: What specific ISO date format should be implemented for the due_date field? → A: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ)
- Q: Should there be any validation or restrictions on tag values? → A: Tags should have length limits and character restrictions to prevent abuse and ensure consistency
- Q: What should be the default priority level for new tasks? → A: Default to Medium priority as it's the middle ground that doesn't overstate or understate importance
- Q: How should tasks with null/missing due dates be positioned when sorting by due date? → A: Null due dates should be sorted last (at the end) as these tasks are considered less time-sensitive
- Q: What specific validation rules should apply to tags? → A: Tags should have max length of 50 chars, alphanumeric + hyphens/underscores only, max 10 tags per task
- Q: What should be the priority sort order when sorting by priority? → A: Priority sort order: High > Medium > Low (descending by importance)
- Q: Should search functionality match keywords in title, description, or both? → A: Search matches keywords in both title and description (OR logic)
- Q: How strict should due date validation be? → A: Strict ISO 8601 format validation with clear error messages
- Q: How should CLI commands maintain backward compatibility? → A: Maintain backward compatibility with optional parameters for new features

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add tasks with priority and tags in under 30 seconds
- **SC-002**: Filtering operations return results in under 1 second for up to 1000 tasks
- **SC-003**: 100% of existing Phase I functionality continues to work without degradation
- **SC-004**: Users can successfully filter tasks by priority with 95% accuracy
- **SC-005**: Sorting operations correctly order tasks according to specified criteria 100% of the time
