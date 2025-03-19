# Getting Started

Welcome to the HealthPro API project! This guide will help you quickly set up and run the project.

## Prerequisites
- Python 3.12.3
- PostgreSQL Database
- Redis (Optional, if used for caching)
- Docker & Docker Compose (Optional, for containerized setup)
- Git

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/yourusername/healthpro.git
   cd healthpro
   ```

2. **Create and Activate Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Copy `.env.example` to `.env` and update necessary values:
   ```sh
   cp .env.example .env
   ```

5. **Run Database Migrations:**
   ```sh
   alembic upgrade head
   ```

6. **Start the Application:**
   ```sh
   uvicorn src.app.main:app --reload
   ```

7. **Access API Docs:**
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view Swagger UI.

## Running with Docker

1. **Build and Start Containers:**
   ```sh
   docker-compose up --build
   ```

2. **Check Running Containers:**
   ```sh
   docker ps
   ```

## Running Tests
   ```sh
   pytest
   ```

## Contributing
Check out the [contributing guide](contributing.md) for guidelines on how to contribute to this project.

---
Now you are ready to develop with HealthPro API! 🚀

