# Agent Guidelines for MREdu

> **IMPORTANT**: After completing any change to the project, always verify if this AGENTS.md file needs to be updated to reflect new commands, workflows, dependencies, or improvements.

## Build/Test Commands

### Using just (recommended)

Run `just` for an interactive menu (requires [gum](https://github.com/charmbracelet/gum)), or `just --list` to see all available commands. Common commands:

- **Install dependencies**: `just install` (or `uv sync`)
- **Run all tests**: `just test`
- **Run single test**: `just test-one test_word_count`
- **Run with coverage**: `just coverage`
- **Build package**: `just build`
- **Clean artifacts**: `just clean`
- **Run examples**: `just example3` or `just examples` (all)
- **Project stats**: `just stats`
- **Package info**: `just info`

### Code Quality Commands (NEW)

- **Lint code**: `just lint` (check code quality)
- **Lint and fix**: `just lint-fix` (auto-fix issues)
- **Format code**: `just format` (apply ruff formatting)
- **Check format**: `just format-check` (verify formatting)
- **Type check**: `just typecheck` (run mypy)
- **All checks**: `just check-all` (lint + format + typecheck)
- **Setup hooks**: `just setup-hooks` (install pre-commit)
- **Run pre-commit**: `just pre-commit-all` (all files)

### Using uv directly

- **Install dependencies**: `uv sync`
- **Install package (editable)**: Automatically done by `uv sync`
- **Run all tests**: `uv run pytest`
- **Run single test**: `uv run pytest tests/test_simul.py::test_word_count`
- **Run with coverage**: `uv run pytest --cov=mredu`
- **Run examples**: `uv run python examples/example3.py`
- **Lint code**: `uv run ruff check mredu/ tests/ examples/`
- **Format code**: `uv run ruff format mredu/ tests/ examples/`
- **Type check**: `uv run mypy mredu/ tests/`
- **Pre-commit**: `uv run pre-commit run --all-files`

### Publishing to PyPI

- **Check package**: `just check-package`
- **Publish to Test PyPI**: `just publish-test`
- **Publish to PyPI**: `just publish` (requires confirmation)

## Code Style

**Note**: Code quality is enforced by `ruff` (linter + formatter), `mypy` (type checker), and `pre-commit` hooks. Run `just check-all` before committing.

### Formatting (enforced by ruff)

- **Line length**: 100 characters max
- **Quote style**: Single quotes (`'`)
- **Indentation**: 4 spaces (no tabs)
- **Import sorting**: Automatic (stdlib → third-party → local)

### Imports

- Standard library imports first (e.g., `re`, `itertools`, `pathlib`)
- Third-party imports second (e.g., `toolz`, `rich`)
- Local imports last (e.g., `from mredu.simul import ...`)
- **Enforced by**: ruff's isort rules

### Type Hints

- Use type hints for all function signatures: `Iterable[Pair]`, `Callable[[Key, Value], MapperResult]`, etc.
- Define custom type aliases at module level: `Pair = Tuple[Key, Value]`
- Support both str and Path objects for file paths: `Union[str, Path]`
- **Checked by**: mypy with moderate strictness

### Naming Conventions

- Functions: `snake_case` (e.g., `input_file`, `process_mapper`)
- Private functions: prefix with `__` (e.g., `__flatten`, `__input_file`)
- Type variables: `PascalCase` (e.g., `Key`, `Value`)
- Avoid ambiguous names: No single-letter vars like `l` (use `data`, `items`, etc.)
- **Enforced by**: ruff's pep8-naming rules

### Error Handling

- Use try/except in user-facing functions like `run()` with rich console error formatting
- Provide descriptive error messages using `rich.console`
- Use specific exceptions (FileNotFoundError, PermissionError, ValueError) instead of generic Exception
- Always include context in error messages (e.g., file path, operation being performed)
- Use `raise ... from err` to maintain exception chains
- **Enforced by**: ruff's flake8-bugbear rules (B904)

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
- Interactive task menu with gum integration (optional, falls back to just --list)
- Automated testing, building, and publishing workflows
- Release automation with version bumping and tagging
- Package verification commands
- Fixed shell compatibility issues in `publish` and `release` commands (bash shebang, proper `read` handling)

### Bug Fixes (Completed)
- Fixed `justfile` publish command: Changed from `sh` to `bash` with proper shebang
- Fixed `read: arg count` error by using `read -r` instead of `@read`
- Added `set -euo pipefail` to publish and release recipes for better error handling
- Both commands now properly accept user input for confirmation

### Code Quality Tools (Completed ✅)
- **ruff** (v0.14.3+): Ultrafast linter and formatter
  - Configured with 100 char line length, single quotes
  - Enforces pycodestyle, pyflakes, isort, pep8-naming, pyupgrade, flake8-bugbear, flake8-comprehensions, flake8-simplify, flake8-return
  - Auto-fixes import sorting, trailing whitespace, and more
- **mypy** (v1.18.2+): Static type checker
  - Python 3.9+ compatibility
  - Configured with moderate strictness
  - Ignores missing imports for toolz (no stubs available)
- **pre-commit** (v4.3.0+): Git hooks framework
  - Runs ruff (lint + format), mypy, and basic file checks
  - Automatically enforces code quality on every commit
  - 9 hooks configured (trailing whitespace, end-of-file, yaml, toml, merge conflicts, ruff check, ruff format, mypy)
  - Excludes `data/` directory from formatting hooks (preserves test data)
- **justfile commands**: 9 new commands added
  - `just lint`, `just lint-fix`, `just format`, `just format-check`
  - `just typecheck`, `just check-all`
  - `just setup-hooks`, `just pre-commit-all`
- **Code improvements**:
  - All code formatted with ruff (5 files reformatted)
  - 11 linting issues fixed (7 auto, 4 manual)
  - All type errors resolved
  - Exception chains properly maintained (`raise ... from err`)
  - Ambiguous variable names eliminated
- **Cleanup**:
  - Removed `setup.py` (superseded by `pyproject.toml`)
  - Removed `Ejemplos con MREdu.ipynb` (not part of package)
  - Updated README.md with clearer installation instructions (pip + uv)

## Next Steps (Recommended)

### High Priority

1. **CI/CD with GitHub Actions** ⭐ RECOMMENDED NEXT
   - Automated testing on push/PR
   - Multi-version Python testing (3.8-3.13)
   - Code quality checks (ruff + mypy)
   - Coverage reporting
   - Automated PyPI publishing on release tags

   Create `.github/workflows/ci.yml`:
   ```yaml
   name: CI
   on: [push, pull_request]
   jobs:
     quality:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v4
         - run: uv sync
         - run: uv run ruff check .
         - run: uv run ruff format --check .
         - run: uv run mypy mredu/ tests/
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v4
           with:
             python-version: ${{ matrix.python-version }}
         - run: uv sync
         - run: uv run pytest --cov=mredu --cov-report=xml
         - uses: codecov/codecov-action@v4
           if: matrix.python-version == '3.13'
   ```

### Medium Priority

2. **Enhanced Testing**
   - Add parametrized tests with `@pytest.mark.parametrize`
   - Add property-based testing with `hypothesis`
   - Add integration/end-to-end tests
   - Add performance benchmarks
   - Increase coverage from 91% to 95%+

3. **Documentation**
   - Set up Sphinx or MkDocs for documentation
   - Generate API reference from docstrings
   - Create tutorial/getting started guide
   - Publish to ReadTheDocs or GitHub Pages
   - Add docstring examples with doctest

4. **Type Checking Improvements**
   - Use `from __future__ import annotations` for cleaner type hints
   - Add more specific types (e.g., `Iterator` vs `Iterable`, `os.PathLike`)
   - Define Protocol classes for duck typing
   - Fix `input_kv_file` return type (currently `Iterable[List[str]]`, should be `Iterable[Tuple[str, str]]`)

### Low Priority

5. **CLI Interface**
   - Add command-line interface with Click or Typer
   - Example: `mredu wordcount data/file.txt`

6. **Development Environment**
   - Add devcontainer configuration
   - Add Docker setup for reproducible environments

7. **README Enhancements**
   - Add badges (build status, coverage, PyPI version)
   - Add more usage examples
   - Add contributing guidelines
   - Add installation instructions for different package managers

8. **Release Automation**
   - Use `commitizen` or `semantic-release` for version management
   - Auto-generate CHANGELOG from commits
   - Semantic versioning enforcement

## Project Status

- **Tests**: 12/12 passing (100%)
- **Coverage**: 91% (64/70 lines)
- **Code Quality**: ✅ All checks passing (ruff + mypy + pre-commit)
- **Python Support**: 3.9+ (mypy requires 3.9+, runtime still supports 3.8)
- **Platform Support**: Linux, macOS, Windows
- **Package Status**: Ready for PyPI publication
- **Dependencies**: Modern tooling (uv, pytest, twine, just, ruff, mypy, pre-commit, bpython)
- **Version**: 1.1.1
- **Justfile**: 30+ automated commands, all working correctly
- **Pre-commit hooks**: ✅ Installed and configured (9 hooks)

## Quick Start for Developers

1. **Clone and setup**:
   ```bash
   git clone https://github.com/ramonpin/mredu.git
   cd mredu
   uv sync                    # Install all dependencies
   just setup-hooks           # Setup pre-commit hooks
   ```

2. **Development workflow**:
   ```bash
   just test                  # Run tests
   just check-all             # Run all quality checks
   just format                # Format code
   just lint-fix              # Fix linting issues
   ```

3. **Before committing**:
   - Pre-commit hooks will automatically run
   - Or manually: `just check-all && just test`
   - Ensure all checks pass before pushing
