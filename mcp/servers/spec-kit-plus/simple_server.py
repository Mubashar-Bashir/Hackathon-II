#!/usr/bin/env python3
"""
Simple Spec-Kit Plus MCP Server
"""

import asyncio
from mcp.server import Server
from mcp.types import TextContent, Prompt, GetPromptResult, GetPromptRequestParams
from mcp import ServerCapabilities, PromptsCapability
from typing import List

# Initialize the MCP server
server = Server("spec-kit-plus-mcp")


@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """List all available Spec-Kit Plus commands as MCP prompts."""
    import os
    from pathlib import Path

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
    import os
    from pathlib import Path

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


async def run_server():
    """Run the server using the built-in run_stdio_server method."""
    from mcp.server.stdio import run_stdio_server

    # Create server capabilities
    capabilities = ServerCapabilities(
        prompts=PromptsCapability()
    )

    # Run the server using stdio
    await run_stdio_server(
        server,
        capabilities
    )


if __name__ == "__main__":
    asyncio.run(run_server())