# Makefile for a Python project running on Docker Compose

# Define the Docker Compose file name
COMPOSE_FILE = docker-compose.yml

# Define the Docker Compose project name
PROJECT_NAME = cvparser

# Define the source files
SRC = $(wildcard *.py)


# Define the rule to build the Docker images
build:
	@echo "Building Docker images..."
	@docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) build

# Define the rule to run the Docker containers
run:
	@echo "Running Docker containers..."
	@docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) up -d

# Define the rule to stop the Docker containers
stop:
	@echo "Stopping Docker containers..."
	@docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down

# Define the rule to clean the project
clean:
	@echo "Cleaning project..."
	@docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down --rmi local --volumes

.PHONY: build run stop clean