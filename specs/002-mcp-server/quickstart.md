# MCP Server Quickstart Guide

## Overview

This guide explains how to set up and use the MCP (Model Context Protocol) server that exposes Spec-Kit Plus commands as MCP prompts in Claude Code.

## Prerequisites

- Python 3.13+
- Claude Code installed and configured
- Required Python packages: `mcp`, `pydantic`, `anyio`

## Setup

1. **Install Dependencies** (if not already installed):
   ```bash
   pip install mcp pydantic anyio
   ```

2. **Verify Configuration**:
   - The `.mcp.json` file should be present in the project root
   - The MCP server configuration should point to the correct server file

3. **Start Claude Code**:
   - Navigate to the project root directory
   - Start Claude Code - the MCP server will automatically connect

## Usage

### Available Commands

All commands from `.claude/commands/` are available as MCP prompts:

- `/sp.specify` - Create or update feature specifications
- `/sp.plan` - Create technical implementation plans
- `/sp.tasks` - Generate task breakdowns
- `/sp.implement` - Execute implementation tasks
- And all other `sp.*` commands

### Example Usage

1. **Create a Specification**:
   ```
   /sp.specify Create a feature to add user authentication
   ```

2. **Generate a Plan**:
   ```
   /sp.plan Create a feature to add user authentication
   ```

3. **Generate Tasks**:
   ```
   /sp.tasks Create a feature to add user authentication
   ```

## Troubleshooting

### Server Not Connecting

- Verify that `.mcp.json` exists and has the correct configuration
- Check that the server file path is correct
- Ensure required Python packages are installed

### Commands Not Working

- Verify that command files exist in `.claude/commands/`
- Check that command files have proper YAML frontmatter
- Ensure the server has read permissions for command files

## Configuration

The server configuration is in `.mcp.json`:

```json
{
  "mcpServers": {
    "spec-kit": {
      "command": "python3",
      "args": [
        "mcp/servers/spec-kit-plus/server.py"
      ],
      "env": {}
    }
  }
}
```

## Architecture

- **Server**: `mcp/servers/spec-kit-plus/server.py` - Main MCP server implementation
- **Commands**: `.claude/commands/` - Source directory for Spec-Kit Plus commands
- **Configuration**: `.mcp.json` - Claude Code MCP configuration
- **Project Structure**: Follows the SDD (Spec-Driven Development) workflow