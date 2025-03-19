# Database Migrations

## Setup Database
```bash
docker-compose up -d
docker exec -it db psql -U user -d database
```

## Running Migrations
```bash
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

---

1. alembic init alembic

2. Update `env.py`

3. alembic revision --autogenerate -m "Initial migration"

4. alembic upgrade head