# ADR 001: Event-Triggered Notification Architecture

## Status
Accepted

## Context
The Time & Automation feature requires a notification system to alert users when tasks are due. We need to decide between two architectural approaches:
- **Event-triggered approach**: Check for due tasks when CLI commands are executed
- **Background daemon approach**: Run a continuous background process to monitor due tasks

## Decision
We will implement an event-triggered notification architecture where the system checks for due tasks each time a CLI command is executed, with an optional background daemon capability.

## Rationale
- **Resource efficiency**: Event-triggered approach minimizes CPU and battery usage
- **Simplicity**: No need to manage background processes
- **Reliability**: No risk of background process failures
- **User-triggered**: Notifications occur when users are actively using the application
- **Performance**: Meets requirements for minimal resource usage as clarified in spec

## Alternatives Considered
1. **Background daemon approach**: Continuous monitoring would provide real-time notifications but consume more resources
2. **Scheduled cron-style checking**: Periodic checks would balance resources but still require background management

## Consequences
### Positive
- Minimal resource usage (CPU, battery)
- Simple architecture with no background process management
- Lower complexity and maintenance
- Meets performance requirements

### Negative
- Notifications only occur when CLI is used (not real-time)
- Users might miss due tasks if they don't use CLI frequently

## Implementation
- Scheduler service will check for due tasks during CLI command execution
- Notification adapter will send system notifications using plyer
- Optional background daemon capability available for real-time notifications if needed