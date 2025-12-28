# Quickstart: Phase II: Core - Neon DB Schema & Better Auth JWT Integration

## Prerequisites
- Python 3.13+
- uv package manager
- Neon PostgreSQL database instance
- BETTER_AUTH_SECRET environment variable

## Setup

### 1. Environment Configuration
```bash
# Set up environment variables
export DATABASE_URL="postgresql://username:password@neon-host.region.aws.neon.tech/dbname"
export BETTER_AUTH_SECRET="your-secret-key-here"
export JWT_EXPIRATION_HOURS=24
```

### 2. Install Dependencies
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install fastapi sqlmodel pyjwt better-auth psycopg2-binary
```

### 3. Database Setup
```bash
# Run database migrations
python -m src.core.database migrate
```

## Usage

### 1. Start the Server
```bash
cd backend
uvicorn src.main:app --reload
```

### 2. Register a User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Login to Get JWT Token
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### 4. Use JWT Token for Task Operations
```bash
# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Task",
    "description": "Task description",
    "status": "pending",
    "priority": "medium"
  }'
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout and invalidate token
- `GET /auth/me` - Get current user info

### Tasks
- `GET /tasks` - Get all tasks for authenticated user
- `POST /tasks` - Create new task for authenticated user
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update specific task
- `DELETE /tasks/{id}` - Delete specific task

## Error Responses

All error responses follow the format:
```json
{
  "message": "Error description",
  "error_code": "ERROR_CODE"
}
```

Common error codes:
- `UNAUTHORIZED`: Invalid or missing JWT token
- `FORBIDDEN`: User doesn't have access to resource
- `VALIDATION_ERROR`: Request data doesn't meet requirements
- `NOT_FOUND`: Requested resource doesn't exist