# Kindergarten Management System

A Django-based management system designed to support the administration and daily operations of a kindergarten.

The system is intended to provide centralized management for areas such as resources, children, contracts, library records, cleaning schedules, documents, menus, and other administrative functionality.

## Tech Stack

- Python 3.13
- Django
- Django REST Framework
- PostgreSQL 17
- Docker
- Docker Compose
- uv
- Ruff
- pytest
- pytest-django
- pre-commit
- drf-spectacular / Swagger

---

# Development Setup

The standard development environment for this project uses **Docker and Docker Compose**.

Application commands such as Django management commands, tests, linting, and formatting should normally be executed inside the `web` container.

## Prerequisites

Install:

- Git
- Docker
- Docker Compose

`uv` is used for Python dependency management inside the project.

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

POSTGRES_DB=kindergarten_db
POSTGRES_USER=kindergarten_user
POSTGRES_PASSWORD=kindergarten_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Do not commit the real `.env` file.

It should be included in `.gitignore`.

---

# Docker Development Environment

## Build and start the project

```bash
docker compose up --build -d
```

This starts:

- PostgreSQL
- Django

## Check running containers

```bash
docker compose ps
```

## View Django logs

```bash
docker compose logs -f web
```

## View PostgreSQL logs

```bash
docker compose logs -f db
```

## Stop the project

```bash
docker compose down
```

PostgreSQL data is stored in a Docker volume and persists when containers are stopped or recreated.

> Do not run `docker compose down -v` unless you intentionally want to delete the PostgreSQL data volume.

---

# Dependency Management

The project uses **uv** for Python dependency management.

Dependencies are defined in:

```text
pyproject.toml
```

Exact resolved dependency versions are stored in:

```text
uv.lock
```

The lock file should be committed to Git.

## Synchronize dependencies

Inside Docker:

```bash
docker compose exec web uv sync
```

Non-Docker equivalent:

```bash
uv sync
```

## Add a runtime dependency

For example:

```bash
docker compose exec web uv add django-filter
```

General form:

```bash
docker compose exec web uv add <package>
```

## Add a development dependency

For example:

```bash
docker compose exec web uv add --dev pytest
```

General form:

```bash
docker compose exec web uv add --dev <package>
```

Development dependencies include tools such as:

- Ruff
- pytest
- pytest-django
- pre-commit

---

# Django Commands

Django commands should normally be executed inside the `web` container.

## Django system check

```bash
docker compose exec web uv run python manage.py check
```

## Create migrations

```bash
docker compose exec web uv run python manage.py makemigrations
```

## Apply migrations

```bash
docker compose exec web uv run python manage.py migrate
```

Non-Docker equivalent:

```bash
uv run python manage.py migrate
```

## Show migrations

```bash
docker compose exec web uv run python manage.py showmigrations
```

## Create a superuser

```bash
docker compose exec web uv run python manage.py createsuperuser
```

## Open Django shell

```bash
docker compose exec web uv run python manage.py shell
```

## Development server

Docker Compose automatically starts the Django development server.

If it needs to be started manually:

```bash
docker compose exec web uv run python manage.py runserver 0.0.0.0:8000
```

Non-Docker equivalent:

```bash
uv run python manage.py runserver
```

---

# Django Admin

The Django administration interface is available at:

```text
http://localhost:8000/admin/
```

A superuser must exist before logging in.

Create one with:

```bash
docker compose exec web uv run python manage.py createsuperuser
```

---

# API Documentation

API documentation is generated using **drf-spectacular**.

Depending on the configured URL routes, Swagger documentation is available through the project's Swagger endpoint.

For example:

```text
http://localhost:8000/api/swagger/
```

The OpenAPI schema can also be exposed through the configured schema endpoint.

---

# Code Quality

The project uses **Ruff** for Python linting and formatting.

Ruff configuration is stored in:

```text
pyproject.toml
```

## Run Ruff linting

```bash
docker compose exec web uv run ruff check .
```

Non-Docker equivalent:

```bash
uv run ruff check .
```

## Automatically fix supported lint problems

```bash
docker compose exec web uv run ruff check . --fix
```

## Format Python code

```bash
docker compose exec web uv run ruff format .
```

Non-Docker equivalent:

```bash
uv run ruff format .
```

## Check formatting without changing files

```bash
docker compose exec web uv run ruff format --check .
```

---

# Testing

The project uses:

- pytest
- pytest-django

pytest configuration is stored in:

```text
pyproject.toml
```

## Run all tests

```bash
docker compose exec web uv run pytest
```

Non-Docker equivalent:

```bash
uv run pytest
```

## Run administration tests

```bash
docker compose exec web uv run pytest administration/tests
```

## Run a specific test file

For example:

```bash
docker compose exec web uv run pytest administration/tests/test_database.py
```

## Run a specific test

Example:

```bash
docker compose exec web uv run pytest administration/tests/test_database.py::test_user_can_be_created
```

---

# Testing Conventions

Each Django application should maintain its own `tests/` package.

Example:

```text
administration/
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_database.py
│   ├── test_models.py
│   ├── test_api.py
│   ├── test_integration.py
│   └── conftest.py
```

