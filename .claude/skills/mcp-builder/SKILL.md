---
name: mcp-builder
description: Creates and configures Model Context Protocol (MCP) servers for Spec-Kit Plus commands. Use when setting up MCP integration to make Spec-Kit Plus commands (like /sp.specify, /sp.plan, /sp.tasks, /sp.implement) available as MCP prompts in Claude Code.
---

# MCP Builder

## Overview

The MCP Builder skill helps create Model Context Protocol (MCP) servers that expose Spec-Kit Plus commands as MCP prompts. This enables Claude Code to access the complete Spec-Kit Plus workflow (Specify → Plan → Tasks → Implement) through MCP integration.

## Core Capabilities

### 1. Create MCP Server Implementation

Builds a Python-based MCP server that can load and serve all commands from the `.claude/commands` directory as MCP prompts.

**Implementation:**
- Creates a server using the `mcp` library
- Implements `list_prompts()` to discover all available commands
- Implements `get_prompt()` to retrieve command details and usage
- Reads command definitions from `.claude/commands/*.md` files
- Extracts descriptions from YAML frontmatter

### 2. Generate MCP Configuration

Creates the `.mcp.json` configuration file needed to register the server with Claude Code.

**Configuration includes:**
- Server name and identification
- Command execution details
- Environment settings
- Path to the server implementation

### 3. Validate MCP Server Setup

Ensures the MCP server can be properly launched and integrated with Claude Code.

**Validation steps:**
- Check that required dependencies are installed
- Verify server can be started without errors
- Confirm commands are properly loaded from `.claude/commands`

## MCP Server Implementation

The MCP server should be implemented as follows:

```python
#!/usr/bin/env python3
"""
Spec-Kit Plus MCP Server
"""

import asyncio
import anyio
from mcp.server import Server
from mcp.types import TextContent, Prompt, GetPromptResult, GetPromptRequestParams
from mcp import ServerCapabilities, PromptsCapability
from mcp.server.stdio import stdio_server
from pathlib import Path
from typing import List

# Initialize the MCP server
server = Server("spec-kit-plus-mcp")

@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """List all available Spec-Kit Plus commands as MCP prompts."""
    prompts = []
    commands_dir = Path(".claude/commands")

    if commands_dir.exists():
        for cmd_file in commands_dir.glob("*.md"):
            cmd_name = cmd_file.stem
            cmd_title = cmd_name.replace("sp.", "Spec-Kit Plus: ").replace("_", " ").title()

            # Read the command description from the file
            description = "Spec-Kit Plus command"
            try:
                content = cmd_file.read_text()
                # Extract description from YAML frontmatter if available
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip() == '---' and i > 0:
                        # Found the end of frontmatter, break
                        break
                    if line.startswith('description:'):
                        description = line.split(':', 1)[1].strip().strip('"').strip("'")
                        break
            except Exception:
                pass

            prompts.append(
                Prompt(
                    name=cmd_name,
                    title=cmd_title,
                    description=description,
                )
            )

    return prompts

@server.get_prompt()
async def handle_get_prompt(request: GetPromptRequestParams) -> GetPromptResult:
    """Execute a Spec-Kit Plus command and return the result."""
    cmd_name = request.name

    # Validate that the command exists
    cmd_file = Path(f".claude/commands/{cmd_name}.md")
    if not cmd_file.exists():
        return GetPromptResult(
            messages=[TextContent(role="user", content=f"Command {cmd_name} not found")]
        )

    try:
        content = cmd_file.read_text()

        # Extract the description from frontmatter
        description = "No description available"
        lines = content.split('\n')
        in_frontmatter = False
        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter and line.startswith('description:'):
                description = line.split(':', 1)[1].strip().strip('"').strip("'")

        # Extract the main prompt content (after frontmatter)
        main_content = []
        in_frontmatter = False
        skip_to_main = False
        for line in lines:
            if line.strip() == '---' and not in_frontmatter:
                in_frontmatter = True
                continue
            elif line.strip() == '---' and in_frontmatter:
                in_frontmatter = False
                skip_to_main = True
                continue

            if not in_frontmatter and skip_to_main:
                main_content.append(line)

        # Join the main content, removing leading empty lines
        main_content = '\n'.join(main_content).strip()

        response = f"## {cmd_name}\n\n"
        response += f"**Description:** {description}\n\n"
        response += f"**Command Usage:** You can run this command using `/sp.{cmd_name.replace('sp.', '')}`\n\n"
        response += f"**Details:**\n{main_content[:1000]}..." if len(main_content) > 1000 else f"**Details:**\n{main_content}"

        return GetPromptResult(
            messages=[TextContent(role="user", content=response)]
        )
    except Exception as e:
        return GetPromptResult(
            messages=[TextContent(role="user", content=f"Error reading command {cmd_name}: {str(e)}")]
        )

def main():
    """Main entry point for the MCP server."""
    capabilities = ServerCapabilities(
        prompts=PromptsCapability()
    )

    async def run():
        async with stdio_server(server, capabilities) as (read_stream, write_stream):
            await server.run(
                read_stream=read_stream,
                write_stream=write_stream,
                initialization_options=None
            )

    anyio.run(run)

if __name__ == "__main__":
    main()
```

## MCP Configuration

The `.mcp.json` file should be configured as follows:

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

## Usage

1. Create the server implementation file at `mcp/servers/spec-kit-plus/server.py`
2. Create the configuration file at `.mcp.json` in the project root
3. Ensure all Spec-Kit Plus command files exist in `.claude/commands/`
4. Start Claude Code in the project directory to automatically load the MCP server
5. Use commands like `/sp.specify`, `/sp.plan`, `/sp.tasks`, `/sp.implement` as MCP prompts
