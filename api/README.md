# To-Do API

A production-grade task management API built with FastAPI following clean architecture principles.

## Features

- **Authentication & Authorization**
  - JWT token authentication
  - OAuth2 password flow
  - Role-based access control
  
- **Task Management**
  - Nested todo items with priorities
  - Due dates and reminders
  - Task categorization
  - Activity logging
  
- **Collaboration**
  - Workspace-based organization
  - Task sharing between users
  - Real-time updates via WebSockets
  - Comment threads on tasks

- **Infrastructure**
  - MySQL database with connection pooling
  - Alembic database migrations
  - Structured logging with rotation
  - Automated test suite

## Technologies

**Core**
- Python 3.11
- FastAPI 0.100+
- Pydantic V2
- SQLAlchemy 2.0

**Database**
- MySQL 8.0
- Alembic (migrations)
- Redis (caching)

**Auth**
- JWT
- Bcrypt (password hashing)
- OAuth2

**DevOps**
- pytest (unit/integration tests)
- HTTPX (test client)
- pre-commit (linting)
- mypy (type checking)

## Installation

```bash
# Clone repository
git clone https://github.com/your-org/todo-api.git
cd todo-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Copy environment template:
```bash
cp dotenv_template .env
```

2. Update `.env` with your settings:
```ini
DATABASE_URL=mysql+asyncmy://user:pass@localhost/todo
JWT_SECRET_KEY=your-secret-key
REDIS_URL=redis://localhost:6379
```

3. Initialize database:
```bash
alembic upgrade head
```

## Running the API

Start the development server:
```bash
uvicorn app.main:app --reload
```

### or

```bash
python -m app.run
```

API documentation available at:
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Development Setup

```bash
# Run tests
pytest -v

# Format code
black .

# Check types
mypy app/

# Run linters
flake8 app/