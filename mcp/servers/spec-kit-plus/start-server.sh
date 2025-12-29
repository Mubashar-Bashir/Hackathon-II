#!/bin/bash
# Script to start the Spec-Kit Plus MCP server

# Change to the project root directory
cd "$(dirname "$0")/../.."

# Start the MCP server
python mcp/servers/spec-kit-plus/server.py