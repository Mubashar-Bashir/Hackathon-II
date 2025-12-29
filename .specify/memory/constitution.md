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
- **Python 3.12+**: Use Python 3.12+ features and libraries (updated from 3.13+ requirement to match current environment)
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
- **Phase III**: AI-powered chatbot interface with MCP server architecture and OpenAI Agents SDK

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

## Phase-III Specific Rules: AI-Agentic & MCP Governance Protocol

### Architectural Sovereignty (The Stateless Rule)
- **Zero-Memory Backend**: The FastAPI server must remain 100% stateless. It is forbidden to store conversation context in global variables or local cache.
- **History Rehydration**: Every request to `/api/chat` must begin by querying the `Message` table in the Neon DB to rebuild the conversation thread.

### MCP Protocol Enforcement
- **Tool Isolation**: The AI Agent must interact with the Todo database **exclusively** through the Official MCP SDK tools.
- **No Direct DB Access**: Claude Code must not write SQL queries inside the Chatbot logic; it must call the defined tools (`add_task`, `list_tasks`, etc.).
- **Schema Strictness**: All MCP tools must use Pydantic V2 for input validation. Any tool call with missing or extra parameters must be rejected.

### Security & Identity Locking
- **User-ID Propagation**: The `user_id` from the Better Auth JWT must be injected into every MCP tool call.
- **Privacy Guardrail**: The system must verify that a user can only access `Conversation` and `Task` records where `owner_id == current_user_id`.

### Agentic Workflow (Spec-Kit Plus)
- **Spec-First Implementation**: No code can be generated without a corresponding `.md` file in the `/specs` directory.
- **Traceability**: Every commit or implementation task must reference the specific Layer (P1-P5) defined in `specs/architecture.md`.

### UI/UX & Interaction Standards
- **Confirmation Handshake**: For destructive actions (Delete/Clear), the AI Agent must ask for user confirmation before executing the tool.
- **ChatKit Integration**: Use OpenAI ChatKit for the frontend. Theme must follow the Phase-II 'Bright Neon' Glassmorphism style.
- **Language Support**: Ensure the Agent handles natural language processing correctly (via OpenAI model capabilities).

## Non-Negotiables
- All development follows the Spec-Kit Plus workflow: Specify → Plan → Tasks → Implement
- No feature creep without proper specification
- Maintain backward compatibility where possible
- Follow Python best practices and PEP standards
- Use structured logging for observability
