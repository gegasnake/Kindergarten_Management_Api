# Development

This document describes the standard development workflow for the project.

## Development Environment

Development is Docker-based.

Application commands should normally be executed inside the `web` container.

Start the environment:

```bash
docker compose up -d
```

Check the running services:

```bash
docker compose ps
```

---

## Django Commands

Run Django system checks:

```bash
docker compose exec web uv run python manage.py check
```

Create migrations:

```bash
docker compose exec web uv run python manage.py makemigrations
```

Apply migrations:

```bash
docker compose exec web uv run python manage.py migrate
```

---

## Dependencies

Add a runtime dependency:

```bash
docker compose exec web uv add <package>
```

Add a development dependency:

```bash
docker compose exec web uv add --dev <package>
```

Synchronize dependencies:

```bash
docker compose exec web uv sync
```

Changes to dependencies should update `pyproject.toml` and, where applicable, `uv.lock`.

---

## Ruff

Ruff provides linting and formatting.

Run lint validation:

```bash
docker compose exec web uv run ruff check .
```

Automatically fix supported lint violations:

```bash
docker compose exec web uv run ruff check . --fix
```

Format the project:

```bash
docker compose exec web uv run ruff format .
```

Check formatting without modifying files:

```bash
docker compose exec web uv run ruff format --check .
```

---

## mypy

mypy provides static type checking.

Run:

```bash
docker compose exec web uv run mypy
```

New code should avoid introducing new mypy errors.

---

## tox

Tox provides the common interface for project validation.

Run the complete validation suite:

```bash
docker compose exec web uv run tox
```

Individual environments can also be executed separately.

For example:

```bash
docker compose exec web uv run tox run -e tests
```

```bash
docker compose exec web uv run tox run -e lint
```

```bash
docker compose exec web uv run tox run -e type
```

---

## Pre-commit

Pre-commit runs automated checks before Git commits are created.

Install hooks:

```bash
docker compose exec web uv run pre-commit install
```

Run all hooks manually:

```bash
docker compose exec web uv run pre-commit run --all-files
```

A failing hook should be resolved before committing.

---

## Recommended Workflow

A typical development workflow is:

```text
Create/update branch
        ↓
Make changes
        ↓
Run tests
        ↓
Run tox
        ↓
Run pre-commit
        ↓
Commit
        ↓
Push
        ↓
GitHub Actions CI
```

Before pushing significant changes, run:

```bash
docker compose exec web uv run tox
```

This reduces the chance of CI failures.
