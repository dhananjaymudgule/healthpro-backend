# Configuration Guide

## Environment Variables
The following environment variables must be configured for the application to run properly.

### 1. Database Settings
```
DATABASE_URL=postgresql://user:password@host/dbname
```

### 2. Security Settings
```
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Email Settings (SMTP Configuration)
```
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

### 4. Deployment Settings
```
DEBUG=True  # Set to False in production
```

## Updating Configuration
Modify `.env` file for local development and update secrets in the deployment platform.

---
Your application is now properly configured! ✅

