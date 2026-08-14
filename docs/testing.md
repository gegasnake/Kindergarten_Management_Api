# Testing

The project uses **pytest** and **pytest-django** as its automated testing framework.

## Running Tests

Run all tests:

```bash
docker compose exec web uv run pytest
```

Tests are also executed as part of tox:

```bash
docker compose exec web uv run tox run -e tests
```

The complete validation suite can be run with:

```bash
docker compose exec web uv run tox
```

---

## Test Structure

Each Django application should maintain its tests inside a dedicated `tests/` package.

Example:

```text
administration/
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_models.py
    ├── test_api.py
    └── test_integration.py
```

As applications grow, the structure may be expanded further.

---

## File Naming

Test files must follow the convention:

```text
test_*.py
```

Examples:

```text
test_models.py
test_api.py
test_permissions.py
test_services.py
```

---

## Test Naming

Test functions should describe the expected behavior.

Prefer:

```python
def test_resource_can_be_created():
    ...
```

over:

```python
def test_resource():
    ...
```

Test class names should describe the component being tested:

```python
class TestResourceAPI:
    ...
```

---

## Database Tests

Tests that access the Django database should use:

```python
import pytest


@pytest.mark.django_db
def test_example():
    ...
```

or an appropriate pytest fixture that enables database access.

Django creates a separate test database for database tests.

Tests should never depend on data manually created in the development database.

---

## Fixtures

Shared pytest fixtures should be placed in:

```text
conftest.py
```

For example:

```python
import pytest


@pytest.fixture
def example_data():
    return {
        "name": "Example",
    }
```

Fixtures should be reused when they represent common test setup.

---

## Types of Tests

The project may contain several types of tests.

### Model Tests

Test model behavior, validation, methods, and relationships.

Typical location:

```text
tests/test_models.py
```

### API Tests

Test REST endpoints, status codes, request validation, authentication, permissions, and response data.

Typical location:

```text
tests/test_api.py
```

### Integration Tests

Test interactions between multiple components.

Typical location:

```text
tests/test_integration.py
```

---

## CI

Tests are automatically executed by GitHub Actions through tox.

A failing test produces a non-zero exit code, causing the CI workflow to fail.

Therefore, tests should pass locally before changes are pushed.
