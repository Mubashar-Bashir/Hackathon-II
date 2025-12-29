# ADR 003: Date/Time and Notification Technology Stack

## Status
Accepted

## Context
The Time & Automation feature requires robust date/time handling for recurring tasks and cross-platform notifications for due date alerts. We need to select appropriate libraries for these capabilities.

## Decision
We will use pendulum for date/time calculations and plyer for cross-platform notifications.

## Rationale
### For Date/Time (pendulum):
- **Robust date arithmetic**: Handles complex calculations needed for recurring tasks
- **Leap year support**: Built-in handling of leap years and month-end edge cases
- **Intuitive API**: Easier to use than standard datetime or dateutil
- **Timezone support**: Comprehensive timezone handling if needed in future

### For Notifications (plyer):
- **Cross-platform compatibility**: Works across Windows, Mac, and Linux
- **Simple integration**: Easy to integrate with CLI applications
- **System-level notifications**: Provides desktop popups as preferred in spec
- **Minimal dependencies**: Lightweight solution

## Alternatives Considered
### Date/Time alternatives:
1. **python-dateutil**: Good functionality but less intuitive API
2. **arrow**: Alternative but less comprehensive than pendulum
3. **Standard datetime**: Basic functionality insufficient for complex date calculations

### Notification alternatives:
1. **Platform-specific solutions**: Would require separate implementations for each OS
2. **plygui**: More complex than needed for simple notifications
3. **Custom platform-specific implementations**: Would increase complexity significantly

## Consequences
### Positive
- Reliable date calculations with built-in edge case handling
- Consistent notification experience across platforms
- Well-maintained, popular libraries with good community support
- Meets performance and compatibility requirements

### Negative
- Additional dependencies to manage
- Potential version compatibility issues in future
- Notification appearance varies slightly across platforms

## Implementation
- Install pendulum and plyer dependencies
- Use pendulum for all date/time calculations in scheduler service
- Use plyer for all system notifications in notification adapter
- Handle graceful degradation if notifications unavailable