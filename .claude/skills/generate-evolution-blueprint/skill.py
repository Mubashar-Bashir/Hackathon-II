"""
Generate Evolution Blueprint Skill
Scans the todo-app codebase and generates cloud-ready blueprints including Dockerfile and deployment configurations.
"""

import ast
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class BlueprintGenerator:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.blueprints_dir = self.project_root / "blueprints"
        self.blueprints_dir.mkdir(exist_ok=True)

    def scan_todo_app(self) -> Dict:
        """Scan the todo-app directory to understand its structure and dependencies."""
        scan_results = {
            "dependencies": self._extract_dependencies(),
            "modules": self._scan_modules(),
            "entry_points": self._find_entry_points(),
            "architecture": self._analyze_architecture()
        }
        return scan_results

    def _extract_dependencies(self) -> List[str]:
        """Extract dependencies from pyproject.toml."""
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, 'r') as f:
                content = f.read()

            # Simple parsing of dependencies (in a real implementation, use proper TOML parsing)
            dependencies = []
            if 'dependencies' in content:
                lines = content.split('\n')
                in_deps = False
                for line in lines:
                    if '[project]' in line:
                        in_deps = False
                    if 'dependencies' in line:
                        in_deps = True
                        continue
                    if in_deps and '>=' in line:
                        dep = line.strip().strip(',').strip('"').strip("'")
                        if dep.startswith('"') or dep.startswith("'"):
                            dep = dep[1:-1]
                        if dep:
                            dependencies.append(dep)
            return dependencies
        return []

    def _scan_modules(self) -> List[Dict]:
        """Scan Python modules in the src directory."""
        modules = []
        src_path = self.project_root / "src"

        if src_path.exists():
            for py_file in src_path.rglob("*.py"):
                module_info = {
                    "file": str(py_file.relative_to(self.project_root)),
                    "imports": self._extract_imports(py_file),
                    "classes": self._extract_classes(py_file),
                    "functions": self._extract_functions(py_file)
                }
                modules.append(module_info)

        return modules

    def _extract_imports(self, file_path: Path) -> List[str]:
        """Extract import statements from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)

            imports = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
            return imports
        except:
            return []

    def _extract_classes(self, file_path: Path) -> List[str]:
        """Extract class names from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)

            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
            return classes
        except:
            return []

    def _extract_functions(self, file_path: Path) -> List[str]:
        """Extract function names from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)

            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
            return functions
        except:
            return []

    def _find_entry_points(self) -> List[str]:
        """Find entry points in the application."""
        entry_points = []
        main_path = self.project_root / "src" / "main.py"

        if main_path.exists():
            with open(main_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for main functions and CLI app references
            if 'def main()' in content:
                entry_points.append("main")
            if 'cli_app()' in content:
                entry_points.append("cli_app")
            if 'interactive_main()' in content:
                entry_points.append("interactive_main")

        return entry_points

    def _analyze_architecture(self) -> Dict:
        """Analyze the architecture of the todo-app."""
        architecture = {
            "layers": ["models", "core", "storage", "ui"],
            "patterns": ["hexagonal", "repository"],
            "frameworks": ["pydantic", "typer", "rich"]
        }
        return architecture

    def generate_dockerfile(self) -> str:
        """Generate a Dockerfile for the todo-app."""
        dockerfile_content = """# Multi-stage build for the Todo CLI Application
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \\
    && apt-get install -y --no-install-recommends \\
        build-essential \\
    && rm -rf /var/lib/apt/lists/*

FROM base AS dependencies

# Install Python dependencies
COPY pyproject.toml .
COPY uv.lock* . || true

# Install uv package manager if not available
RUN pip install --upgrade pip \\
    && pip install uv

# Install project dependencies
RUN uv venv --seed --python 3.13 .venv \\
    && . .venv/bin/activate \\
    && uv pip install --system --no-cache-dir -e .

FROM base AS runtime

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv

# Copy application code
COPY . .

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Set permissions
RUN chmod +x /app/src/main.py

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser \\
    && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD python -c "import sys; from src.main import main; print('App is healthy')" || exit 1

# Default command
CMD ["python", "-m", "todo_app.main"]
"""
        return dockerfile_content

    def generate_blueprint_yaml(self, scan_results: Dict) -> str:
        """Generate a blueprint.yaml with cloud deployment configuration."""
        blueprint = {
            "apiVersion": "v1",
            "kind": "CloudBlueprint",
            "metadata": {
                "name": "todo-app-blueprint",
                "version": "0.1.0",
                "description": "Cloud-ready blueprint for the Todo CLI application"
            },
            "spec": {
                "application": {
                    "name": "todo-app",
                    "type": "cli",
                    "language": "python",
                    "version": "3.13",
                    "architecture": "hexagonal",
                    "patterns": scan_results.get("architecture", {}).get("patterns", [])
                },
                "container": {
                    "baseImage": "python:3.13-slim",
                    "port": None,  # CLI app doesn't expose ports
                    "healthCheck": {
                        "command": ["python", "-c", "import sys; from src.main import main; print('App is healthy')"],
                        "interval": 30,
                        "timeout": 3
                    },
                    "security": {
                        "runAsNonRoot": True,
                        "readOnlyRootFilesystem": False,
                        "allowPrivilegeEscalation": False
                    }
                },
                "dependencies": {
                    "python": scan_results.get("dependencies", [])
                },
                "deployment": {
                    "environments": ["development", "staging", "production"],
                    "strategy": "rolling",
                    "replicas": 1  # CLI app, typically single instance
                },
                "storage": {
                    "type": "ephemeral",  # CLI uses in-memory storage for now
                    "persistence": False,
                    "backup": False
                },
                "monitoring": {
                    "logging": {
                        "level": "INFO",
                        "format": "json"
                    },
                    "metrics": False
                },
                "evolutionPath": {
                    "phase1": "CLI application (current)",
                    "phase2": "Web API with REST endpoints",
                    "phase3": "Microservices architecture",
                    "phase4": "Cloud-native with event-driven architecture"
                }
            }
        }
        return yaml.dump(blueprint, default_flow_style=False, indent=2)

    def generate_docker_compose(self) -> str:
        """Generate a docker-compose.yml for multi-container setup."""
        compose_content = """version: '3.8'

services:
  todo-app:
    build:
      context: .
      dockerfile: blueprints/Dockerfile
    container_name: todo-app-cli
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONDONTWRITEBYTECODE=1
    volumes:
      - .:/app
      - todo-data:/app/data  # For future persistent storage
    networks:
      - todo-network
    security_opt:
      - no-new-privileges:true
    read_only: false  # CLI app may need write access for temp files
    tmpfs:
      - /tmp

volumes:
  todo-data:
    driver: local

networks:
  todo-network:
    driver: bridge
"""
        return compose_content

    def generate_k8s_manifests(self):
        """Generate Kubernetes deployment manifests."""
        k8s_dir = self.blueprints_dir / "k8s"
        k8s_dir.mkdir(exist_ok=True)

        # Deployment manifest
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "todo-app-cli",
                "labels": {
                    "app": "todo-app-cli"
                }
            },
            "spec": {
                "replicas": 1,
                "selector": {
                    "matchLabels": {
                        "app": "todo-app-cli"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "todo-app-cli"
                        }
                    },
                    "spec": {
                        "securityContext": {
                            "runAsNonRoot": True,
                            "runAsUser": 1000,
                            "fsGroup": 2000
                        },
                        "containers": [
                            {
                                "name": "todo-app",
                                "image": "todo-app:latest",
                                "imagePullPolicy": "Never",
                                "securityContext": {
                                    "allowPrivilegeEscalation": False,
                                    "readOnlyRootFilesystem": False,
                                    "runAsNonRoot": True,
                                    "runAsUser": 1000
                                },
                                "resources": {
                                    "requests": {
                                        "memory": "128Mi",
                                        "cpu": "100m"
                                    },
                                    "limits": {
                                        "memory": "256Mi",
                                        "cpu": "500m"
                                    }
                                },
                                "livenessProbe": {
                                    "exec": {
                                        "command": ["python", "-c", "import sys; from src.main import main; print('App is healthy')"]
                                    },
                                    "initialDelaySeconds": 30,
                                    "periodSeconds": 30
                                }
                            }
                        ]
                    }
                }
            }
        }

        with open(k8s_dir / "deployment.yaml", 'w') as f:
            yaml.dump(deployment, f, default_flow_style=False, indent=2)

    def generate_terraform_configs(self):
        """Generate Terraform configuration for infrastructure as code."""
        terraform_dir = self.blueprints_dir / "terraform"
        terraform_dir.mkdir(exist_ok=True)

        # Main Terraform configuration
        main_tf = """# Terraform configuration for Todo App Infrastructure
terraform {
  required_version = ">= 1.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = ">= 2.22.0"
    }
  }
}

# Configure the Docker provider
provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Create a network for the todo app
resource "docker_network" "todo_network" {
  name     = "todo-app-network"
  driver   = "bridge"
}

# Build and run the todo app container
resource "docker_image" "todo_app" {
  name         = "todo-app:latest"
  keep_locally = true
}

resource "docker_container" "todo_app" {
  name  = "todo-app-cli"
  image = docker_image.todo_app.name

  networks_advanced {
    name = docker_network.todo_network.name
  }

  # Security configurations
  user = "1000:1000"
  security_opts = [
    "no-new-privileges:true"
  ]

  # Health check
  healthcheck {
    test         = ["CMD", "python", "-c", "import sys; from src.main import main; print('App is healthy')"]
    interval     = "30s"
    timeout      = "3s"
    start_period = "5s"
    retries      = 3
  }

  depends_on = [
    docker_network.todo_network
  ]
}

output "container_id" {
  value = docker_container.todo_app.id
}

output "network_name" {
  value = docker_network.todo_network.name
}
"""

        with open(terraform_dir / "main.tf", 'w') as f:
            f.write(main_tf)

    def generate_all_blueprints(self):
        """Generate all blueprint files."""
        print("🔍 Scanning todo-app for blueprint generation...")
        scan_results = self.scan_todo_app()

        print("📄 Generating Dockerfile...")
        dockerfile_content = self.generate_dockerfile()
        with open(self.blueprints_dir / "Dockerfile", 'w') as f:
            f.write(dockerfile_content)

        print("📄 Generating blueprint.yaml...")
        blueprint_content = self.generate_blueprint_yaml(scan_results)
        with open(self.blueprints_dir / "blueprint.yaml", 'w') as f:
            f.write(blueprint_content)

        print("📄 Generating docker-compose.yml...")
        compose_content = self.generate_docker_compose()
        with open(self.blueprints_dir / "docker-compose.yml", 'w') as f:
            f.write(compose_content)

        print("📄 Generating Kubernetes manifests...")
        self.generate_k8s_manifests()

        print("📄 Generating Terraform configurations...")
        self.generate_terraform_configs()

        print(f"✅ Blueprints generated successfully in {self.blueprints_dir}/")
        print("📁 Generated files:")
        print("   - Dockerfile")
        print("   - blueprint.yaml")
        print("   - docker-compose.yml")
        print("   - k8s/deployment.yaml")
        print("   - terraform/main.tf")

        return str(self.blueprints_dir)


def run_skill(args: Optional[List[str]] = None) -> str:
    """Main function to run the Generate Evolution Blueprint skill."""
    project_root = args[0] if args and len(args) > 0 else "."

    generator = BlueprintGenerator(project_root)

    try:
        blueprints_path = generator.generate_all_blueprints()
        return f"Blueprint generation completed successfully. Files created in: {blueprints_path}"
    except Exception as e:
        return f"Error generating blueprints: {str(e)}"


if __name__ == "__main__":
    import sys
    args = sys.argv[1:] if len(sys.argv) > 1 else None
    print(run_skill(args))