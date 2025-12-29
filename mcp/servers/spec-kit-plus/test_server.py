#!/usr/bin/env python3
"""
Simple MCP Test Server
"""

import asyncio
from mcp.server import Server
from mcp.types import TextContent, Prompt, GetPromptResult, GetPromptRequestParams
from mcp.server.stdio import stdio_server
from typing import List

# Initialize the MCP server
server = Server("test-mcp-server")

@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """List test prompts."""
    return [
        Prompt(
            name="test-prompt",
            title="Test Prompt",
            description="A simple test prompt"
        )
    ]

@server.get_prompt()
async def handle_get_prompt(request: GetPromptRequestParams) -> GetPromptResult:
    """Handle getting a prompt."""
    return GetPromptResult(
        messages=[TextContent(role="user", content=f"Hello from test prompt: {request.name}")]
    )

async def run_server():
    """Run the server using stdio for communication."""
    # Create server capabilities
    from mcp import ServerCapabilities, PromptsCapability
    capabilities = ServerCapabilities(
        prompts=PromptsCapability()
    )

    # Run the server using stdio
    async with stdio_server(server, capabilities) as (read_stream, write_stream):
        await server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=None
        )

if __name__ == "__main__":
    asyncio.run(run_server())