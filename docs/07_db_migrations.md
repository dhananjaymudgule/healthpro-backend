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



```
src/
├── app/
│   ├── db/
│   │   ├── models/              # Database models (ORM)
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   ├── repositories/        # CRUD operations for models
│   │   │   ├── user_repository.py
│   │   │   ├── patient_repository.py
│   │   ├── session.py           # DB session handling
│   ├── modules/
│   │   ├── users/
│   │   │   ├── services.py       # Business logic for users
│   │   │   ├── routes.py         # API endpoints
│   │   ├── patients/
│   │   │   ├── services.py       # Business logic for patients
│   │   │   ├── routes.py         # API endpoints
```



# **📌 Database Migration Documentation (PostgreSQL + Alembic)**
🚀 This guide will help you set up and run database migrations for the **HealthPro** project using **PostgreSQL, SQLAlchemy (async), and Alembic**.

---

## **📌 1️⃣ Prerequisites**
Before running migrations, make sure you have:
- **Python 3.12+**
- **PostgreSQL Installed** (or use Docker)
- **PGAdmin** (optional, for GUI database management)
- **Alembic Installed** (`pip install alembic`)

---

## **📌 2️⃣ Setting Up PostgreSQL (If Not Installed)**
🔹 If PostgreSQL is not installed, follow these steps:

### **📌 Install PostgreSQL (Windows)**
1. Download & install PostgreSQL from 👉 [PostgreSQL Official Site](https://www.postgresql.org/download/)
2. During installation, set the **username** (`postgres`) and **password** (e.g., `securepassword`)
3. Open **pgAdmin** to manage the database easily

### **📌 Create Database**
Run this command to create a new database:
```sql
CREATE DATABASE healthpro_db;
```

---

## **📌 3️⃣ Configure Database in `.env`**
🔹 **Inside the project, create a `.env` file** and add your database connection:

```ini
DATABASE_URL=postgresql+asyncpg://postgres:securepassword@localhost:5432/healthpro_db
```
✅ **Ensure that `asyncpg` is used for async database operations**.

---

## **📌 4️⃣ Initialize Alembic**
🔹 Run the following command **only once** to set up Alembic in the project:
```bash
alembic init alembic
```
🔹 This creates an `alembic/` directory inside the project.

---

## **📌 5️⃣ Update `alembic/env.py` for Async PostgreSQL**
Since Alembic **does not support async PostgreSQL (`asyncpg`)**, we need to modify `env.py` to use `psycopg2` **only for migrations**.

### **🔹 Open `alembic/env.py` and Find This Line**
```python
from src.app.db.session import engine
```
🔹 **Replace it with:**
```python
from sqlalchemy import create_engine
from src.app.core.config import settings

# ✅ Convert asyncpg → psycopg2 (sync) just for Alembic migrations
SYNC_DATABASE_URL = settings.DATABASE_URL.replace("asyncpg", "psycopg2")

connectable = create_engine(SYNC_DATABASE_URL)
```
✅ **This ensures that Alembic migrations work while keeping your app async.**

---

## **📌 6️⃣ Running Migrations**
After configuring Alembic, you can now run migrations.

### **🔹 1️⃣ Create a Migration File**
```bash
alembic revision --autogenerate -m "Initial migration"
```
🔹 This will generate a migration file inside `alembic/versions/`.

### **🔹 2️⃣ Apply the Migration to the Database**
```bash
alembic upgrade head
```
🔹 This will **create tables** in the PostgreSQL database.

---

## **📌 7️⃣ Verify Database Migration**
### **🔹 Check If Tables Exist**
Run the following **PostgreSQL command**:
```bash
psql -U postgres -d healthpro_db -c "\dt"
```
🔹 This should list tables like **`users`, `patients`**.

### **🔹 Check Table Data**
Run:
```bash
psql -U postgres -d healthpro_db -c "SELECT * FROM users;"
```
🔹 This will display user records.

---

## **📌 8️⃣ Reset Migrations (If Needed)**
If migrations break, you can reset them.

### **🔹 1️⃣ Drop Alembic Migration History**
```bash
psql -U postgres -d healthpro_db -c "DROP TABLE IF EXISTS alembic_version CASCADE;"
```

### **🔹 2️⃣ Delete Existing Alembic Migrations**
```bash
rm -rf alembic/versions/*
```

### **🔹 3️⃣ Recreate Migrations**
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## **📌 9️⃣ Folder Structure**
```bash
src/
├── app/
│   ├── db/
│   │   ├── models/              # Database models (ORM)
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   ├── repositories/        # CRUD operations for models
│   │   │   ├── user_repository.py
│   │   │   ├── patient_repository.py
│   │   ├── session.py           # DB session handling
│   ├── modules/
│   │   ├── users/
│   │   │   ├── services.py       # Business logic for users
│   │   │   ├── routes.py         # API endpoints
│   │   ├── patients/
│   │   │   ├── services.py       # Business logic for patients
│   │   │   ├── routes.py         # API endpoints
├── alembic/                      # Migration folder
│   ├── versions/                  # Auto-generated migration scripts
│   ├── env.py                     # Alembic configuration
│   ├── README                      # Alembic documentation
├── .env                           # Environment variables (Database URL)
```

---

## **📌 10️⃣ Summary Table**
| **Step** | **Command** |
|----------|------------|
| **1️⃣ Install PostgreSQL** | [Download PostgreSQL](https://www.postgresql.org/download/) |
| **2️⃣ Create Database** | `CREATE DATABASE healthpro_db;` |
| **3️⃣ Set Up `.env`** | `DATABASE_URL=postgresql+asyncpg://postgres:securepassword@localhost:5432/healthpro_db` |
| **4️⃣ Initialize Alembic** | `alembic init alembic` |
| **5️⃣ Fix `env.py`** | Use `psycopg2` for migrations |
| **6️⃣ Create Migration** | `alembic revision --autogenerate -m "Initial migration"` |
| **7️⃣ Apply Migration** | `alembic upgrade head` |
| **8️⃣ Verify Tables** | `psql -U postgres -d healthpro_db -c "\dt"` |
| **9️⃣ Reset Migrations** | `DROP TABLE alembic_version;` → `rm -rf alembic/versions/*` |

---

## **✅ Now Your Database is Fully Set Up!** 🚀
### **Next Steps**
1. **Push your code to GitHub** 📌  
2. **Deploy using Docker or CI/CD** (if needed)  
3. **Test API using FastAPI & PostgreSQL**  

