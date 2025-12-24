# Terraform configuration for Todo App Infrastructure
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
