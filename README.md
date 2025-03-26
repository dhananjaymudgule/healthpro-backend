# **HealthPro - A Health Tech Platform**  

## **Overview**  
HealthPro is a **FastAPI-based** health tech platform designed to support **user authentication, onboarding, and role-based access control (RBAC)**. It provides **secure user registration, authentication, email verification, patient record management, and JWT-based authorization**.

---

## **Features**
✅ **User Authentication & Role-Based Access Control (RBAC)** (Admin, Doctor, Patient)  
✅ **JWT Token Authentication** (Access & Refresh Tokens)  
✅ **Email Verification & Password Reset**  
✅ **CRUD Operations for Users & Patients**  
✅ **PostgreSQL Database with Async SQLAlchemy & Alembic Migrations**  
✅ **Docker Support for Easy Deployment**  

---

## **Project Structure**
```
healthpro-backend/
├── src/
│   ├── app/
│   │   ├── core/                  # Configuration & security utilities
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   ├── db/
│   │   │   ├── models/                # Database models
│   │   │   │   ├── user.py
│   │   │   │   ├── patient.py
│   │   │   ├── repositories/          # CRUD operations
│   │   │   │   ├── user_repository.py
│   │   │   │   ├── patient_repository.py
│   │   │   ├── session.py             # Async DB session handling
│   │   ├── modules/
│   │   │   ├── users/                 # User authentication & management
│   │   │   │   ├── routes.py
│   │   │   │   ├── services.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── dependencies.py    # User-specific dependencies
│   │   │   ├── patients/              # Patient record management
│   │   │   │   ├── routes.py
│   │   │   │   ├── services.py
│   │   │   │   ├── schemas.py
│   │   ├── main.py                  # FastAPI entry point
│   ├── tests/                       # Unit & integration tests
├── alembic/                         # Database migrations
├── docs/                            # Detailed documentation
├── uploads/                         # Uploaded files
├── venv/                            # When you create venv
├── Dockerfile
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
├── README.md
```

---

## **Installation & Setup**  

### **Prerequisites**  
- ✅ **Python 3.12.3**  
- ✅ **PostgreSQL (Recommended: v17+)**  
- ✅ **Docker** (Optional for containerized deployment)

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/healthpro.git
cd healthpro-backend
```

### **2️⃣ Set Up a Virtual Environment**  
```bash
python -m venv venv

source venv/bin/activate # on Macos

venv\Scripts\activate # On Windows
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**  
Copy the `.env.example` file to `.env` and update database credentials:  
```
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/healthpro_db
SECRET_KEY=your-secret-key
```

---

## **Database Migrations**  
💾 **Ensure PostgreSQL is running before running migrations.**  
```bash
alembic upgrade head  # Apply database migrations
```
To create a new migration after model changes:  
```bash
alembic revision --autogenerate -m "Describe migration change"
alembic upgrade head
```

---

## **Running the Server**  
🚀 **Start FastAPI with Uvicorn**  
```bash
uvicorn src.app.main:app --reload
```
✅ Visit the API documentation at:  
- [Swagger UI](http://127.0.0.1:8000/docs)  
- [ReDoc](http://127.0.0.1:8000/redoc)  

---

## **API Endpoints**  
### **🔐 Authentication & User Management**
| Method | Endpoint                         | Description                    |
|--------|----------------------------------|--------------------------------|
| POST   | `/api/v1/users/verify-email`     | Send email verification link  |
| POST   | `/api/v1/users/signup`           | Register new user             |
| POST   | `/api/v1/users/login`            | Authenticate user             |
| POST   | `/api/v1/users/logout`           | Logout user & revoke token    |
| POST   | `/api/v1/users/refresh`          | Refresh JWT access token      |
| GET    | `/api/v1/users/me`               | Get logged-in user profile    |
| POST   | `/api/v1/users/password-reset`   | Request password reset email  |
| POST   | `/api/v1/users/password-reset/confirm` | Reset password      |


### **📤 File Upload**  
| Method | Endpoint                        | Description   |  
|--------|---------------------------------|--------------|  
| POST   | `/api/v1/users/upload-file/`    | Upload File  |  


### **🏥 Patient Record Management**
| Method | Endpoint                      | Description                         |
|--------|--------------------------------|-------------------------------------|
| POST   | `/api/v1/patients/patient`    | Create new patient record (one per user) |
| GET    | `/api/v1/patients/patient`    | Retrieve logged-in patient info    |
| PATCH  | `/api/v1/patients/patient`    | Update specific fields in patient record |
| DELETE | `/api/v1/patients/patient`    | Delete patient record (Admin Only) |


### **🛠️ Admin & User Management**
| Method | Endpoint                    | Description                  |
|--------|-----------------------------|------------------------------|
| GET    | `/api/v1/users/admin`       | Access admin-only dashboard |
| GET    | `/api/v1/users/list`        | List all users (Admin only) |

---

## **Security & Access Control**
✅ **JWT Token Authentication**  
All protected endpoints require an **Authorization Header**:  
```
Authorization: Bearer <ACCESS_TOKEN>
```

✅ **Role-Based Access Control (RBAC)**
- **Admin** → Manage users & data  
- **Doctor** → View & update patient records  
- **Patient** → View & manage their own record  

---

## **Running with Docker**
1. **Build the Docker image**  
   ```bash
   docker build -t healthpro .
   ```
2. **Run the container**  
   ```bash
   docker run -p 8000:8000 --env-file .env healthpro
   ```
3. **Verify API is running**  
   ```bash
   curl http://127.0.0.1:8000/docs
   ```

---

## **Development & Testing**
🧪 **Run Tests**  
```bash
pytest
```

---

## **Contributing**
Want to contribute? 🚀 Follow these steps:  
1. Fork the repository.  
2. Create a new feature branch (`feature-xyz`).  
3. Commit your changes.  
4. Push to your branch and open a **Pull Request (PR)**.  

---

## **License**
📜 This project is licensed under the **License**.

---

## **🚀 Next Steps**
🔹 Deploy to **AWS, GCP, or Azure**  
🔹 Integrate **CI/CD Pipelines** (GitHub Actions)  
🔹 Improve **API Rate Limiting & Security**  

