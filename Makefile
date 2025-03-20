# Define variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Default target
.DEFAULT_GOAL := help

# 1️⃣ Set up the virtual environment
venv:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip

# 2️⃣ Install dependencies
install: venv
	$(PIP) install -r requirements.txt

# 3️⃣ Run the FastAPI server
run: install
	$(PYTHON) -m uvicorn src.app.main:app --reload

# 4️⃣ Run database migrations
migrate: install
	alembic upgrade head

# 5️⃣ Run tests
test: install
	pytest tests/

# 6️⃣ Run linter (flake8)
lint: install
	flake8 src/

# 7️⃣ Run type checks (mypy)
type-check: install
	mypy src/

# 8️⃣ Clean up cache and temporary files
clean:
	rm -rf $(VENV) __pycache__ .pytest_cache .mypy_cache

# 9️⃣ Show available commands
help:
	@echo "Usage:"
	@echo "  make venv       - Create a virtual environment"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the FastAPI server"
	@echo "  make migrate    - Apply database migrations"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting (flake8)"
	@echo "  make type-check - Run type checking (mypy)"
	@echo "  make clean      - Remove temporary files"
