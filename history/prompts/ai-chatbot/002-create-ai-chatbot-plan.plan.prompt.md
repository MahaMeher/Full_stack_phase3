---
id: 002
title: create-ai-chatbot-plan
stage: plan
date: '2026-01-28'
surface: agent
model: Claude Sonnet 4.5
feature: ai-chatbot
branch: 004-ai-chatbot
user: user
command: /sp.plan
labels:
  - planning
  - ai-chatbot
  - mcp
  - architecture
links:
  SPEC: specs/004-ai-chatbot/spec.md
  PLAN: specs/004-ai-chatbot/plan.md
  TICKET: null
  ADR: null
  PR: null
files_yaml: |
  - specs/004-ai-chatbot/plan.md
tests_yaml: |
  - specs/004-ai-chatbot/plan.md
prompt_text: |
  Create:
  - High-level architecture flow (Frontend → Chat API → Agent Runner → MCP Tools → DB)
  - Component & directory structure for /frontend, /backend, /specs
  - Agent execution lifecycle (stateless request cycle)
  - MCP tool interaction flow
  - Frontend chatbot UI integration plan

  Development approach:
  - Follow Agentic Dev Stack workflow strictly
  - Reuse existing Full-Stack Todo backend (Phase II)
  - Integrate AI chatbot without modifying existing task APIs
  - Use Cohere as LLM provider while preserving OpenAI Agents SDK architecture semantics
  - Use MCP server as the only interface for task operations
  Phases:
  1. Architecture alignment & environment setup
  2. Database models for conversations & messages
  3. MCP server implementation (task tools)
  4. AI agent & runner implementation (Cohere-powered)
  5. Stateless chat API endpoint
  6. Frontend chatbot UI integration (floating icon + panel)
  7. End-to-end validation & demo readiness

  Decisions to document:
  - Agent + MCP separation vs direct DB access
  - Stateless chat design vs in-memory sessions
  - Tool-driven task execution vs free-form AI actions
  - Cohere integration strategy with OpenAI Agents SDK pattern
  Validation & testing:
  - User can add/list/update/complete/delete tasks via chat
  - AI always invokes MCP tools for task actions
  - Conversation persists after server restart
  - User cannot access another user's tasks
  - Frontend chatbot works without breaking existing UI
  - Environment variables correctly wired (Cohere + Better Auth)

  Constraints:
  - No backend business logic duplication
  - No changes to existing task APIs or auth logic
  - No server-side state
  - No Gemini/OpenAI models — Cohere only
  Output:
  - Architecture sketch
  - Phase-wise task breakdown
  - Identified risks & mitigations
  - Readiness checklist for Phase III completion
response_text: |
  Created comprehensive implementation plan for Todo AI Chatbot Integration (Phase III) including:
  - High-level architecture flow with component interactions
  - Detailed directory structure for backend and frontend
  - Agent execution lifecycle with stateless request cycle
  - MCP tool interaction flow with security enforcement
  - Frontend chatbot UI integration plan
  - 7-phase implementation approach with specific tasks
  - Key architectural decisions and rationale
  - Risk assessment and mitigation strategies
  - Validation criteria and readiness checklist
outcome: |
  Successfully created detailed implementation plan that follows Agentic Dev Stack workflow,
  maintains stateless architecture, uses MCP tools for task operations, integrates with
  Cohere API, and preserves existing functionality while adding AI chatbot capabilities.
evaluation: |
  The plan is complete, technically sound, and ready for the tasks generation phase (/sp.tasks).
  All architectural decisions are documented with trade-offs and rationale.
---