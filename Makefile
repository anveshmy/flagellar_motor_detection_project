#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = flagellar_motor_detection_project
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python
DOCKER_IMAGE_NAME = flagellar-motor-detection
DOCKER_RUN_FLAGS = -v $(PWD):/app -p 8888:8888 --rm

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dependencies
.PHONY: requirements
requirements:
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8, black, and isort (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 flagellar_motors_detection
	isort --check --diff flagellar_motors_detection
	black --check flagellar_motors_detection

## Format source code with black
.PHONY: format
format:
	isort flagellar_motors_detection
	black flagellar_motors_detection

## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	conda env create --name $(PROJECT_NAME) -f environment.yml
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"

#################################################################################
# DOCKER COMMANDS                                                               #
#################################################################################

## Build Docker image
.PHONY: docker-build
docker-build:
	docker build -t $(DOCKER_IMAGE_NAME) .

## Run Docker container with default command
.PHONY: docker-run
docker-run:
	docker run $(DOCKER_RUN_FLAGS) $(DOCKER_IMAGE_NAME)

## Run interactive shell in Docker container
.PHONY: docker-shell
docker-shell:
	docker run -it $(DOCKER_RUN_FLAGS) $(DOCKER_IMAGE_NAME) /bin/bash

## Clean Docker artifacts
.PHONY: docker-clean
docker-clean:
	docker rmi $(DOCKER_IMAGE_NAME)
	docker system prune -f

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Make dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) flagellar_motors_detection/dataset.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
