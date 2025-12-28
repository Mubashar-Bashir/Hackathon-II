---
name: better-auth
description: Comprehensive Better Auth implementation for user authentication, registration, and session management. Use when setting up user authentication systems, integrating with frontend applications, implementing JWT-based sessions, and managing user data with email/password authentication.
---

# Better Auth Implementation

## Overview

This skill enables comprehensive Better Auth implementation for user authentication, registration, and session management. It provides guidance for setting up authentication systems, integrating with frontend applications, implementing JWT-based sessions, and managing user data with email/password authentication.

## Core Capabilities

### 1. Authentication Setup
- Configure Better Auth server-side components
- Set up user registration and login flows
- Implement password validation and security
- Configure email verification and password reset

### 2. Frontend Integration
- Integrate Better Auth client-side components
- Implement sign up/sign in UI flows
- Handle session state across components
- Create protected routes and authentication guards

### 3. JWT Management
- Configure JWT token generation and validation
- Set token expiration and refresh mechanisms
- Handle token storage and security
- Implement secure token transmission

### 4. User Management
- Manage user profiles and account settings
- Handle user data privacy and security
- Implement role-based access control
- Create user session management

## Quick Start

1. Configure Better Auth server-side with your database
2. Set up client-side integration in your frontend
3. Implement authentication routes and guards
4. Add user profile and management features

## Server-Side Configuration Examples

### Better Auth Setup with Database
```python
# backend/main.py
from better_auth import auth_app
from better_auth.config import Config
from better_auth.database import Database
from better_auth.models import User

# Configure Better Auth with database
config = Config(
    secret="your-secret-key-here",  # Should come from environment
    database_url="postgresql://user:pass@localhost/dbname",
    # Additional configuration
)

# Initialize auth app
app = auth_app(config)

# Add authentication routes
app.include_router(auth_router)
```

### JWT Token Validation for FastAPI
```python
# backend/core/auth.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from typing import Optional
import jwt
from pydantic import BaseModel

from .config import settings
from ..models.user import User

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

def verify_token(token: str) -> TokenData:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        if user_id is None or email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return TokenData(user_id=user_id, email=email)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def get_current_user(credentials: HTTPBearer = Depends(security)) -> User:
    """Get current user from JWT token."""
    token = credentials.credentials
    token_data = verify_token(token)
    user = get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

## Frontend Integration Examples

### Next.js Client Setup
```typescript
// lib/auth.ts
import { createAuthClient } from 'better-auth/client';

export const auth = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  // Additional configuration
});
```

### Authentication Hook
```typescript
// hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { auth } from '@/lib/auth';

export function useAuth() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const session = await auth.getSession();
        setUser(session?.user || null);
      } catch (error) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const result = await auth.signIn.email({ email, password });
      setUser(result.user);
      return result;
    } catch (error) {
      throw error;
    }
  };

  const signOut = async () => {
    try {
      await auth.signOut();
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  return { user, loading, signIn, signOut };
}
```

### Protected Route Component
```typescript
// components/ProtectedRoute.tsx
'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { ReactNode, useEffect } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
  fallback?: ReactNode;
}

export function ProtectedRoute({
  children,
  fallback = <div>Loading...</div>
}: ProtectedRouteProps) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/signin');
    }
  }, [user, loading, router]);

  if (loading) {
    return fallback;
  }

  if (!user) {
    return null;
  }

  return <>{children}</>;
}
```

## Resources

### scripts/
- `setup-auth.py` - Better Auth server-side setup utility
- `generate-auth-routes.py` - Authentication route generator
- `migrate-users.py` - User database migration script

### references/
- `auth-best-practices.md` - Authentication security guidelines
- `jwt-configuration.md` - JWT token configuration guide
- `user-management.md` - User data handling patterns

### assets/
- `auth-templates/` - Authentication flow templates
- `component-templates/` - Auth UI component templates
