# Reusable Intelligence Skills for Todo App Implementation

This document outlines the specialized Claude Code skills created for implementing the todo app with Next.js frontend, FastAPI backend, SQLModel database, and Better Auth authentication.

## Available Skills

### 1. nextjs-frontend
**Purpose**: Comprehensive Next.js 16+ application development with App Router, responsive UI, and Better Auth integration
**Use Cases**:
- Creating Next.js pages and components
- Implementing responsive UI with Tailwind CSS
- Setting up Better Auth integration
- Creating API routes in Next.js

### 2. fastapi-backend
**Purpose**: FastAPI backend development with Pydantic V2, SQLModel ORM, and authentication middleware
**Use Cases**:
- Creating RESTful API endpoints
- Implementing request/response validation
- Adding authentication and authorization
- Building service layer for business logic

### 3. sqlmodel-db
**Purpose**: SQLModel ORM development with Neon PostgreSQL integration
**Use Cases**:
- Creating database models with relationships
- Implementing CRUD operations
- Managing database connections and sessions
- Handling schema migrations

### 4. better-auth
**Purpose**: Better Auth implementation for user authentication and session management
**Use Cases**:
- Setting up authentication systems
- Integrating with frontend applications
- Implementing JWT-based sessions
- Managing user data and profiles

### 5. sqlmodel-db-expert
**Purpose**: Expert in creating and managing SQLModel database models with proper relationships, validation, and security patterns
**Use Cases**:
- Creating SQLModel database tables with proper relationships
- Implementing validation rules and constraints
- Setting up foreign key relationships and cascade operations
- Designing secure models with user isolation patterns
- Creating Pydantic schemas for API operations

### 6. security-model-designer
**Purpose**: Expert in designing secure database models and API endpoints with proper user isolation, authentication, and authorization patterns
**Use Cases**:
- Implementing user_id scoping and filtering
- Designing secure foreign key relationships
- Creating authentication and authorization patterns
- Implementing JWT-based security flows
- Ensuring cross-user data isolation

### 7. conversation-history-manager
**Purpose**: Expert in designing and implementing conversation and message storage systems with proper relationships, role tracking, and history management
**Use Cases**:
- Creating conversation and message models with proper relationships
- Implementing role tracking (user/assistant) systems
- Designing message history and retrieval patterns
- Setting up conversation threading and organization
- Managing conversation metadata and timestamps

### 8. api-endpoint-designer
**Purpose**: Expert in designing secure and efficient API endpoints with proper authentication, validation, and response patterns
**Use Cases**:
- Creating secure API endpoints with authentication
- Implementing proper request/response validation
- Designing endpoint patterns with user isolation
- Creating RESTful API designs with proper HTTP status codes
- Implementing API security patterns

## MCP Integration

These skills are designed to work with Model Context Protocol (MCP) servers to provide reusable intelligence during the implementation phase. Each skill contains:

- **SKILL.md**: Detailed documentation and usage instructions
- **Scripts**: Executable tools for common tasks
- **References**: In-depth documentation for complex topics
- **Assets**: Templates and boilerplate code

## Implementation Workflow

During `/sp.implement`, these skills will be automatically available and can be invoked when:

1. Creating new components or pages
2. Generating API endpoints
3. Setting up database models
4. Implementing authentication features
5. Performing common development tasks
6. Designing secure systems with user isolation
7. Creating conversation and message systems
8. Implementing security patterns across any layer

The skills follow the Reusable Intelligence principle by providing specialized, context-aware assistance that can be invoked on-demand during the implementation process, making the development more efficient and consistent.