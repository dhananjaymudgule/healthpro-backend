# Architecture

## Overview
This project is built with **FastAPI**, using a modular structure with the following key components:

- `api/` – API routes.
- `modules/` – Business logic and services.
- `db/` – Database models, session handling, and migrations.
- `core/` – Configurations, security, and authentication.
- `tasks/` – Background tasks (e.g., email sending).
- `tests/` – Unit and integration tests.

## Technologies Used
- **FastAPI** (Web Framework)
- **PostgreSQL** (Database)
- **SQLAlchemy & Alembic** (ORM & Migrations)
- **JWT** (Authentication)
- **FastAPI-Mail** (Email Service)
- **Docker** (Containerization)
- **CI/CD with GitHub Actions**

---
