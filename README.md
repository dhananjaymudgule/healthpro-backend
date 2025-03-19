# HealthPro - A Health Tech Platform

## Overview
HealthPro is a FastAPI-based health tech platform designed for user onboarding with authentication and role-based access control (RBAC). The platform supports email verification, password-based authentication, token-based authorization, and password reset functionalities.

## Features
- User Registration with Email Verification
- Role-Based Access Control (RBAC) (Admin, Doctor, Patient)
- Secure Authentication (JWT Tokens - Access & Refresh)
- Password Reset via Email
- Logout and Token Revocation
- API Documentation via Swagger UI

## Project Structure
```
my_fastapi_project/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── users.py
│   │   │   │   ├── items.py
│   │   ├── modules/
│   │   │   ├── users/
│   │   │   │   ├── routes.py          # User-related API endpoints (Signup, Login, Logout, Password Reset)
│   │   │   │   ├── dependencies.py    # User-specific dependencies
│   │   │   │   ├── services.py        # Business logic for onboarding users
│   │   │   │   ├── schemas.py         # Pydantic models for request validation
│   │   │   │   ├── models.py          # User database model
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py            # Authentication & password hashing utilities
│   │   │   ├── exceptions.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── models/
│   │   │   │   ├── user.py             # Database model for user onboarding
│   │   │   ├── repositories/
│   │   │   │   ├── user_repository.py  # CRUD operations for users
│   │   ├── tasks/
│   │   │   ├── email.py               # Email verification tasks
│   │   ├── main.py
├── tests/
│   ├── test_users/
│   │   ├── test_routes.py         # Test user onboarding API
├── Dockerfile
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
```

## Installation
### Prerequisites
- Python 3.12.3
- PostgreSQL Database
- Docker (optional for containerized deployment)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/healthpro.git
   cd healthpro
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Copy `.env.example` to `.env` and update the values as per your database and email settings.

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the FastAPI server:
   ```bash
   uvicorn src.app.main:app --reload
   ```

## API Endpoints
### Authentication & User Management
| Method | Endpoint                         | Description                    |
|--------|----------------------------------|--------------------------------|
| POST   | `/api/v1/users/verify-email`     | Verify email before signup    |
| POST   | `/api/v1/users/signup`           | Register new user             |
| POST   | `/api/v1/users/login`            | Authenticate user             |
| POST   | `/api/v1/users/logout`           | Logout user                   |
| POST   | `/api/v1/users/refresh`          | Refresh access token          |
| GET    | `/api/v1/users/me`               | Get user profile              |
| POST   | `/api/v1/users/password-reset`   | Request password reset email  |
| POST   | `/api/v1/users/password-reset/confirm` | Reset password      |

### Admin & User Management
| Method | Endpoint                         | Description                    |
|--------|----------------------------------|--------------------------------|
| GET    | `/api/v1/users/admin`            | Admin-only dashboard           |
| GET    | `/api/v1/users/list`             | List all users (Admin only)    |

### API Documentation
Once the server is running, access API docs:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t healthpro .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env healthpro
   ```

## Contributing
1. Fork the repository.
2. Create a new branch (`feature-xyz`).
3. Commit your changes.
4. Push to your branch and create a Pull Request.

## License
This project is licensed under the MIT License.

