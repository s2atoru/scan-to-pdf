---
applyTo: "**"
---
# Project general coding standards

## Naming Conventions
- Use PascalCase for component names, interfaces, and type aliases
- Use camelCase for variables, functions, and methods
- Prefix private class members with underscore (_)
- Use ALL_CAPS for constants

## Coding Practices
- For Python coding conventions and guidelines, see: [python.instructions.md](./instructions/python.instructions.md)

## Semantic commit messages

We prefer Conventional Commits (a.k.a. semantic commits) to make the commit
history structured and machine-readable. The basic format is:

```
<type>(<scope>): <short summary>

<optional body>

<optional footer>
```

Common `type` values:
- feat: a new feature
- fix: a bug fix
- docs: documentation only changes
- style: formatting, missing semicolons, no production code change
- refactor: code change that neither fixes a bug nor adds a feature
- perf: a code change that improves performance
- test: adding or updating tests
- chore: build process or auxiliary tools

Examples:

```
feat(auth): add password reset flow
fix(api): handle 500 on user lookup
docs: update contributing guide with semantic commit rules
```

### Recommended commit/PR additions

- Commit granularity: 1 commit should represent a single logical change.
- Tests: Add or update tests for `feat` and `fix` changes when applicable.
- PR template: Include `What`, `Why`, `How`, `Test`, `Impact` sections in PR body.
- Branch naming: `feat/<short-desc>`, `fix/<ticket>-<short-desc>`, `chore/<task>`.
- Rebase vs Merge: Use squash-merge for feature branches to keep history tidy.

### Local checks (run before committing or creating PR)

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src || true
uv run pytest -q
uv run pre-commit run --all-files
```

## Testing Standards

- Tests must validate real behavior: avoid meaningless assertions like `assert True`.
- Each test must express a concrete expected behavior (e.g., given input X, expect output Y).
- Keep mocks minimal and prefer tests that exercise real logic where practical.
- Avoid hardcoding values to force tests to pass. Do not add test-only conditionals into production code (e.g., `if TEST_MODE:`).
- Do not embed magic numbers or test-only values into production code; separate test configuration via environment variables or config files.
- Follow Red-Green-Refactor: write a failing test first, then implement and refactor.
- Test boundary conditions, error cases, and abnormal inputs as well as normal paths.
- Prioritize real quality over coverage metrics alone.
- Use descriptive test names that state what is being tested.

## Error Handling
- Use try/catch blocks for async operations
- Implement proper error boundaries in React components
- Always log errors with contextual information
