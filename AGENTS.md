# Agent Guidelines for MREdu

## Build/Test Commands

### Using just (recommended)

Run `just --list` to see all available commands. Common commands:

- **Install dependencies**: `just install` (or `uv sync`)
- **Run all tests**: `just test`
- **Run single test**: `just test-one test_word_count`
- **Run with coverage**: `just coverage`
- **Build package**: `just build`
- **Clean artifacts**: `just clean`
- **Run examples**: `just example3` or `just examples` (all)
- **Project stats**: `just stats`
- **Package info**: `just info`

### Using uv directly

- **Install dependencies**: `uv sync`
- **Install package (editable)**: Automatically done by `uv sync`
- **Run all tests**: `uv run pytest`
- **Run single test**: `uv run pytest tests/test_simul.py::test_word_count`
- **Run with coverage**: `uv run pytest --cov=mredu`
- **Run examples**: `uv run python examples/example3.py`

### Publishing to PyPI

- **Check package**: `just check-package`
- **Publish to Test PyPI**: `just publish-test`
- **Publish to PyPI**: `just publish` (requires confirmation)

## Code Style

### Imports

- Standard library imports first (e.g., `re`, `itertools`, `pathlib`)
- Third-party imports second (e.g., `toolz`, `rich`)
- Local imports last (e.g., `from mredu.simul import ...`)

### Type Hints

- Use type hints for all function signatures: `Iterable[Pair]`, `Callable[[Key, Value], MapperResult]`, etc.
- Define custom type aliases at module level: `Pair = Tuple[Key, Value]`
- Support both str and Path objects for file paths: `Union[str, Path]`

### Naming Conventions

- Functions: `snake_case` (e.g., `input_file`, `process_mapper`)
- Private functions: prefix with `__` (e.g., `__flatten`, `__input_file`)
- Type variables: `PascalCase` (e.g., `Key`, `Value`)

### Error Handling

- Use try/except in user-facing functions like `run()` with rich console error formatting
- Provide descriptive error messages using `rich.console`
- Use specific exceptions (FileNotFoundError, PermissionError, ValueError) instead of generic Exception
- Always include context in error messages (e.g., file path, operation being performed)

### File Path Handling

- Always use `pathlib.Path` for file operations to ensure cross-platform compatibility
- Accept both `str` and `Path` objects in function signatures: `Union[str, Path]`
- Convert string paths to Path objects internally: `path_obj = Path(path)`

## Recent Improvements

### Migration to uv (Completed)
- Modern dependency management with `uv`
- Fast lockfile-based installs
- `pyproject.toml` following PEP 621 standards
- All dependencies managed in dependency groups

### Minor Improvements (Completed)
- Fixed docstring in `process_reducer` (was incorrectly labeled as "mapper")
- Added pathlib.Path support for Windows compatibility
- Implemented granular error handling (FileNotFoundError, PermissionError, UnicodeDecodeError)
- Added 6 new tests (12 total, 91% coverage)
- Better error messages with context

### Task Automation (Completed)
- Added comprehensive justfile with 20+ commands
- Automated testing, building, and publishing workflows
- Release automation with version bumping and tagging
- Package verification commands
- Fixed shell compatibility issues in `publish` and `release` commands (bash shebang, proper `read` handling)

### Bug Fixes (Completed)
- Fixed `justfile` publish command: Changed from `sh` to `bash` with proper shebang
- Fixed `read: arg count` error by using `read -r` instead of `@read`
- Added `set -euo pipefail` to publish and release recipes for better error handling
- Both commands now properly accept user input for confirmation

## Next Steps (Recommended)

### High Priority

1. **Code Quality Tools**
   - Add `ruff` for linting and formatting
   - Add `mypy` for static type checking
   - Configure pre-commit hooks for automated checks
   ```toml
   # Add to pyproject.toml dependency-groups.dev
   "ruff>=0.8.0",
   "mypy>=1.0.0",
   "pre-commit>=3.0.0",
   ```

2. **CI/CD with GitHub Actions**
   - Automated testing on push/PR
   - Multi-version Python testing (3.8-3.13)
   - Coverage reporting
   - Automated PyPI publishing on release tags
   
   Create `.github/workflows/test.yml`:
   ```yaml
   name: Tests
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v4
         - run: uv sync
         - run: uv run pytest --cov
   ```

### Medium Priority

3. **Enhanced Testing**
   - Add parametrized tests with `@pytest.mark.parametrize`
   - Add property-based testing with `hypothesis`
   - Add integration/end-to-end tests
   - Add performance benchmarks

4. **Documentation**
   - Set up Sphinx or MkDocs for documentation
   - Generate API reference from docstrings
   - Create tutorial/getting started guide
   - Publish to ReadTheDocs or GitHub Pages

5. **Type Checking Improvements**
   - Use `from __future__ import annotations` for cleaner type hints
   - Add more specific types (e.g., `Iterator` vs `Iterable`, `os.PathLike`)
   - Define Protocol classes for duck typing

### Low Priority

6. **CLI Interface**
   - Add command-line interface with Click or Typer
   - Example: `mredu wordcount data/file.txt`

7. **Development Environment**
   - Add devcontainer configuration
   - Add Docker setup for reproducible environments

8. **README Enhancements**
   - Add badges (build status, coverage, PyPI version)
   - Add more usage examples
   - Add contributing guidelines

9. **Release Automation**
   - Use `commitizen` or `semantic-release` for version management
   - Auto-generate CHANGELOG from commits
   - Semantic versioning enforcement

## Project Status

- **Tests**: 12/12 passing (100%)
- **Coverage**: 91% (64/70 lines)
- **Python Support**: 3.8+
- **Platform Support**: Linux, macOS, Windows
- **Package Status**: Ready for PyPI publication
- **Dependencies**: Modern tooling (uv, pytest, twine, just)
- **Version**: 1.1.0
- **Justfile**: 20+ automated commands, all working correctly
