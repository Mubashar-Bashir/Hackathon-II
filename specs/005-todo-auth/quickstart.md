# Quickstart Guide: Todo App with Authentication and Task Management

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ installed
- npm or yarn package manager
- PostgreSQL (or access to Neon Serverless PostgreSQL)

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Set up environment variables:
   ```bash
   # Create .env file in backend directory
   echo "DATABASE_URL=postgresql://username:password@localhost:5432/todo_app" >> .env
   echo "BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production" >> .env
   echo "JWT_EXPIRATION_HOURS=24" >> .env
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   # Create .env.local file in frontend directory
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" >> .env.local
   echo "BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production" >> .env.local
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## API Usage

### Authentication

1. **Register a new user**:
   ```bash
   curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "name": "User Name", "password": "securepassword"}'
   ```

2. **Login to get JWT token**:
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d 'username=user@example.com&password=securepassword'
   ```

### Task Management

Once you have a JWT token, you can manage tasks:

1. **Create a task**:
   ```bash
   curl -X POST http://localhost:8000/api/{user_id}/tasks \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"title": "My Task", "description": "Task description", "priority": "high"}'
   ```

2. **Get all tasks**:
   ```bash
   curl -X GET http://localhost:8000/api/{user_id}/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

3. **Update a task**:
   ```bash
   curl -X PUT http://localhost:8000/api/{user_id}/tasks/{task_id} \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"title": "Updated Task Title", "status": "in_progress"}'
   ```

4. **Complete a task**:
   ```bash
   curl -X PATCH http://localhost:8000/api/{user_id}/tasks/{task_id}/complete \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

5. **Delete a task**:
   ```bash
   curl -X DELETE http://localhost:8000/api/{user_id}/tasks/{task_id} \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## Running Tests

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Database Migrations

The application uses SQLModel with Alembic for database migrations. To create and run migrations:

1. Install alembic if not already installed:
   ```bash
   pip install alembic
   ```

2. Initialize alembic (first time only):
   ```bash
   alembic init alembic
   ```

3. Generate migration:
   ```bash
   alembic revision --autogenerate -m "Add new table"
   ```

4. Run migration:
   ```bash
   alembic upgrade head
   ```

## Deployment

### Backend Deployment
- Set environment variables for production
- Use a WSGI/ASGI server like Gunicorn for production: `gunicorn src.main:app`

### Frontend Deployment
- Build the application: `npm run build`
- Serve the build folder with a web server or deploy to Vercel/Netlify

## Troubleshooting

### Common Issues

1. **CORS errors**: Make sure your frontend and backend URLs are properly configured in the CORS settings
2. **JWT token validation errors**: Ensure the `BETTER_AUTH_SECRET` is identical in both frontend and backend
3. **Database connection errors**: Verify your PostgreSQL connection string is correct
4. **Authentication errors**: Check that the user_id in the URL matches the authenticated user's ID

### API Documentation
The API is documented with OpenAPI/Swagger. Visit `http://localhost:8000/docs` to view the interactive API documentation.