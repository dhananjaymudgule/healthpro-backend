# Deployment Guide

## 1. Running Locally

### Using Uvicorn
```sh
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Using Docker
```sh
docker-compose up --build
```

## 2. Deploying to Render

1. **Create a Render account** and set up a new web service.
2. **Connect your GitHub repository**.
3. **Set environment variables** in Render’s dashboard.
4. **Deploy** by clicking "Manual Deploy" or pushing new changes to GitHub.

## 3. Deploying with Docker

### Build and Push Docker Image
```sh
docker build -t yourdockerhubusername/healthpro:latest .
docker push yourdockerhubusername/healthpro:latest
```

### Deploy to a Cloud Provider (AWS, GCP, DigitalOcean, etc.)
- **AWS:** Use **ECS** or **Lightsail**
- **GCP:** Use **Cloud Run**
- **DigitalOcean:** Use **App Platform**

## 4. Database Migration
Before starting the application in production, run:
```sh
alembic upgrade head
```

## 5. Environment Variables
Ensure the following `.env` variables are set:
```
DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 6. Monitoring & Logging
Use logging tools like:
- **Prometheus + Grafana** for monitoring
- **ELK Stack** for centralized logging

---
Your HealthPro API is now ready for production! 🚀

