# Phase III Architecture: Layered Dependency Roadmap

## Overview
This document defines the architectural layers for Phase III implementation of the AI-Driven Todo System. Each layer must be completed before the next layer begins implementation.

## Layer Dependencies

### Layer 1 (Database): Conversation and Message Models
**Dependencies**: None (Base dependency)
**Components**:
- SQLModel tables for Conversation and Message
- Database schema extensions to support chat history
- User-scoped conversation storage
- Message history with role tracking (user/assistant)

**Requirements**:
- All database queries must filter by user_id for security
- Conversation and Message tables must be properly related
- Schema must support stateless execution pattern

### Layer 2 (MCP Server): Official MCP SDK Tools
**Dependencies**: Layer 1 (Database models must be functional)
**Components**:
- Official MCP SDK integration
- MCP tools that interface with Layer 1 database
- Task operation tools: add_task, list_tasks, complete_task, delete_task, update_task
- User_id validation in all tools for security

**Requirements**:
- Tools must be stateless and fetch data from DB each time
- All tools must receive user_id to ensure proper scoping
- Tools must use Pydantic V2 for input validation

### Layer 3 (Orchestration): OpenAI Agents SDK
**Dependencies**: Layer 2 (MCP tools must be functional)
**Components**:
- OpenAI Agents SDK integration
- AI logic that uses Layer 2 MCP tools
- Stateless history management using Layer 1 database
- Natural language processing for task operations

**Requirements**:
- Must use MCP tools exclusively for database operations
- Must fetch conversation history from database for each request
- Must maintain context awareness within sessions

### Layer 4 (Frontend): ChatKit UI
**Dependencies**: Layer 3 (AI orchestration must be functional)
**Components**:
- OpenAI ChatKit integration
- UI connected to Layer 3 API
- Conversation interface with message history
- Real-time chat functionality

**Requirements**:
- Must connect to the stateless chat endpoint
- Must maintain conversation continuity
- Must follow Phase II UI design patterns

## Enforcement Rules
1. **No layer shall be implemented until its predecessor is verified and functional**
2. **Claude Code must check architecture.md before starting any sub-task**
3. **After completing each layer, run tests to verify functionality before proceeding**
4. **All implementations must follow the stateless execution pattern**

## Verification Gates
- Layer 1: Database schema creation and relationship verification
- Layer 2: MCP tools functional and accessible
- Layer 3: AI agent can successfully use MCP tools
- Layer 4: Frontend can communicate with backend AI system

## Security Requirements
- All layers must enforce user_id scoping
- No cross-user data access allowed
- JWT authentication required at all layers
- Required API's,url's , security tokens etc should be implemented via .env to make sure dont expose hardcoded.
- before git push verify no secrets, api keys never exposed used through .env 