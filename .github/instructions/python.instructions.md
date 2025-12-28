---
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py, **/*.ipynb'
---

# Python Coding Conventions

## Python Instructions

- Write clear and concise comments for each function.
- Ensure functions have descriptive names and include type hints.
- Provide docstrings following PEP 257 conventions.
- Use the `typing` module for type annotations (e.g., `List[str]`, `Dict[str, int]`).
- Provide type hints for functions and methods.
- Ensure code is compatible with Python 3.12+.
- Use built-in generics (e.g., `list[str]`, `dict[str, int]`) if using Python 3.9 or later.
- Use the `typing` module for type annotations (e.g., `List[str]`, `Dict[str, int]`) if supporting earlier Python versions.
- Break down complex functions into smaller, more manageable functions.

## General Instructions

- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

## Code Style and Formatting

- Follow the **PEP 8** style guide for Python.
- Maintain proper indentation (use 4 spaces for each level of indentation).
- Ensure lines do not exceed 79 characters (per PEP 8 recommendations).
- Place function and class docstrings immediately after the `def` or `class` keyword.
- Use blank lines to separate functions, classes, and code blocks where appropriate.
- Use f-strings for formatting; **avoid wildcard imports** (`from module import *`).
- Use list comprehensions and generator expressions where appropriate.
- Use `ruff` for import ordering and formatting consistency.

## Naming conventions

- Packages / Modules: lowercase, short; use underscores only if necessary (e.g., `package_name`, `module_name.py`).
- Classes / Exceptions: PascalCase (e.g., `UserProfile`, `InvalidStateError`).
- Functions / Methods / Variables: snake_case (e.g., `load_config`, `to_dataframe`).
- Constants: UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`).
- Boolean names: prefix with `is_`, `has_`, `can_`, `should_`.
- Private API: prefix with `_` (e.g., `_parse_token`).
- Test files: `test_<module>.py`; test functions: `test_<target>_<condition>_<expected>`.
- Async functions: use `async def` (no `_async` suffix).
- Acronyms: treat as words in PascalCase (e.g., `HttpServer`, `get_url`).

## Edge Cases and Testing

- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.
- Write unit tests for functions and document them with docstrings explaining the test cases.

### Exception Handling

- Use specific exception types rather than bare `except:` clauses.
- Provide meaningful error messages that describe what went wrong and how to fix it.
- Document expected exceptions in docstrings using `Raises:` section.
- Example:
  ```python
  try:
      result = int(user_input)
  except ValueError as e:
      raise ValueError(f"Expected integer, got: {user_input}") from e
  ```

## Docstrings and Comments

- Follow PEP 257 conventions for docstrings.
- Use Google-style docstring format for consistency (Parameters, Returns, Raises sections).
- Document all public functions, methods, and classes.
- For complex logic, include inline comments explaining the reasoning.

## Formatting and linting

- Use `ruff` for lint and formatting (including import ordering).
- Use `mypy` for static type checking.
- Run `pre-commit` hooks locally before committing to ensure consistency.

## Local development environment (uv workflow)

This project uses [uv](https://github.com/astral-sh/uv) for Python version and dependency management.

### Initial setup

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # install uv if not present
uv sync                                        # resolve deps & create .venv
```

### Python version

Pinned to the 3.12 line: `requires-python = ">=3.12,<3.13"` in `pyproject.toml`.

If multiple versions are installed:
```bash
uv sync --python 3.12
```

### Common commands

```bash
uv run pytest -q          # tests
uv run ruff check .       # lint
uv run ruff format .      # format
uv add <pkg>              # add runtime dependency
uv add --group dev <pkg>  # add dev-only dependency
uv remove <pkg>           # remove dependency
uv lock --upgrade && uv sync   # upgrade all & re-sync
uv sync --frozen          # deterministic CI install
```

### Dependency management

- Runtime dependencies live under `[project].dependencies` in `pyproject.toml`.
- Development-only packages (tests, lint, tooling) are specified under `[dependency-groups].dev`.
- Optional user-facing features go under `[project.optional-dependencies]` (e.g., `pip install .[svm]`).

### Pre-commit integration

Run tools via uv to ensure the managed interpreter is used:

```bash
uv run pre-commit run --all-files
```

Configure hooks to call `uv run ruff` or `uv run pytest` for consistency.

## Example of Proper Documentation

```python
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given the radius.
    
    Args:
        radius: The radius of the circle (must be non-negative).
    
    Returns:
        The area of the circle, calculated as π * radius^2.
    
    Raises:
        ValueError: If radius is negative.
    """
    if radius < 0:
        raise ValueError(f"Radius must be non-negative, got {radius}")
    
    import math
    return math.pi * radius ** 2
```
