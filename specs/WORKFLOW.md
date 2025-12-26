# Workflow with Spec-KitPlus + Claude Code

## Process
1. **Write/Update Spec** → @specs/features/new-feature.md
2. **Ask Claude Code to Implement** → "Implement @specs/features/new-feature.md"
3. **Claude Code reads**: Root CLAUDE.md, Feature spec, API spec, Database spec, Relevant CLAUDE.md
4. **Claude Code implements** in both frontend and backend
5. **Test and iterate** on spec if needed

## Referencing Specs in Claude Code
```markdown
# Implement a feature
You: @specs/features/task-crud.md implement the create task feature

# Implement API
You: @specs/api/rest-endpoints.md implement the GET /api/tasks endpoint

# Update database
You: @specs/database/schema.md add due_date field to tasks

# Full feature across stack
You: @specs/features/authentication.md implement Better Auth login
```

## Summary

| Component | Purpose |
|-----------|---------|
| /.spec-kit/config.yaml | Spec-Kit configuration |
| /specs/<features>/** | What to build |
| /CLAUDE.md | How to navigate and use specs |
| /frontend/CLAUDE.md | Frontend-specific patterns |
| /backend/CLAUDE.md | Backend-specific patterns |

## Key Point:
Spec-Kit Plus provides organized, structured specs that Claude Code can reference. The CLAUDE.md files tell Claude Code how to use those specs and project-specific conventions.

## Monorepo vs Separate Repos

| Approach | Pros | Cons |
|----------|------|------|
| Monorepo ⭐ | Single CLAUDE.md context, easier cross-cutting changes | Larger repo |
| Separate Repos | Clear separation, independent deployments | Claude Code needs workspace setup |

### Recommendation:
Use monorepo for the hackathon – simpler for Claude Code to navigate and edit both frontend and backend in a single context.

## Key Benefits of This Structure

| Benefit | Description |
|---------|-------------|
| Single Context | Claude Code sees entire project, can make cross-cutting changes |
| Layered CLAUDE.md | Root file for overview, subfolder files for specific guidelines |
| Specs Folder | Reference specifications directly with @specs/filename.md |
| Clear Separation | Frontend and backend code in separate folders, easy to navigate |