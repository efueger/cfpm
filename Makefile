########################## THE LITTLE LOVELY MAKEFILE ##########################

# List all available targets
help:
	@echo "To use this Makefile, make sure you have poetry installed and is"\
		"in PATH.\n\nAvaliable targets:"
	@sh -c "$(MAKE) -p no_targets__ | \
		awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {\
			split(\$$1,A,/ /);for(i in A)print A[i]\
		}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"

# Required for list
no_targets__:

# Clean cache stuff
clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

# Format using black
format: install-dev
	@poetry run black cfpm/ tests/

# Install an editable cfpm with development tools
install-dev:
	@poetry install -q

# Install cfpm
install:
	@pip install .

# Build cfpm
build:
	@poetry build

# Pytests and checks and stuff
test: install-dev
	@echo 'Running pytest'
	@poetry run pytest tests/ 
	@echo 'Running flake8'
	@poetry run flake8
	@echo 'Running pydocstyle'
	@poetry run pydocstyle cfpm
	@echo 'Running mypy'
	@poetry run mypy cfpm

# Make a coverage report
coverage: install-dev
	@poetry run pytest --cov=cfpm tests/
