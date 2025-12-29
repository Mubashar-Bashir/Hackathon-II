# API Contract: Authentication Endpoints

## Base URL
`/auth`

## Endpoints

### POST /auth/register
**Description**: Register a new user account

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Request Validation**:
- Email: Valid email format
- Password: Minimum 8 characters with mixed case, numbers, special characters

**Success Response (201)**:
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "message": "User registered successfully"
}
```

**Error Responses**:
- 400: VALIDATION_ERROR - Invalid input
- 409: USER_EXISTS - Email already registered

### POST /auth/login
**Description**: Authenticate user and return JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200)**:
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Error Responses**:
- 401: INVALID_CREDENTIALS - Invalid email/password
- 400: VALIDATION_ERROR - Invalid input

### GET /auth/me
**Description**: Get authenticated user information

**Headers**:
- Authorization: Bearer {jwt_token}

**Success Response (200)**:
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "name": "User Name"
}
```

**Error Responses**:
- 401: UNAUTHORIZED - Invalid or expired token
- 403: FORBIDDEN - Insufficient permissions

### POST /auth/logout
**Description**: Logout user and invalidate token (optional)

**Headers**:
- Authorization: Bearer {jwt_token}

**Success Response (200)**:
```json
{
  "message": "Successfully logged out"
}
```

**Error Responses**:
- 401: UNAUTHORIZED - Invalid token