Files should only be added when they contain meaningful tests.

## Naming conventions

Test files should follow:

```text
test_*.py
```

Test functions should follow:

```python
def test_expected_behavior():
    ...
```

Test classes should follow:

```python
class TestResourceAPI:
    ...
```

Shared pytest fixtures should be placed in:

```text
conftest.py
```

## Test locations

Model tests:

```text
test_models.py
```

API tests:

```text
test_api.py
```

Integration tests:

```text
test_integration.py
```

General application tests may use:

```text
test_app.py
```

Database-specific tests may use:

```text
test_database.py
```

## Database tests

Tests that access the Django database should use:

```python
import pytest


@pytest.mark.django_db
def test_example():
    ...
```

or an appropriate pytest/pytest-django database fixture.

pytest-django creates a separate test database so tests do not modify the normal development database.

---

# Pre-commit

The project uses **pre-commit** to automatically perform code-quality and repository-hygiene checks before commits are created.

Configuration is stored in:

```text
.pre-commit-config.yaml
```

Configured checks include:

- Ruff linting
- Ruff formatting
- Trailing whitespace
- End-of-file fixing
- YAML validation
- TOML validation
- Large accidental file checks

## Install Git hooks

```bash
uv run pre-commit install
```

The Git hook itself is installed on the host because the project's `.git` repository is managed by the host Git installation.

This normally only needs to be done once after cloning the repository.

## Run all pre-commit checks manually

```bash
uv run pre-commit run --all-files
```

If a hook fails, the commit is blocked until the problem is fixed.

Some hooks may automatically modify files. If that happens, review the changes, stage them again, and retry the commit.

---

# Standard Development Workflow

A typical development session looks like this.

## 1. Start Docker

```bash
docker compose up -d
```

## 2. Synchronize dependencies when necessary

```bash
docker compose exec web uv sync
```

## 3. Apply database migrations

```bash
docker compose exec web uv run python manage.py migrate
```

## 4. Develop the feature

Write or modify the required Django code.

## 5. Run Ruff

```bash
docker compose exec web uv run ruff check .
```

Fix supported problems automatically when appropriate:

```bash
docker compose exec web uv run ruff check . --fix
```

## 6. Format the code

```bash
docker compose exec web uv run ruff format .
```

## 7. Run tests

```bash
docker compose exec web uv run pytest
```

## 8. Run Django checks

```bash
docker compose exec web uv run python manage.py check
```

## 9. Run all pre-commit checks

```bash
uv run pre-commit run --all-files
```

## 10. Commit

```bash
git add .
git commit -m "Describe the change"
```

The installed pre-commit hook automatically runs the configured checks before Git creates the commit.

---

# Quick Command Reference

| Task | Command |
|---|---|
| Start containers | `docker compose up -d` |
| Build and start | `docker compose up --build -d` |
| Stop containers | `docker compose down` |
| Check containers | `docker compose ps` |
| Django logs | `docker compose logs -f web` |
| Sync dependencies | `docker compose exec web uv sync` |
| Django check | `docker compose exec web uv run python manage.py check` |
| Create migrations | `docker compose exec web uv run python manage.py makemigrations` |
| Apply migrations | `docker compose exec web uv run python manage.py migrate` |
| Create superuser | `docker compose exec web uv run python manage.py createsuperuser` |
| Django shell | `docker compose exec web uv run python manage.py shell` |
| Ruff lint | `docker compose exec web uv run ruff check .` |
| Ruff auto-fix | `docker compose exec web uv run ruff check . --fix` |
| Ruff format | `docker compose exec web uv run ruff format .` |
| Run tests | `docker compose exec web uv run pytest` |
| Run administration tests | `docker compose exec web uv run pytest administration/tests` |
| Pre-commit checks | `uv run pre-commit run --all-files` |

---

# Non-Docker Command Reference

The standard workflow for this project uses Docker.

For reference, the equivalent local commands are:

```bash
uv sync

uv run python manage.py migrate

uv run python manage.py runserver

uv run ruff check .

uv run ruff format .

uv run pytest

uv run pre-commit run --all-files
```

Application execution, Django commands, linting, formatting, and tests should normally be performed through Docker.

---

# Project Structure

The project currently follows a structure similar to:

```text
KindergartenManagementSystem/
├── administration/
│   ├── migrations/
│   ├── tests/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

# Planned Functionality

The Kindergarten Management System is planned to include administrative functionality for:

- Resource and inventory management
- Children management
- Parent information
- Kindergarten fees
- Age/group management
- Library and book tracking
- Employee contracts
- Children contracts
- DOCX/PDF document upload and download
- Contract generation
- Cleaning schedules
- HASP document management
- Summer kindergarten menus
- Additional administrative functionality as the project grows

---

# Development Principles

The project aims to maintain:

- Reproducible dependency management with `uv`
- Consistent Python environments
- Containerized development with Docker
- Automated formatting and linting with Ruff
- Automated testing with pytest
- Isolated Django test databases
- Pre-commit quality checks
- Clear application-level test organization
- Incremental development through small, testable features
