---
id: 009
title: phase-ii-constitution-update
stage: refactor
date: 2025-12-27
surface: agent
model: Claude Sonnet 4.5
feature: auth-db-schema
branch: 004-auth-db-schema
user: mubashar
command: sp.constitution
labels: ["constitution", "phase-ii", "monorepo", "security", "workflow"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

# Phase-II Constitution Update

## Prompt Text
```
you can update with existing without duplications """ /sp.constitution "Update for Phase-II:
1. Establish Monorepo structure (backend/ and frontend/).
2. Define SQLModel + Neon as the primary storage layer.
3. Enforce Better Auth JWT verification for all API routes.
4. Require all DB queries to filter by authenticated user_id.
5. Set Next.js 16 App Router as the frontend standard. """..."Phase-II Constitution (Strategic Sections)
1. Monorepo Governance
Root Sovereignty: The root directory governs all sub-projects. No cross-directory imports are allowed (e.g., frontend cannot import directly from backend).

Context Isolation: Claude must treat frontend/ as a TypeScript/Next.js environment and backend/ as a Python/FastAPI environment.

2. The "User-ID" Law (Security)
Mandatory Isolation: Every database query MUST include a user_id filter derived from the JWT.

Zero-Trust API: No endpoint shall return data without a valid Authorization: Bearer <token> header verification.

Secret Sync: The BETTER_AUTH_SECRET must be identical in both frontend/.env and backend/.env.

3. Technical Stack Enforcement
Backend:

Framework: FastAPI.

Database: Neon PostgreSQL via SQLModel.

Validation: All API inputs must use Pydantic models.

Frontend:

Framework: Next.js 16 (App Router).

Styling: Tailwind CSS.

Auth: Better Auth with JWT plugin enabled.

4. Spec-Kit Plus Workflow
Traceability: Every Pull Request or code change must reference a .tasks entry from the specs/ directory.

No Manual Edits: Any manual change to the code is a violation of the "Agentic Dev Stack" protocol. " just adjust under phase-II dont replace, dont make duplications use concise and synch with top bottom layers
```

## Response Text
Updated the project constitution to include Phase-II specific rules while maintaining existing structure. Added comprehensive sections covering:

1. Updated Phase II scope to include both API layer and web interface
2. Monorepo Structure rules with directory governance and environment isolation
3. Storage and Authentication requirements (SQLModel + Neon, JWT verification, user data isolation)
4. Technical Stack Standards for both backend and frontend
5. Security Enforcement with zero-trust API and mandatory isolation
6. Development Workflow with traceability and agentic development protocol

The update maintains all existing constitution principles while adding Phase-II specific governance that aligns with the strategic requirements provided.

## Outcome
Successfully updated constitution with Phase-II specific rules that govern monorepo structure, authentication, security, and development workflow without duplicating or replacing existing principles.

## Evaluation
The constitution now properly governs Phase-II development with specific rules for monorepo governance, security enforcement, and technical stack standards while maintaining backward compatibility with existing principles.