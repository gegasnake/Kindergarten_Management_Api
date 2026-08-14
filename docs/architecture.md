# Architecture

This document describes the high-level architecture and organization of the Kindergarten Management System.

## High-Level Architecture

The application currently follows a Django-based backend architecture.

```text
Client
   |
   | HTTP / REST
   v
Django / Django REST Framework
   |
   | ORM
   v
PostgreSQL
```

Django is responsible for application logic, API endpoints, administration, authentication, and database access.

PostgreSQL provides persistent relational storage.

---

## Django Applications

Functionality is separated into Django applications.

The current administration application is located at:

```text
administration/
```

As the system grows, additional applications may be introduced when separate business domains require them.

---

## Project Configuration

Project-level Django configuration is stored under:

```text
config/
```

Django settings are separated by responsibility rather than by deployment environment.

For example:

```text
config/
└── settings/
    ├── __init__.py
    ├── base.py
    ├── apps.py
    ├── database.py
    ├── middleware.py
    ├── security.py
    ├── templates.py
    ├── internationalization.py
    └── static.py
```

`base.py` combines the individual settings modules into the final Django configuration.

Environment-specific values such as database credentials and secrets are supplied through environment variables.

---

## Database

PostgreSQL 17 is used as the primary database.

Django communicates with PostgreSQL through the Django ORM.

During Docker development:

```text
Django
   |
   | POSTGRES_HOST=db
   v
PostgreSQL container
```

Database data is stored in a persistent Docker volume.

This means restarting or recreating normal containers does not automatically remove database data.

---

## Dependency Management

Python dependencies are managed with `uv`.

```text
pyproject.toml
      |
      v
    uv
      |
      v
uv.lock
```

`pyproject.toml` defines project dependencies and tool configuration.

`uv.lock` records the resolved dependency versions to provide reproducible environments.

---

## Validation Architecture

Project validation is coordinated through tox.

```text
tox
├── pytest
├── Ruff lint
├── Ruff format --check
├── mypy
├── Django system checks
└── MkDocs build
```

This provides a common validation interface for both development and Continuous Integration.

---

## Continuous Integration

GitHub Actions runs the validation suite automatically.

```text
Push / Pull Request
        |
        v
GitHub Actions
        |
        v
uv sync --locked
        |
        v
tox
        |
        v
Pass / Fail
```

This ensures that the same quality checks can be executed locally and in CI.

---

## Future Architecture

The architecture will evolve as business modules are implemented.

Potential domains include:

```text
Kindergarten Management System
├── Resources
├── Children
├── Groups
├── Parents
├── Fees
├── Library
├── Contracts
└── Cleaning schedules
```

Architecture decisions should favor clear separation of responsibilities and maintainability as the project grows.
