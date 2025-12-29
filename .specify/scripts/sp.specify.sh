#!/bin/bash
# sp.specify - Create or update the feature specification from a natural language feature description

# This script creates or updates a feature specification based on user input
# It follows the SDD (Spec-Driven Development) approach

set -e  # Exit on any error

# Get the feature description from command line arguments
FEATURE_DESCRIPTION="$*"

if [ -z "$FEATURE_DESCRIPTION" ]; then
    echo "Usage: sp.specify <feature_description>"
    echo "Example: sp.specify 'User should be able to reset their password via email'"
    exit 1
fi

echo "Creating specification for: $FEATURE_DESCRIPTION"

# Create specs directory if it doesn't exist
mkdir -p specs

# Generate a feature name from the description
FEATURE_NAME=$(echo "$FEATURE_DESCRIPTION" | sed 's/[^a-zA-Z0-9 ]//g' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

# Create a unique feature directory
FEATURE_DIR="specs/${FEATURE_NAME}"

# If directory already exists, append a number
if [ -d "$FEATURE_DIR" ]; then
    counter=1
    while [ -d "${FEATURE_DIR}_${counter}" ]; do
        counter=$((counter + 1))
    done
    FEATURE_DIR="${FEATURE_DIR}_${counter}"
fi

mkdir -p "$FEATURE_DIR"

# Create the main specification file
SPEC_FILE="${FEATURE_DIR}/spec.md"
cat > "$SPEC_FILE" << EOF
# Feature: $FEATURE_DESCRIPTION

## User Stories
- As a user, I can ...

## Acceptance Criteria
### [Specific functionality]
- Given [context]
- When [action]
- Then [expected outcome]

## Technical Requirements
- [List technical requirements]

## API Endpoints
- [List required API endpoints]

## Database Schema
- [List required database changes]

## Error Handling
- [List error scenarios and handling]

## Security Considerations
- [List security requirements]

## Performance Requirements
- [List performance requirements]

## Testing Requirements
- [List testing requirements]

## Dependencies
- [List dependencies on other systems/features]

## Assumptions
- [List any assumptions made]

## Constraints
- [List any constraints or limitations]

## Out of Scope
- [List what is explicitly not included]

## Open Questions
- [List any unresolved questions that need clarification]
EOF

# Create plan file
PLAN_FILE="${FEATURE_DIR}/plan.md"
cat > "$PLAN_FILE" << EOF
# Implementation Plan for: $FEATURE_DESCRIPTION

## Scope and Dependencies
### In Scope
- [List what is included in this feature]

### Out of Scope
- [List what is explicitly excluded]

### External Dependencies
- [List systems/services/teams and ownership]

## Key Decisions and Rationale
### Options Considered
- [List alternative approaches considered]

### Trade-offs
- [List trade-offs for each option]

### Rationale
- [Explain why the chosen approach was selected]

## Interfaces and API Contracts
### Public APIs
- [List inputs, outputs, and errors]

### Versioning Strategy
- [Describe versioning approach]

### Error Taxonomy
- [List error types and status codes]

## Non-Functional Requirements (NFRs) and Budgets
### Performance
- [List performance requirements: p95 latency, throughput, resource caps]

### Reliability
- [List SLOs, error budgets, degradation strategy]

### Security
- [List auth, data handling, secrets, auditing requirements]

### Cost
- [List unit economics]

## Data Management and Migration
### Source of Truth
- [Describe data source]

### Schema Evolution
- [Describe migration strategy]

### Data Retention
- [List retention policies]

## Operational Readiness
### Observability
- [List logs, metrics, traces requirements]

### Alerting
- [List thresholds and on-call owners]

### Runbooks
- [List common tasks]

### Deployment and Rollback
- [List deployment and rollback strategies]

### Feature Flags
- [List compatibility requirements]

## Risk Analysis and Mitigation
### Top 3 Risks
1. [Risk 1, blast radius, kill switches/guardrails]
2. [Risk 2, blast radius, kill switches/guardrails]
3. [Risk 3, blast radius, kill switches/guardrails]

## Evaluation and Validation
### Definition of Done
- [List tests, scans requirements]

### Output Validation
- [List format/requirements/safety checks]
EOF

# Create tasks file
TASKS_FILE="${FEATURE_DIR}/tasks.md"
cat > "$TASKS_FILE" << EOF
# Actionable Tasks for: $FEATURE_DESCRIPTION

## Backend Tasks
- [ ] [Task 1: Backend implementation]
- [ ] [Task 2: Backend implementation]
- [ ] [Task 3: Backend implementation]

## Frontend Tasks
- [ ] [Task 1: Frontend implementation]
- [ ] [Task 2: Frontend implementation]
- [ ] [Task 3: Frontend implementation]

## API Tasks
- [ ] [Task 1: API implementation]
- [ ] [Task 2: API implementation]

## Database Tasks
- [ ] [Task 1: Database schema changes]
- [ ] [Task 2: Database migration]

## Testing Tasks
- [ ] [Task 1: Unit tests]
- [ ] [Task 2: Integration tests]
- [ ] [Task 3: E2E tests]

## Security Tasks
- [ ] [Task 1: Security validation]
- [ ] [Task 2: Security validation]

## Performance Tasks
- [ ] [Task 1: Performance validation]
- [ ] [Task 2: Performance validation]

## Documentation Tasks
- [ ] [Task 1: API documentation]
- [ ] [Task 2: User documentation]

## Validation Tasks
- [ ] [Task 1: Feature validation]
- [ ] [Task 2: Feature validation]
EOF

echo "Specification created successfully!"
echo "Feature: $FEATURE_DESCRIPTION"
echo "Directory: $FEATURE_DIR"
echo ""
echo "Files created:"
echo "- $SPEC_FILE (Main specification)"
echo "- $PLAN_FILE (Implementation plan)"
echo "- $TASKS_FILE (Actionable tasks)"
echo ""
echo "Next steps:"
echo "1. Review and update the specification files"
echo "2. Run 'sp.plan' to generate implementation plan"
echo "3. Run 'sp.tasks' to generate detailed tasks"
echo "4. Run 'sp.implement' to execute the implementation"