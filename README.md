# Calendar Client — OSPSD Team 11

## Purpose

This project implements a Calendar Client. The interface defines a contract for calendar operations (creating, reading, updating, and deleting events), while the concrete implementation targets Google Calendar via its API.


## Architecture

```
.
├── components/
│   ├── calendar_client_api/          # Interface 
│   │   └── src/calendar_client_api/
│   │       ├── client.py             # CalendarClient
│   │       ├── event.py              # Event contract, Attendee + EventCreate + EventUpdate dataclasses
│   │       └── registry              # Registry + get_client()
│   └── google_calendar_client_impl/  # Concrete implementation
│       └── src/google_calendar_client_impl/
│           ├── client_impl.py        # GoogleCalendarClient
│           └── event_impl.py         # GoogleCalendarEvent
├── tests/
│   ├── integration/                  # DI and cross-component tests
│   └── e2e/                          # End-to-end tests against real APIs
├── docs/                             # Documentation Source Files
├── mkdocs.yml
├── pyproject.toml                    # workspace config
└── .circleci/config.yml              # CI pipeline
```

## Setup

### Prerequisites

- **Python 3.13+**
- **[uv](https://docs.astral.sh/uv/)** — the package manager for this project

### Installation

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Clone the repository
git clone <repo-url> && cd <repo-name>
```

## Toolchain Usage

| Tool | Purpose | Command |
|------|---------|---------|
| **uv** | Dependency & workspace management | `uv sync --all-packages --extra dev` |
| **ruff** | Linting & formatting | `ruff check .` / `ruff format .` |
| **mypy** | Static type checking (strict mode) | `mypy .` |
| **pytest** | Test runner with coverage (≥ 85 % threshold) | `pytest` |
| **MkDocs** | Documentation site | `mkdocs serve` / `mkdocs build` |
| **CircleCI** | Continuous integration | Triggered on push (see `.circleci/config.yml`) |

