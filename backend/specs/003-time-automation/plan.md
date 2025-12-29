# Implementation Plan: Time & Automation

## 1. Technical Context

**Feature**: Time & Automation with recurring tasks and notification system
**Branch**: 003-time-automation
**Existing Architecture**: Hexagonal architecture with CLI interface, core services, and in-memory storage
**Target**: Implement time-aware capabilities while preserving existing functionality

### 1.1 Current State
- Working todo-app with CLI interface (Typer-based)
- Core service layer with business logic in src/core/todo_service.py
- In-memory repository pattern in src/storage/
- Existing commands: add, complete, list, delete, update
- Rich formatting for UI output

### 1.2 Target State
- Enhanced CLI with recurring task support
- Due date and time reminder system with event-triggered notifications
- Recurring task functionality with proper edge case handling
- "Next 7 Days" view for upcoming deadlines
- System notifications using cross-platform library

### 1.3 Research Findings
- Current CLI uses Typer with commands: add, complete, list, delete, update
- UI/UX patterns use Rich for formatted output with consistent command structure
- Main integration points: src/ui/cli.py (CLI interface), src/core/todo_service.py (business logic)
- New integration points needed: src/core/scheduler.py, src/core/notification_adapter.py

## 2. Required Skills and Agents

### 2.1 Development Skills
- Python 3.13+ with Pydantic, Typer, and Rich
- Date/time manipulation with pendulum or python-dateutil
- Cross-platform notifications with plyer
- CLI interface design with Typer
- Event-driven architecture patterns

### 2.2 Architecture Skills
- Hexagonal architecture implementation
- Dependency injection patterns
- Service layer design
- Repository pattern extensions
- Event-triggered processing design

## 3. Constitution Check

### 3.1 Alignment with Project Principles
- ✅ Maintain hexagonal architecture
- ✅ Preserve existing functionality
- ✅ Add new features through clean interfaces
- ✅ Follow existing code patterns and conventions

### 3.2 Quality Gates
- All new code must pass existing tests
- No breaking changes to existing CLI commands
- Proper error handling for new features
- Performance impact under acceptable thresholds (100ms for due task check, 200ms for 7-day view)
- Resource usage minimized (event-triggered preferred over continuous background processing)

## 4. Phase 0: Research (COMPLETED)

### 4.1 Current CLI Analysis
- ✅ Researched existing CLI command structure (Typer-based with add, complete, list, delete, update)
- ✅ Understood current UI/UX patterns (Rich formatting, consistent command structure)
- ✅ Identified integration points (src/ui/cli.py, src/core/todo_service.py, src/models/todo.py)

### 4.2 Technology Decisions
- **Date/Time Library**: pendulum for robust date/time calculations (handles leap years, time zones)
- **Notifications**: plyer for cross-platform system notifications
- **Scheduler Architecture**: Event-triggered approach (when CLI runs) vs continuous background daemon
- **Security**: Time-based data has same security requirements as other task data (no special encryption needed)

## 5. Phase 1: Design & Implementation

### 5.1 Data Model Extensions
- ✅ Extended Task model with recurrence and due date fields (data-model.md)
- ✅ Maintained backward compatibility with existing tasks
- ✅ Added recurrence_pattern (enum: DAILY, WEEKLY, MONTHLY, NONE)
- ✅ Added due_date (datetime), reminder_sent (bool), next_occurrence_date (datetime)

### 5.2 Service Layer Design
- **Scheduler Service**: Handles recurring task logic and due date checking
- **Notification Adapter**: Cross-platform notification delivery using plyer
- **Event-Triggered Processing**: Check for due/recurring tasks when CLI is invoked

### 5.3 UI/UX Enhancements
- Enhanced CLI commands with new options (--recurrence, --due-date)
- Improved task listing with due date and recurrence indicators
- New "upcoming" command for next 7 days view
- Clear visual indicators for due dates and recurring tasks

## 6. Implementation Strategy

### 6.1 Non-Disruptive Integration
- All new features as optional extensions
- No changes to existing command behavior
- Backward compatibility maintained
- New fields default to values that preserve existing functionality

### 6.2 Incremental Delivery Approach
- **Phase 1**: Data model extensions and basic scheduler foundation
- **Phase 2**: Recurring task creation and completion logic
- **Phase 3**: Notification system implementation
- **Phase 4**: CLI enhancements and upcoming tasks view
- **Phase 5**: Integration and optimization

## 7. Risk Mitigation

### 7.1 Existing Functionality Protection
- Thorough testing approach documented in tasks.md
- Feature integration designed to preserve existing functionality
- Backward compatibility ensured through optional fields

### 7.2 Performance Considerations
- Efficient querying design for due/recurring tasks
- Event-triggered approach implemented (not continuous background processing)
- Performance impact minimized through smart design
- Resource usage constraints: minimal CPU and battery usage preferred

### 7.3 Security & Privacy
- Time-based data has same security requirements as other task data
- No special encryption or access controls needed beyond standard user authentication

## 8. Architecture Design

### 8.1 Component Structure
```
src/
├── core/
│   ├── todo_service.py          # Enhanced with recurring task methods
│   ├── scheduler.py            # New: Handles recurring logic and due date checks
│   └── notification_adapter.py # New: Cross-platform notification delivery
├── models/
│   └── todo.py                 # Enhanced with recurrence fields
└── ui/
    └── cli.py                  # Enhanced with new commands and options
```

### 8.2 Service Dependencies
- TodoService → SchedulerService (for recurring task logic)
- SchedulerService → NotificationAdapter (for sending notifications)
- CLI → TodoService (for all operations, maintaining existing patterns)

### 8.3 Event-Triggered Architecture
- When CLI commands are executed, scheduler checks for due tasks
- No continuous background processing (minimizes resource usage)
- Optional background daemon capability for real-time notifications (if needed)

## 9. Completed Artifacts

The following artifacts have been created as part of this implementation plan:

- **spec.md**: Comprehensive feature specification with all clarifications
- **tasks.md**: Detailed implementation tasks with dependencies
- **plan.md**: This implementation plan document
- **research.md**: Research findings and technology decisions
- **data-model.md**: Detailed data model specification
- **quickstart.md**: Quickstart guide for implementation