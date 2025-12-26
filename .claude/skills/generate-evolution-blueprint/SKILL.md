---
name: generate-evolution-blueprint
description: Scans the todo-app codebase and generates cloud-ready blueprints including Dockerfile and deployment configurations for future evolution to cloud-native architecture.
---

# Generate Evolution Blueprint Skill

This skill scans your todo-app source code and generates cloud-ready blueprints that demonstrate your code is "Cloud-Ready" from day one. It creates Dockerfiles, deployment configurations, and infrastructure as code templates to support evolution from Phase I (Python CLI) to future cloud-native phases.

## When to Use This Skill

Use when you want to:
1. Generate cloud deployment blueprints for your todo-app
2. Create Dockerfile and containerization configurations
3. Generate infrastructure as code templates for future phases
4. Demonstrate cloud-readiness of your current Phase I implementation

## Files Generated

This skill will generate:
- `blueprints/Dockerfile` - Containerization blueprint
- `blueprints/blueprint.yaml` - Cloud deployment configuration
- `blueprints/docker-compose.yml` - Multi-container configuration
- `blueprints/k8s/` - Kubernetes deployment manifests
- `blueprints/terraform/` - Infrastructure as code templates

## Implementation

The skill will:
1. Scan the `todo-app/src/` directory structure
2. Analyze dependencies from `pyproject.toml`
3. Generate appropriate cloud deployment configurations
4. Create the blueprints in a dedicated folder