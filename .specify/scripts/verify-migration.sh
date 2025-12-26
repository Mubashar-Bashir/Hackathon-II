#!/bin/bash
# Migration verification script for monorepo migration

set -e

echo "Running migration verification..."

# Check that backend directory exists and has expected structure
if [ ! -d "backend/src" ]; then
    echo "ERROR: backend/src directory not found"
    exit 1
fi

if [ ! -d "backend/tests" ]; then
    echo "ERROR: backend/tests directory not found"
    exit 1
fi

if [ ! -f "backend/pyproject.toml" ]; then
    echo "ERROR: backend/pyproject.toml not found"
    exit 1
fi

# Check that todo application files exist in backend
if [ ! -f "backend/src/main.py" ]; then
    echo "ERROR: backend/src/main.py not found"
    exit 1
fi

# Run tests from backend directory to verify functionality
echo "Running tests from backend directory..."
cd backend
if python -m pytest tests/ -v; then
    echo "All tests passed!"
else
    echo "ERROR: Tests failed"
    exit 1
fi

# Test that the application can run
echo "Testing application execution..."
if python -m src.main --help; then
    echo "Application help command works!"
else
    echo "ERROR: Application execution failed"
    exit 1
fi

cd ..
echo "Migration verification completed successfully!"