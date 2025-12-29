# Todo App - Hackathon II

## Project Overview

This is a complete todo application with secure user authentication and comprehensive task management features. The application provides users with the ability to create, view, update, and delete tasks while ensuring data isolation between users.

### Features
- User registration and authentication with JWT
- Secure password storage with bcrypt
- Task management (Create, Read, Update, Delete)
- User data isolation
- Responsive web interface

### Tech Stack
- **Backend**: Python 3.13+, FastAPI, SQLModel, PostgreSQL
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Authentication**: JWT-based with bcrypt password hashing
- **Database**: PostgreSQL (Neon for production, SQLite for development)

## Project Structure

```
├── backend/                 # FastAPI backend application
│   ├── src/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # Data models
│   │   ├── services/      # Business logic
│   │   ├── storage/       # Data access layer
│   │   └── core/          # Core utilities and config
│   └── tests/             # Backend tests
├── frontend/               # Next.js frontend application
│   ├── app/               # Next.js 14 App Router pages
│   ├── components/        # React components
│   ├── lib/               # Utilities and API client
│   ├── contexts/          # React Context providers
│   └── tests/             # Frontend tests
├── specs/                  # SDD specifications
│   └── features/          # Feature specifications
└── docs/                   # Documentation
```

## Current Implementation Status

### ✅ Working Features
- [x] User registration with email and password
- [x] User authentication with JWT tokens
- [x] Secure password hashing with bcrypt
- [x] Task creation with user association
- [x] Task retrieval for authenticated users
- [x] User data isolation (users can only access their own tasks)
- [x] Frontend authentication flow (login/register)
- [x] Basic task management interface

### 🔄 In Progress Features
- [ ] Complete task update functionality
- [ ] Task deletion functionality
- [ ] Advanced task filtering and sorting
- [ ] Comprehensive error handling
- [ ] Complete test coverage

### 📋 Specification Compliance
- [x] User registration requirement
- [x] User authentication requirement
- [x] Create task requirement
- [x] View tasks requirement (basic)
- [ ] Update task requirement
- [ ] Delete task requirement
- [ ] Mark complete requirement

## Setup and Development

### Prerequisites
- Python 3.13+
- Node.js 18+
- PostgreSQL (or SQLite for development)
- pnpm or npm

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Configuration
Create `.env` files in both directories:

**backend/.env:**
```env
DATABASE_URL=sqlite:///./todo_app.db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRATION_HOURS=24
```

**frontend/.env.local:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Documentation

### Authentication Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user (returns JWT)
- `GET /auth/me` - Get current user info (requires JWT)

### Task Endpoints
- `GET /tasks` - Get user's tasks (requires JWT)
- `POST /tasks` - Create new task (requires JWT)
- `GET /tasks/{task_id}` - Get specific task (requires JWT)
- `PUT /tasks/{task_id}` - Update task (requires JWT)
- `DELETE /tasks/{task_id}` - Delete task (requires JWT)

## Development Workflow

### SDD (Spec-Driven Development) Process
1. **Read specification**: `@specs/features/todo-app-auth-task-management.md`
2. **Create implementation plan**: `@specs/features/todo-app-auth-task-management.plan.md`
3. **Define tasks**: `@specs/features/todo-app-auth-task-management.tasks.md`
4. **Implement features**
5. **Test thoroughly**
6. **Document changes**

### Current Implementation Plan
The project follows the SDD approach with the following implementation plan:
- **Phase 1**: Backend foundation (complete)
- **Phase 2**: Frontend foundation (complete)
- **Phase 3**: Integration and testing (in progress)
- **Phase 4**: Optimization and deployment (pending)

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
# Unit tests
npm run test
# E2E tests
npx playwright test
```

## Deployment

### Backend
- Deploy to Heroku, Railway, or similar Python hosting
- Configure environment variables
- Set up PostgreSQL database

### Frontend
- Deploy to Vercel, Netlify, or similar static hosting
- Configure environment variables
- Point to production backend API

## Security Considerations

- Passwords are hashed with bcrypt (12 rounds minimum)
- JWT tokens have 24-hour expiration
- User data is isolated at database and API levels
- Input validation on both frontend and backend
- CORS configured for production domains only

## Contributing

1. Read the feature specification
2. Follow the SDD workflow
3. Write tests for new functionality
4. Maintain existing functionality
5. Update documentation as needed

## Troubleshooting

### Common Issues
- **CORS errors**: Check backend CORS configuration
- **JWT validation**: Verify JWT secret configuration
- **Database connection**: Ensure database URL is correct
- **Authentication**: Verify token is properly passed in requests

### Debugging API
```bash
# Test registration
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User", "password": "password123"}'

# Test login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=test@example.com&password=password123'

# Test task creation (with token)
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Test Task", "description": "Test Description"}'
```

## Project Status
- **Backend**: 90% complete (all endpoints working)
- **Frontend**: 80% complete (authentication and basic task UI)
- **Testing**: 60% complete (basic functionality tested)
- **Documentation**: 70% complete

## Next Steps
1. Complete remaining task management functionality (update, delete)
2. Implement comprehensive error handling
3. Add advanced filtering and sorting
4. Complete full test coverage
5. Deploy to production

---

**Created**: 2025-12-27
**Last Updated**: 2025-12-27
**Version**: Phase II - Core Implementation