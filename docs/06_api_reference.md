# API Reference
```
src/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── users.py  <-- Registers routes from modules/users/routes.py
│   ├── modules/
│   │   ├── users/
│   │   │   ├── routes.py  <-- Defines user-related API endpoints
│   ├── main.py  <-- Registers routes globally
```


```src/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── patients.py  <-- Register patient-related routes
│   ├── modules/
│   │   ├── patients/
│   │   │   ├── routes.py  <-- Defines /api/v1/patient-info/{user_id} endpoint
│   │   │   ├── models.py  <-- PatientInfo database model
│   │   │   ├── schemas.py  <-- Pydantic models
│   │   │   ├── services.py  <-- Business logic for patient info
│   ├── main.py  <-- Registers API routes
```

## Users Endpoints

### Signup
`POST /api/v1/users/signup`
Registers a new user after verifying their email.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "password": "securepassword",
  "role": "patient"
}
```
**Response:**
```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "johndoe@example.com",
  "role": "patient",
  "is_active": true
}
```

### Login
`POST /api/v1/users/login`
Authenticates the user and returns access and refresh tokens.

### Logout
`POST /api/v1/users/logout`
Clears the refresh token, logging the user out.

### Refresh Token
`POST /api/v1/users/refresh`
Issues a new access token using a refresh token.

### Verify Email
`POST /api/v1/users/verify-email`
Verifies the user's email before signup.

### Password Reset
- `POST /api/v1/users/password-reset`: Sends a password reset link.
- `POST /api/v1/users/password-reset/confirm`: Confirms password reset.

---




# Contributing

## How to Contribute
1. Fork the repository and clone it.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit (`git commit -m "Add new feature"`).
4. Push your changes (`git push origin feature-name`).
5. Open a pull request.

## Code Style
- Follow **PEP 8** coding standards.
- Use **type hints** for better readability.
- Ensure tests pass before submitting a PR.

---




