#!/bin/bash
# Spec-Kit Plus MCP Server wrapper
# This script provides a simple interface to run Spec-Kit Plus commands

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMMANDS_DIR="$PROJECT_ROOT/.claude/commands"

if [ "$1" = "list-prompts" ]; then
    # List all available commands
    for cmd_file in "$COMMANDS_DIR"/sp.*.md; do
        if [ -f "$cmd_file" ]; then
            cmd_name=$(basename "$cmd_file" .md)
            title=$(grep -E "^description:" "$cmd_file" | head -1 | cut -d: -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sed 's/^"//;s/"$//' | sed "s/^/'/;s/$/'/")
            if [ -z "$title" ]; then
                title="Spec-Kit Plus command: $cmd_name"
            fi
            echo "{\"name\":\"$cmd_name\",\"title\":\"${cmd_name//sp./Spec-Kit Plus: }\",\"description\":\"$title\"}"
        fi
    done
elif [ "$1" = "get-prompt" ] && [ -n "$2" ]; then
    # Get a specific command
    cmd_name="$2"
    cmd_file="$COMMANDS_DIR/$cmd_name.md"

    if [ -f "$cmd_file" ]; then
        description=$(grep -E "^description:" "$cmd_file" | head -1 | cut -d: -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sed 's/^"//;s/"$//')
        if [ -z "$description" ]; then
            description="Spec-Kit Plus command"
        fi

        # Extract content after the YAML frontmatter
        content=$(sed -n '/^---$/,/^---$/{/^---$/!p;}' "$cmd_file" | sed 's/"/\\"/g' | tr '\n' ' ')

        echo "{\"messages\":[{\"role\":\"user\",\"content\":\"## $cmd_name\\n\\n**Description:** $description\\n\\n**Command Usage:** You can run this command using /sp.${cmd_name//sp./}\\n\\n**Details:** $content\"}]}"
    else
        echo "{\"messages\":[{\"role\":\"user\",\"content\":\"Command $cmd_name not found\"}]}"
    fi
else
    echo "Usage: $0 {list-prompts|get-prompt <command-name>}" >&2
    exit 1
fi