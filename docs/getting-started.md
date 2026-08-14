# Getting Started

This guide explains how to set up and run the **Kindergarten Management System** development environment.

The project uses Docker for the development environment, `uv` for Python dependency management, and PostgreSQL as the database.

---

## Requirements

Before starting, install:

- Git
- Docker
- Docker Compose

You do **not** need to manually install Python, PostgreSQL, Django, or the project's Python dependencies on your host machine.

The application environment is managed through Docker.

---

## Clone the Repository

Clone the project:

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd KindergartenManagementSystem
```

---

## Environment Variables

The project uses environment variables for configuration and secrets.

Create a `.env` file in the project root:

```bash
touch .env
```

Add the required variables:

```env
SECRET_KEY=your-development-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=kindergarten_db
POSTGRES_USER=kindergarten_user
POSTGRES_PASSWORD=kindergarten_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

The `.env` file contains environment-specific configuration and must **not** be committed to Git.

An `.env.example` file should be maintained in the repository to document the required environment variables without containing real secrets.

---

## Build the Development Environment

Build the Docker images:

```bash
docker compose build
```

Alternatively, build and start the project with:

```bash
docker compose up --build
```

To run the containers in the background:

```bash
docker compose up --build -d
```

---

## Check Container Status

Verify that the containers are running:

```bash
docker compose ps
```

The main services are:

| Service | Purpose |
| --- | --- |
| `web` | Django application |
| `db` | PostgreSQL database |

The PostgreSQL container includes a health check. The Django container waits for PostgreSQL to become healthy before starting.

---

## Dependency Management

Python dependencies are managed using `uv`.

The main dependency configuration is stored in:

```text
pyproject.toml
```

Exact resolved dependency versions are stored in:

```text
uv.lock
```

The Docker image installs dependencies using the uv-managed project configuration.

If dependencies need to be synchronized manually inside the development container:

```bash
docker compose exec web uv sync
```

### Adding a Runtime Dependency

```bash
docker compose exec web uv add <package>
```

Example:

```bash
docker compose exec web uv add django-filter
```

### Adding a Development Dependency

```bash
docker compose exec web uv add --dev <package>
```

Example:

```bash
docker compose exec web uv add --dev pytest
```

After changing dependencies, commit both `pyproject.toml` and `uv.lock` when they have changed.

---

## Database Migrations

Apply all existing Django migrations:

```bash
docker compose exec web uv run python manage.py migrate
```

Check migration status:

```bash
docker compose exec web uv run python manage.py showmigrations
```

When model changes require new migrations:

```bash
docker compose exec web uv run python manage.py makemigrations
```

Then apply them:

```bash
docker compose exec web uv run python manage.py migrate
```

---

## Create an Administrator

Create a Django superuser:

```bash
docker compose exec web uv run python manage.py createsuperuser
```

Follow the prompts to provide the username, email address, and password.

---

## Access the Application

Once the containers are running, the Django application is available at:

```text
http://localhost:8000/
```

### Django Admin

The Django administration interface is available at:

```text
http://localhost:8000/admin/
```

Log in using the superuser account created earlier.

---

## Django System Check

Verify that the Django configuration is valid:

```bash
docker compose exec web uv run python manage.py check
```

A successful result should report:

```text
System check identified no issues (0 silenced).
```

---

## Run Tests

The project uses `pytest` and `pytest-django`.

Run the complete test suite:

```bash
docker compose exec web uv run pytest
```

Tests that require database access use a separate Django test database and do not operate directly on the normal development database.

See [Testing](testing.md) for more information about the project's testing conventions.

---

## Code Quality

The project uses Ruff for linting and formatting.

### Check Code

```bash
docker compose exec web uv run ruff check .
```

### Automatically Fix Supported Ruff Issues

```bash
docker compose exec web uv run ruff check . --fix
```

### Format Code

```bash
docker compose exec web uv run ruff format .
```

### Check Formatting Without Modifying Files

```bash
docker compose exec web uv run ruff format --check .
```

---

## Static Type Checking

The project uses mypy for static type checking.

Run mypy with:

```bash
docker compose exec web uv run mypy
```

---

## Complete Validation

Tox provides the common interface for running the project's automated validation suite.

Run:

```bash
docker compose exec web uv run tox
```

The validation suite includes:

- pytest
- Ruff lint checks
- Ruff formatting validation
- mypy static type checking
- Django system checks
- MkDocs documentation validation

Individual tox environments can also be executed separately.

For example:

```bash
docker compose exec web uv run tox run -e tests
```

or:

```bash
docker compose exec web uv run tox run -e lint
```

---

## Pre-commit

The project uses pre-commit hooks to catch common problems before commits are created.

Install the hooks when setting up the repository:

```bash
docker compose exec web uv run pre-commit install
```

Run all hooks manually:

```bash
docker compose exec web uv run pre-commit run --all-files
```

Pre-commit performs checks such as:

- Ruff linting
- Ruff formatting
- Trailing whitespace detection
- End-of-file fixing
- YAML validation
- TOML validation
- Accidental large-file detection

If a configured hook fails, the commit is prevented until the issue is resolved.

---

## Documentation

Project documentation is built with MkDocs.

Build the documentation:

```bash
docker compose exec web uv run mkdocs build --strict
```

The documentation build can also be validated through tox:

```bash
docker compose exec web uv run tox run -e docs
```

To serve the documentation locally:

```bash
docker compose exec web uv run mkdocs serve --dev-addr=0.0.0.0:8001
```

If port `8001` is exposed by Docker Compose, the documentation can then be opened at:

```text
http://localhost:8001/
```

---

## Continuous Integration

GitHub Actions automatically validates the project on configured pushes and pull requests.

The CI pipeline prepares Python 3.13, `uv`, and PostgreSQL, synchronizes dependencies from the lockfile, and executes the tox validation suite.

Before pushing code, developers should preferably run:

```bash
docker compose exec web uv run tox
```

This helps ensure that the same validation checks executed by CI already pass locally.

---

## Stop the Development Environment

Stop the containers:

```bash
docker compose down
```

This does not delete the PostgreSQL Docker volume, so database data remains available the next time the containers are started.

Start them again with:

```bash
docker compose up -d
```

---

## Reset the Development Database

> **Warning:** The following command deletes the PostgreSQL Docker volume and therefore removes the local development database.

Stop the containers and remove their volumes:

```bash
docker compose down -v
```

Then rebuild/start the environment:

```bash
docker compose up --build -d
```

Apply migrations again:

```bash
docker compose exec web uv run python manage.py migrate
```

Create a new superuser if required:

```bash
docker compose exec web uv run python manage.py createsuperuser
```

---

## Typical Development Workflow

A normal development session looks like:

```bash
# Start the environment
docker compose up -d

# Make code changes

# Run tests
docker compose exec web uv run pytest

# Run the complete validation suite
docker compose exec web uv run tox

# Run pre-commit checks
docker compose exec web uv run pre-commit run --all-files

# Commit changes
git add .
git commit -m "Describe the change"

# Push changes
git push
```

GitHub Actions will then run the CI validation suite against the pushed code.
