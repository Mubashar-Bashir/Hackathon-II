# Tasks: MCP Server for Spec-Kit Plus Commands

**Feature**: 002-mcp-server
**Generated**: 2025-12-25
**Status**: Draft
**Input**: Feature specification and implementation plan

## Overview

This task breakdown implements the MCP server that exposes Spec-Kit Plus commands in `.claude/commands` as MCP prompts, enabling Claude Code integration with the complete SDD workflow.

## Dependencies

- User Story 1 (P1) must complete before User Story 2 (P2)
- User Story 2 (P2) must complete before User Story 3 (P3)

## Implementation Strategy

**MVP Scope**: User Story 1 - Basic MCP server that discovers and exposes commands from `.claude/commands`
**Delivery**: Incremental delivery with each user story as a complete, independently testable increment

## Parallel Execution Examples

- Server implementation and configuration can be developed in parallel with different team members
- Unit tests can be written in parallel with implementation tasks

---

## Phase 1: Setup

**Goal**: Initialize project structure and dependencies for the MCP server

- [X] T001 Create mcp server directory structure at `mcp/servers/spec-kit-plus/`
- [X] T002 Install required dependencies (`mcp`, `pydantic`, `anyio`) using uv
- [X] T003 Create basic server.py file with MCP server skeleton

## Phase 2: Foundational

**Goal**: Implement core MCP server infrastructure and basic functionality

- [X] T004 [P] Implement MCP server initialization with proper imports
- [X] T005 [P] Create list_prompts function to discover command files from `.claude/commands`
- [X] T006 [P] Create get_prompt function to retrieve command details
- [X] T007 Implement proper error handling for missing command files
- [X] T008 Set up server communication via stdio using MCP protocol
- [X] T009 [P] Add logging for server operations and errors

## Phase 3: User Story 1 - Access Spec-Kit Commands via MCP (Priority: P1)

**Goal**: Enable Claude Code to access Spec-Kit Plus commands through MCP prompts

**Independent Test**: Claude Code can start with MCP server configured and successfully execute a basic command like `/sp.specify`

- [X] T010 [US1] Implement command discovery to load all files from `.claude/commands`
- [X] T011 [US1] Create proper command name extraction from filename (e.g., `sp.specify.md` → `sp.specify`)
- [X] T012 [US1] Format command titles appropriately (e.g., "Spec-Kit Plus: Specify")
- [X] T013 [US1] Implement list_prompts endpoint to return all discovered commands
- [X] T014 [US1] Test basic command listing functionality
- [X] T015 [US1] Implement basic get_prompt functionality for command details
- [X] T016 [US1] Test successful command execution through MCP interface

## Phase 4: User Story 2 - Command Metadata Discovery (Priority: P2)

**Goal**: Provide clear descriptions and usage information for each Spec-Kit Plus command

**Independent Test**: Command descriptions are properly extracted from YAML frontmatter and displayed in Claude Code

- [X] T017 [US2] Implement YAML frontmatter parsing to extract command descriptions
- [X] T018 [US2] Extract description field from YAML frontmatter of each command file
- [X] T019 [US2] Return description in prompt metadata when requested
- [X] T020 [US2] Implement fallback to default description when no description in frontmatter
- [X] T021 [US2] Test description extraction for commands with YAML frontmatter
- [X] T022 [US2] Test fallback behavior for commands without descriptions

## Phase 5: User Story 3 - Error Handling for Missing Commands (Priority: P3)

**Goal**: Handle missing or invalid commands gracefully to maintain server stability

**Independent Test**: Requesting a non-existent command returns clear error message

- [X] T023 [US3] Implement validation for requested command existence
- [X] T024 [US3] Return appropriate error message when command file doesn't exist
- [X] T025 [US3] Handle malformed YAML frontmatter gracefully
- [X] T026 [US3] Test error handling for non-existent command requests
- [X] T027 [US3] Test server stability when command files have invalid content
- [X] T028 [US3] Verify server continues operating despite individual command failures

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Complete implementation with configuration, testing, and documentation

- [X] T029 Create `.mcp.json` configuration file to register server with Claude Code
- [X] T030 Test MCP server integration with Claude Code
- [X] T031 [P] Add performance monitoring to ensure <1 second response time
- [X] T032 [P] Optimize server startup time to be under 5 seconds
- [X] T033 Add comprehensive error logging and debugging capabilities
- [X] T034 Update AGENTS.md to document the MCP server usage
- [X] T035 [P] Create quickstart guide for MCP server setup and usage
- [X] T036 Verify 100% of commands in `.claude/commands` are accessible via MCP prompts