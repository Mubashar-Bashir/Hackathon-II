---
name: nextjs-frontend
description: Comprehensive Next.js 16+ application development with App Router, responsive UI, and Better Auth integration. Use when building frontend components, pages, layouts, and authentication flows for Next.js applications with Tailwind CSS styling.
---

# Next.js Frontend Development

## Overview

This skill enables comprehensive Next.js 16+ application development using the App Router architecture, with responsive UI components and Better Auth integration. It provides guidance for creating pages, components, layouts, and authentication flows following modern React and Next.js best practices.

## Core Capabilities

### 1. Page and Route Creation
- Create Next.js pages using App Router structure
- Implement nested routing with layout files
- Use React Server Components by default, Client Components only when needed

### 2. Component Development
- Build reusable UI components with TypeScript
- Implement responsive design with Tailwind CSS
- Follow Next.js and React best practices

### 3. Authentication Integration
- Setup Better Auth integration for signup/signin flows
- Create protected routes and authentication guards
- Handle session state across components

### 4. API Route Development
- Create Next.js API routes for backend communication
- Implement proper error handling and validation
- Connect with backend services

## Quick Start

1. Create a new page in `app/` directory using App Router structure
2. Use React Server Components by default, Client Components only when needed
3. Apply Tailwind CSS classes for styling
4. Integrate Better Auth using provided hooks and components

## Page Creation Examples

### Server Component Page
```typescript
// app/tasks/page.tsx
import { auth } from 'better-auth/client';
import { TaskList } from '@/components/TaskList';

export default async function TasksPage() {
  const session = await auth();

  if (!session) {
    return redirect('/signin');
  }

  return (
    <div className="container mx-auto">
      <TaskList userId={session.user.id} />
    </div>
  );
}
```

### Client Component with Interactivity
```typescript
'use client';

import { useState } from 'react';
import { createTask } from '@/lib/api';

export function TaskForm() {
  const [title, setTitle] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createTask({ title });
    setTitle('');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="border p-2 w-full"
        placeholder="Add a new task..."
      />
      <button type="submit" className="mt-2 bg-blue-500 text-white p-2">
        Add Task
      </button>
    </form>
  );
}
```

## Better Auth Integration

### Setup Authentication
```typescript
// lib/auth.ts
import { createAuthClient } from 'better-auth/client';

export const auth = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  // Additional configuration
});
```

### Protected Route Component
```typescript
// components/ProtectedRoute.tsx
'use client';

import { useAuth } from 'better-auth/react';
import { redirect } from 'next/navigation';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { data: session, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!session) {
    // Redirect to sign-in page
    return redirect('/signin');
  }

  return <>{children}</>;
}
```

## Resources

### scripts/
- `generate-component.sh` - Generate new React component boilerplate
- `setup-auth.js` - Better Auth frontend setup utility

### references/
- `nextjs-best-practices.md` - Next.js development guidelines
- `tailwind-patterns.md` - Responsive design patterns with Tailwind
- `auth-integration.md` - Better Auth integration guide

### assets/
- `component-templates/` - React component boilerplate templates
- `page-templates/` - Next.js page structure templates
