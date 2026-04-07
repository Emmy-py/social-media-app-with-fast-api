# SOCIAL MEDIA API WITH FastAPI

A modern REST API built with **FastAPI** for managing users, posts, and voting. Features JWT authentication, PostgreSQL database integration, and comprehensive test coverage.

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Database Setup](#database-setup)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Development Notes](#development-notes)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This FastAPI application provides a complete backend for a social media platform with:

- **User Management** - Registration and profile management with JWT authentication
- **Post Management** - Create, read, update, and delete posts with ownership validation
- **Voting System** - Users can upvote/downvote posts
- **Database Migrations** - Alembic for schema versioning
- **Comprehensive Testing** - Pytest test suite with fixtures for isolated database testing
- **Automated Deployment** -  GitHub Actions CI/CD pipeline for testing and deploying to AWS EC2

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.115.0 |
| **ORM** | SQLAlchemy | 2.0.29 |
| **Database** | PostgreSQL | 12+ |
| **Migrations** | Alembic | 1.16.5 |
| **Validation** | Pydantic | ≥2.3.0 |
| **Authentication** | JWT | python-jose 3.3.0 |
| **Password Hashing** | Bcrypt | 4.1.2 |
| **Testing** | Pytest | Latest |
| **CI/CD** | GitHub Actions | Latest |
| **Deployment** | Docker + AWS EC2 | Latest |

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or conda

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/fastapi-post-app.git
cd fastapi-post-app
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Security Note:** 
- Replace `SECRET_KEY` with a strong random value in production
- Never commit `.env` to version control

### 5. Run the Server

```bash
# Development with auto-reload
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API available at `http://localhost:8000`

**Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI Schema: `http://localhost:8000/openapi.json`

## Database Setup

### 1. Create PostgreSQL Database

```bash
# Using psql
psql -U postgres

# In psql shell
CREATE DATABASE fastapi_db;
CREATE DATABASE fastapi_db_test;  -- For testing
```

### 2. Run Alembic Migrations

```bash
# Check current migration status
alembic current

# Create a new migration
alembic revision --autogenerate -m "describe_your_changes"

# Apply all pending migrations
alembic upgrade head

# Rollback to previous version
alembic downgrade -1

# View migration history
alembic history
```

### 3. Database Schema

**Users Table**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
```

**Posts Table**
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published BOOLEAN DEFAULT TRUE,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT now()
);
```

**Votes Table**
```sql
CREATE TABLE votes (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER PRIMARY KEY REFERENCES posts(id) ON DELETE CASCADE
);
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_users.py

# Run specific test function
pytest tests/test_users.py::test_create_user

# Run with coverage
pytest --cov=app tests/

# Run tests matching a pattern
pytest -k "test_login" -v
```

### Test Fixtures

The project uses three main pytest fixtures in `tests/database.py`:

**`session` Fixture**
- Provides fresh database for each test
- Automatically creates and drops tables
- Scope: Function (isolated per test)

**`client` Fixture**
- Provides TestClient with overridden database dependency
- Used to make HTTP requests in tests
- Requires `session` fixture

**Example Test**

```python
def test_create_user(client):
    """Test user creation endpoint"""
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "pass123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
```

## API Endpoints

### Authentication

**POST /login**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=yourpassword"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Users

**POST /users/** - Create user
```json
{
  "email": "newuser@example.com",
  "password": "securepassword123"
}
```

**GET /users/{id}** - Get user profile
```bash
curl -X GET "http://localhost:8000/users/1"
```

### Posts

**POST /posts/** - Create post (requires auth)
```bash
curl -X POST "http://localhost:8000/posts/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "First Post",
    "content": "This is my first post!",
    "published": true
  }'
```

**GET /posts/{id}** - Get post with vote count
```bash
curl -X GET "http://localhost:8000/posts/1"
```

**PUT /posts/{id}** - Update post (owner only)
```bash
curl -X PUT "http://localhost:8000/posts/1" \
  -H "Authorization: Bearer {token}" \
  -d '{"title": "Updated", "content": "...", "published": true}'
```

**DELETE /posts/{id}** - Delete post (owner only)
```bash
curl -X DELETE "http://localhost:8000/posts/1" \
  -H "Authorization: Bearer {token}"
```

### Votes

**POST /vote/** - Vote on a post
```bash
curl -X POST "http://localhost:8000/vote/" \
  -H "Authorization: Bearer {token}" \
  -d '{"post_id": 1, "dir": 1}'
```

## Authentication

### JWT Token-Based Authentication

The API uses **JWT (JSON Web Tokens)** for stateless authentication.

**How It Works:**
1. User logs in with email/password at `/login`
2. Server returns JWT access token
3. Client includes token in `Authorization` header
4. Server validates token on protected routes

**Using Tokens in Requests:**

```bash
curl -X GET "http://localhost:8000/posts/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Token Configuration (from .env):**
```env
ACCESS_TOKEN_EXPIRE_MINUTES=30    # Token expiration
SECRET_KEY=your-secret-key        # Signing key
ALGORITHM=HS256                   # Signing algorithm
```

**Security Best Practices:**
- ✅ Use strong SECRET_KEY (generate: `openssl rand -hex 32`)
- ✅ Set reasonable expiration time
- ✅ Use HTTPS in production
- ✅ Rotate secrets periodically
- ❌ Never hardcode secrets
- ❌ Never expose tokens in URLs

## Development Notes

### Pydantic v2 Changes

This project uses **Pydantic v2** (≥2.3.0).

**Configuration (Pydantic v2):**
```python
class UserResponse(BaseModel):
    class Config:
        from_attributes = True
```

**Serialization:**
```python
# v2 style
user_dict = user.model_dump()
user_json = user.model_dump_json()
```

**Validators:**
```python
from pydantic import field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
```

### SQLAlchemy v2 Updates

This project uses **SQLAlchemy 2.0** (2.0.29).

**Declarative Base:**
```python
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

**Query Syntax (Still Compatible):**
```python
# Legacy style still works in SQLAlchemy 2.0
user = db.query(models.User).filter(models.User.id == 1).first()
```

**Relationships:**
```python
class User(Base):
    __tablename__ = "users"
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"
    owner = relationship("User", back_populates="posts")
```

## Contributing

### Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Install dependencies: `pip install -r requirements.txt`
4. Make changes and add tests
5. Run tests: `pytest -v`
6. Commit with clear message: `git commit -m "feat: your feature"`
7. Push and create Pull Request

### Commit Message Format

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Test changes
- `refactor:` Code refactoring

Example:
```bash
git commit -m "feat(auth): add password reset functionality"
git commit -m "fix(posts): correct vote count calculation"
```

### Code Standards

- Follow PEP 8
- Add type hints to functions
- Write docstrings for complex code
- Ensure tests pass before committing

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

MIT License allows:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

See [LICENSE](LICENSE) for full details.

💡 Tip: Use the Swagger UI to test endpoints. Click Authorize, paste your JWT token, and you’ll be able to call protected routes like /posts/.
