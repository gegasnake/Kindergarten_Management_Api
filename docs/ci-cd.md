# CI/CD

This document describes the project's Continuous Integration and future Continuous Deployment strategy.

## Continuous Integration

The project uses **GitHub Actions** for Continuous Integration.

The workflow is stored under:

```text
.github/workflows/
```

CI runs automatically for configured pushes and pull requests.

---

## CI Pipeline

The current pipeline follows:

```text
Push / Pull Request
        |
        v
GitHub Actions
        |
        v
Setup Python 3.13
        |
        v
Install uv
        |
        v
Start PostgreSQL
        |
        v
uv sync --locked
        |
        v
tox
├── pytest
├── Ruff lint
├── Ruff format validation
├── mypy
├── Django system checks
└── MkDocs validation
        |
        v
CI Passed / Failed
```

---

## Why tox Is Used in CI

GitHub Actions does not duplicate individual validation commands.

Instead, CI executes:

```bash
uv run tox
```

Tox defines the project's validation environments.

This means local development and CI use the same validation process.

---

## PostgreSQL in CI

GitHub Actions provides a temporary PostgreSQL service for database tests.

The CI database is separate from the local development database.

No production database credentials are used during CI.

---

## Dependency Installation

CI installs dependencies using:

```bash
uv sync --locked
```

The `--locked` option ensures that CI uses the committed dependency resolution and does not silently modify `uv.lock`.

---

## Failure Behavior

If any validation fails, tox returns a non-zero exit code.

Examples include:

- failing pytest tests
- Ruff lint violations
- invalid formatting
- mypy errors
- failed Django system checks
- invalid MkDocs documentation

The GitHub Actions job is then marked as failed.

---

## Continuous Deployment

Continuous Deployment is intentionally not configured yet.

A deployment workflow will be introduced after the production hosting infrastructure and deployment strategy have been selected.

Future deployment requirements include:

- deployment separated from CI
- deployment only from approved branches/environments
- successful CI required before deployment
- secrets stored using GitHub Secrets or GitHub Environments
- no production secrets committed to Git
- clearly defined rollback/failure behavior
- documented deployment procedure
