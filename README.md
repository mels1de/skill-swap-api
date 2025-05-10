#Skill Swap API

**Skill Swap** is a backend API for a skill swap platform. It is implemented using **FastAPI**, **PostgreSQL**, **JWT** authentication and asynchronous database handling.

---

##  Features

- **Registration and authorization of users**
- **JWT authentication** with endpoint protection
- **Asynchronous work with PostgreSQL** via SQLAlchemy (Async ORM)
- **Password hashing** using bcrypt (Passlib)
- **Data Validation** using Pydantic
- **Separation of business logic and routes**
- **Ready to containerize with Docker** (planned)
- **Expandable and clean code**, ready to scale

---

## Technology Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Passlib (bcrypt)
- Pydantic
- Uvicorn
- Alembic (planned)
- Docker (planned)

---

## 📁 Project structure
![image](https://github.com/user-attachments/assets/de93c874-1f86-45cc-aeec-f2efb1a1152b)


---

## Installing and deployment

### 1. Clone repository:
git clone https://github.com/<your-username>/skill-swap-api.git
cd skill-swap-api

### 2. Create venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

### 3. Install dependencies:
pip install -r requirements.txt

### 4. Add .env file:
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost/skill_swap_db
SECRET_KEY=your-secret-key

### 5. Launch server:
uvicorn app.main:app --reload


---


Usage instance:
# Registration
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"securepass"}'

# Logining
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepass"

# Getting current user
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <access_token>"


---

Pydantic validators provide reliable input validation.

Upcoming plans:

Docker containerization
Alembic migrations
Swagger UI fixes (done)






