# Installation

## Prerequisites
- Python 3.10+
- PostgreSQL
- Docker (optional)

## Installation Steps
```bash
git clone https://github.com/your-repo.git
cd healthpro-backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Running Locally
```bash
uvicorn src.app.main:app --reload
```
