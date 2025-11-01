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

- Standard library imports first (e.g., `re`, `itertools`)
- Third-party imports second (e.g., `toolz`, `rich`)
- Local imports last (e.g., `from mredu.simul import ...`)

### Type Hints

- Use type hints for all function signatures: `Iterable[Pair]`,
`Callable[[Key, Value], MapperResult]`, etc.
- Define custom type aliases at module level: `Pair = Tuple[Key, Value]`

### Naming Conventions

- Functions: `snake_case` (e.g., `input_file`, `process_mapper`)
- Private functions: prefix with `__` (e.g., `__flatten`, `__input_file`)
- Type variables: `PascalCase` (e.g., `Key`, `Value`)

### Error Handling

- Use try/except in user-facing functions like `run()` with rich console error formatting
- Provide descriptive error messages using `rich.console`
