# ADR-0008: Frontend Technology Stack Selection

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-27
- **Feature:** Todo App with Authentication and Task Management
- **Context:** Need to select appropriate frontend technologies for a modern web application that will provide responsive UI, secure authentication integration, and seamless API communication. The stack must support the microservice architecture decision and integrate well with Better Auth for authentication.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We will use the following frontend technology stack:
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **State Management**: React Context API with custom hooks
- **API Client**: Custom fetch-based client with proper error handling
- **Testing**: Jest, React Testing Library, and Playwright for E2E tests
- **Deployment**: Vercel (recommended for Next.js)

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Next.js App Router provides excellent developer experience with file-based routing
- TypeScript ensures type safety and reduces runtime errors
- Tailwind CSS enables rapid UI development with utility-first approach
- Better Auth provides secure, well-maintained authentication solution
- Server-side rendering capabilities for better SEO and performance
- Built-in API routes for potential edge cases
- Strong ecosystem and community support
- Vercel deployment provides optimized performance and caching

### Negative

- Vendor lock-in to Vercel for optimal deployment experience
- Framework coupling may limit flexibility for future changes
- Learning curve for developers not familiar with Next.js App Router
- Bundle size considerations for complex applications
- Potential complexity with authentication state management across components

## Alternatives Considered

- **Remix**: Excellent for data loading but more complex setup - Rejected for additional complexity beyond requirements
- **Create React App**: Outdated compared to Next.js 16+ with App Router - Rejected for lack of modern features
- **Vue.js/Nuxt.js**: Different ecosystem than selected backend - Rejected for consistency with overall architecture
- **SvelteKit**: Good alternative but smaller ecosystem - Rejected for team familiarity with React ecosystem
- **Vanilla JavaScript**: Would require building many features from scratch - Rejected for development time concerns
- **Angular**: Heavier framework than needed for todo app - Rejected for unnecessary complexity
- **Gatsby**: Better for static sites, less suitable for authenticated applications - Rejected for dynamic content needs

## References

- Feature Spec: /specs/005-todo-auth/spec.md
- Implementation Plan: /specs/005-todo-auth/plan.md
- Related ADRs: ADR-0006 (Full-Stack Architecture), ADR-0007 (Backend Technology Stack)
- Evaluator Evidence: /specs/005-todo-auth/research.md <!-- link to eval notes/PHR showing graders and outcomes -->
