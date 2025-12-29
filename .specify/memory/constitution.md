# Project Constitution

## Purpose
This constitution defines the core principles, constraints, and values that govern the Evolution of Todo project. All development activities must align with these principles.

## Core Values
- **Spec-Driven Development**: All features must be specified before implementation
- **Deterministic Development**: Clear, predictable development process
- **Quality First**: Maintain high code quality and comprehensive testing
- **User-Centric**: Prioritize user value and experience in all decisions

## Architecture Principles
- **Modularity**: Components should be loosely coupled and highly cohesive
- **Testability**: All code must be testable with clear unit and integration tests
- **Maintainability**: Code should be readable, documented, and follow consistent patterns
- **Performance**: Optimize for responsive user experience
- **Security**: Follow security best practices and validate all inputs

## Technology Constraints
- **Python 3.13+**: Use only Python 3.13+ features and libraries
- **CLI-First**: Maintain command-line interface as primary interface
- **Cross-Platform**: Ensure compatibility across major operating systems
- **Dependency Management**: Use uv for package management
- **Type Safety**: Use Pydantic V2 for data validation and typing

## Development Process
- **Specification First**: Use `/sp.specify` to define features before implementation
- **Planning Required**: Use `/sp.plan` to design architecture before coding
- **Task Breakdown**: Use `/sp.tasks` to create atomic, testable tasks
- **Implementation**: Use `/sp.implement` to execute tasks systematically
- **No Code Without Tasks**: Never write code without a corresponding task

## Quality Standards
- **Testing**: All features must include unit tests with >80% coverage
- **Documentation**: All public interfaces must be documented
- **Code Review**: All changes must be reviewed before merging
- **Validation**: Specifications must be validated before implementation
- **Error Handling**: All error paths must be explicitly handled

## Project Scope
- **Phase I**: CLI-based todo application with time automation features
- **Phase II**: API layer with SQL persistence and web interface
- **Phase III**: Enhanced web interface and advanced features (future consideration)

## Phase-II Specific Rules
### Monorepo Structure
- **Directory Governance**: Establish monorepo structure with backend/ and frontend/ directories
- **No Cross-Directory Imports**: Frontend cannot import directly from backend and vice versa
- **Environment Isolation**: Treat frontend/ as TypeScript/Next.js environment and backend/ as Python/FastAPI environment

### Storage and Authentication
- **SQLModel + Neon**: SQLModel with Neon PostgreSQL as the primary storage layer for Phase II
- **JWT Verification**: Better Auth JWT verification required for all API routes
- **User Data Isolation**: All DB queries MUST filter by authenticated user_id
- **Secret Synchronization**: BETTER_AUTH_SECRET must be identical in both frontend/.env and backend/.env

### Technical Stack Standards
- **Backend Framework**: FastAPI with Pydantic V2 validation for all API inputs
- **Frontend Framework**: Next.js 16 App Router as the standard
- **Styling**: Tailwind CSS for consistent styling
- **Authentication**: Better Auth with JWT plugin enabled

### Security Enforcement
- **Zero-Trust API**: No endpoint shall return data without valid Authorization: Bearer <token> header verification
- **Mandatory Isolation**: Every database query MUST include a user_id filter derived from the JWT
- **API Security**: All routes must implement proper authentication and authorization checks

### Development Workflow
- **Traceability**: Every Pull Request or code change must reference a .tasks entry from specs/ directory
- **Spec-Kit Plus Compliance**: Maintain traceability between specifications, tasks, and implementation
- **No Manual Edits**: Any manual change to code without corresponding task is a violation of agentic development protocol

## Non-Negotiables
- All development follows the Spec-Kit Plus workflow: Specify → Plan → Tasks → Implement
- No feature creep without proper specification
- Maintain backward compatibility where possible
- Follow Python best practices and PEP standards
- Use structured logging for observability
