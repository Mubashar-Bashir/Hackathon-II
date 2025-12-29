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

The skills follow the Reusable Intelligence principle by providing specialized, context-aware assistance that can be invoked on-demand during the implementation process, making the development more efficient and consistent.