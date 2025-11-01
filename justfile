# MREdu - Just command runner
# Run 'just --list' to see all available commands

# Default recipe to display help
default:
    @just --list

# Install dependencies and setup development environment
install:
    uv sync

# Run all tests
test:
    uv run pytest

# Run tests with verbose output
test-verbose:
    uv run pytest -v

# Run a specific test
test-one TEST:
    uv run pytest tests/test_simul.py::{{TEST}} -v

# Run tests with coverage report
coverage:
    uv run pytest --cov=mredu --cov-report=term-missing

# Run tests with HTML coverage report
coverage-html:
    uv run pytest --cov=mredu --cov-report=html
    @echo "Coverage report generated in htmlcov/index.html"

# Clean build artifacts and cache files
clean:
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info
    rm -rf .pytest_cache
    rm -rf .coverage
    rm -rf htmlcov/
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    @echo "Cleaned build artifacts and cache files"

# Build the package
build: clean
    uv build

# Install package locally in editable mode (already done by uv sync)
install-local:
    uv sync

# Run example1
example1:
    uv run python examples/example1.py

# Run example2
example2:
    uv run python examples/example2.py

# Run example3 (word count)
example3:
    uv run python examples/example3.py

# Run example4
example4:
    uv run python examples/example4.py

# Run all examples
examples: example1 example2 example3 example4

# Check package before publishing
check-package: build
    uv run twine check dist/*

# Publish to Test PyPI
publish-test: build
    @echo "Publishing to Test PyPI..."
    uv run twine upload --repository testpypi dist/*
    @echo "Published to https://test.pypi.org/project/mredu/"

# Publish to PyPI (production)
publish: build
    #!/usr/bin/env bash
    set -euo pipefail
    echo "⚠️  WARNING: This will publish to PRODUCTION PyPI!"
    echo "Press Ctrl+C to cancel, or Enter to continue..."
    read -r
    uv run twine upload dist/*
    echo "✅ Published to https://pypi.org/project/mredu/"

# View package info
info:
    @echo "Package: mredu"
    @echo "Version: $(grep '^version' pyproject.toml | cut -d'"' -f2)"
    @echo "Python: $(uv run python --version)"
    @echo "Dependencies:"
    @uv run pip list | grep -E "toolz|rich|pytest"

# Format and lint (requires ruff - future improvement)
# lint:
#     uv run ruff check mredu/ tests/
# 
# format:
#     uv run ruff format mredu/ tests/

# Show project statistics
stats:
    @echo "=== MREdu Project Statistics ==="
    @echo "Lines of code (mredu/):"
    @find mredu -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1
    @echo "Lines of tests:"
    @find tests -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1
    @echo "Total Python files:"
    @find . -name "*.py" -not -path "./.venv/*" 2>/dev/null | wc -l
    @echo "Examples:"
    @ls -1 examples/*.py 2>/dev/null | wc -l

# Create a new release (bump version, build, tag)
release VERSION:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Creating release {{VERSION}}..."
    sed -i 's/^version = .*/version = "{{VERSION}}"/' pyproject.toml
    git add pyproject.toml
    git commit -m "chore: Bump version to {{VERSION}}"
    git tag -a v{{VERSION}} -m "Release {{VERSION}}"
    echo "✅ Release {{VERSION}} created. Push with: git push && git push --tags"

# Verify installation from PyPI works
verify-pypi VERSION:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Testing installation of mredu=={{VERSION}} from PyPI..."
    python -m venv /tmp/mredu-test-env
    source /tmp/mredu-test-env/bin/activate
    pip install mredu=={{VERSION}}
    python -c "from mredu import simul; print('✅ Import successful')"
    deactivate
    rm -rf /tmp/mredu-test-env
    echo "✅ PyPI package verified!"
