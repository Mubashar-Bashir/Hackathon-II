---
id: 0002
title: update-sdd-workflow-skills-agents
stage: general
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-task-organization
user: mubashar
command: /sp.phr
labels: ["sdd-workflow", "skills", "agents", "planning", "specification"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/mubashar/code/Hackathon-II/.specify/templates/plan-template.md
 - /home/mubashar/code/Hackathon-II/.claude/commands/sp.plan.md
tests:
 - none
---

## Prompt

--title "update-sdd-workflow-skills-agents" --stage plan --feature "sdd-workflow"

## Response snapshot

Updated the SDD workflow by adding a dedicated section for determining required skills and agents during the planning phase, with clear guidance that these decisions should be made during planning rather than specification phase.

## Outcome

- ✅ Impact: SDD workflow now includes explicit guidance on when to decide required skills and agents, clarifying that this happens during planning phase rather than specification phase
- 🧪 Tests: none
- 📁 Files: Updated plan-template.md and sp.plan.md with skills/agents decision guidance
- 🔁 Next prompts: /sp.plan will now include skills and agents determination as part of the planning process
- 🧠 Reflection: Decoupling skill/agent decisions from specification allows for better architectural consideration while keeping specification focused on user requirements.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
