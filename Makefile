# Makefile for Pygame Project

# Variables
PYTHON = python3
MAIN = main.py
VENV = venv
REQS = requirements.txt

# Default target: Run the game
run: venv
	@$(VENV)/bin/$(PYTHON) $(MAIN)

# Create virtual environment and install dependencies
venv: $(VENV)/bin/activate

$(VENV)/bin/activate: $(REQS)
	@python3 -m venv $(VENV)
	@$(VENV)/bin/pip install -r $(REQS)
	@touch $(VENV)/bin/activate

# Clean virtual environment
clean:
	@rm -rf $(VENV)
	@rm -rf __pycache__

# Help target to display available options
help:
	@echo "Makefile for Pygame project"
	@echo ""
	@echo "Available targets:"
	@echo "  run     - Run the game"
	@echo "  venv    - Create a virtual environment and install dependencies"
	@echo "  clean   - Remove the virtual environment and cached files"
	@echo "  help    - Display this help message"
