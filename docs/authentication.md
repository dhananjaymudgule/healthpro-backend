# Authentication

## Email Verification

✅ How It Works
Step 1: User enters their email → A verification link is sent.
Step 2: When they click the link, the frontend extracts the token and sends it along with the signup data to /signup.
Step 3: Backend verifies the token and creates the user in the database.

## JWT Authentication Flow
1. User logs in with email & password.
2. Server validates credentials and returns access & refresh tokens.
3. Access token is used for API requests.
4. If the access token expires, the refresh token is used to get a new one.
5. User can log out to revoke refresh tokens.

## Roles & Permissions
- **Admin** – Can manage users and the system.
- **Doctor** – Can interact with patients.
- **Patient** – Can access their health data.


---