#!/bin/bash
# Migration rollback script for monorepo migration

set -e

echo "Starting migration rollback..."

# This script would contain logic to restore the original structure
# In a real scenario, this would involve git operations to revert changes
# For now, we'll just document what needs to be done

echo "Rollback steps:"
echo "1. Remove backend/, frontend/, .specify/, .history/ directories"
echo "2. Move files from backend/src back to src/"
echo "3. Move files from backend/tests back to tests/"
echo "4. Move pyproject.toml, uv.lock, README.md back to root"
echo "5. Update git history as needed"

echo "Rollback script completed - please follow manual steps above if needed."