# API

The Kindergarten Management System uses **Django REST Framework** for its REST API.

API documentation is generated using OpenAPI/Swagger tooling configured by the project.

## Purpose

The API layer will expose kindergarten management functionality to authorized clients.

Planned API domains include:

- Resources
- Children
- Groups
- Parents
- Fees
- Library
- Contracts
- Cleaning schedules

The exact endpoint structure will be documented as these modules are implemented.

---

## API Design

API endpoints should follow consistent REST conventions.

Typical operations include:

```text
GET     Retrieve resources
POST    Create a resource
PUT     Replace a resource
PATCH   Update a resource
DELETE  Delete a resource
```

Not every endpoint is required to support every operation.

Permissions and available operations depend on the corresponding business requirements.

---

## API Documentation

Interactive API documentation should be generated from the application's OpenAPI schema.

As endpoints are implemented, this documentation should describe:

- endpoint path
- HTTP method
- request body
- query parameters
- authentication requirements
- permissions
- response structure
- status codes
- validation errors

---

## Testing

API endpoints should have automated tests.

Typical location:

```text
<application>/
└── tests/
    └── test_api.py
```

API tests should verify successful behavior as well as authentication, permissions, validation, and expected error responses.

---

## Future Documentation

This page will grow alongside the API implementation.

Detailed endpoint documentation should only be added after the corresponding functionality exists.
