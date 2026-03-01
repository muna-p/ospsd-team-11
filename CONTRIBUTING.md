# Contributing

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
git clone <repo-url> && cd <repo-name>
uv sync --all-packages --extra dev
```

## Running Tests

```bash
# All tests
uv run pytest

# By tier
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m e2e

# With coverage
uv run pytest --cov=components/calendar_client_api/src --cov=components/google_calendar_client_impl/src
```

## Linting and Type Checking

```bash
# Lint
uv run ruff check .

# Auto-fix lint errors
uv run ruff check . --fix

# Format
uv run ruff format .

# Type check
uv run mypy .
```

## Branch and PR Workflow

1. Create a feature branch from `main`.
2. Make your changes and ensure all checks pass (`ruff check .`, `ruff format . --check`, `mypy .`, `pytest`).
3. Open a pull request. CircleCI will run lint, type checking, and all three test tiers automatically.
