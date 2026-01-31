---
id: 001
title: create-ai-chatbot-spec
stage: spec
date: '2026-01-28'
surface: agent
model: Claude Sonnet 4.5
feature: ai-chatbot
branch: 004-ai-chatbot
user: user
command: /sp.specify
labels:
  - specification
  - ai-chatbot
  - todo-app
  - mcp
links:
  SPEC: specs/004-ai-chatbot/spec.md
  TICKET: null
  ADR: null
  PR: null
files_yaml: |
  - specs/004-ai-chatbot/spec.md
  - specs/004-ai-chatbot/checklists/requirements.md
tests_yaml: |
  - specs/004-ai-chatbot/checklists/requirements.md
prompt_text: |
  Todo AI Chatbot Integration (Phase III)

  Objective

  Integrate an AI-powered conversational chatbot into the existing Full-Stack Todo Application (Phase II) that allows authenticated users to manage their tasks using natural language, without changing any existing task functionality.

  The chatbot must be fully agentic, tool-driven, stateless, and production-grade, following the approved constitution.

  Scope

  This specification covers:
  AI chatbot backend integration

  MCP tool layer for task operations

  Cohere-powered agent (OpenAI Agents SDK–style)

  Stateless chat API

  Database-backed conversation memory

  Frontend chatbot UI integration (icon-based)

  Out of scope:

  Changing existing task APIs

  Modifying authentication logic

  Adding non-required features (reminders, recurrence, AI summaries)
  Target Users

  Authenticated users who:

  Are already logged in via Better Auth

  Want to manage personal tasks using natural language

  Expect a fast, clean, and intuitive chat experience

  Functional Requirements
  1️⃣ Conversational Task Management

  The chatbot must support:

  Adding tasks

  Listing tasks (all / pending / completed)

  Updating task title or description
  Completing tasks

  Deleting tasks

  All actions must be executed only via MCP tools.

  2️⃣ Natural Language Understanding

  The chatbot must correctly interpret user intent such as:

  "Add a task to buy groceries"

  "Show my pending tasks"

  "Mark task 3 as complete"

  "Delete the meeting task"

  "Change task 1 to call mom tonight"

  Intent → tool mapping must follow the constitution strictly.
  Authentication & User Context

  User identity comes from Better Auth

  user_id is injected server-side

  AI must NEVER infer or fabricate user identity

  All MCP tool calls must be scoped to authenticated user_id

  4️⃣ Stateless Chat Architecture

  Each chat request must:

  Receive user message

  Fetch conversation history from database

  Persist user message

  Run AI agent with history + message

  Invoke MCP tools if needed
  Persist assistant response

  Return response to frontend

  No server memory allowed.

  AI & Agent Requirements
  AI Provider

  Cohere API

  API Key provided via environment variable
  COHERE_API_KEY

  Agent Framework Style

  Follow OpenAI Agents SDK concepts

  Agent + Runner pattern

  Tool-based execution
  Deterministic outputs

  Provider Replacement Rule

  Gemini / OpenAI models are NOT allowed

  Cohere must be used while preserving OpenAI Agents SDK architecture semantics

  MCP Tool Layer
  MCP Server Responsibilities

  Expose task operations as tools

  Validate parameters strictly

  Persist task changes using existing database models

  Return structured JSON responses

  Required MCP Tools
  add_task

  list_tasks

  update_task

  complete_task

  delete_task

  No other tools are permitted.

  Database Requirements
  Required Models

  Task (already exists)

  Conversation
  Message

  Persistence Rules

  All user and assistant messages must be stored

  Conversation continuity must survive server restarts

  Database is the single source of truth

  API Specification
  Chat Endpoint

  POST /api/chat

  Request Body

  conversation_id (optional)

  message (required string)
  Response

  conversation_id

  response

  tool_calls (if any)

  Server must remain stateless.

  Frontend Integration Requirements
  Chatbot UI

  Floating chatbot icon visible across app

  Opens a modern chat panel/modal

  Clean, professional UI consistent with existing app design

  Smooth animations (open/close, message send)

  Loading indicators and error handling

  UX Rules
  Chatbot must not interrupt core task UI

  Must feel optional, friendly, and powerful

  Clear confirmation messages after actions

  Technical Constraints

  Backend: FastAPI (existing)

  AI Logic: OpenAI Agents SDK–style runner

  LLM: Cohere API

  Tools: MCP Server

  ORM: SQLModel

  Database: Neon PostgreSQL

  Auth: Better Auth

  Frontend: Existing Next.js app
  Non-Functional Requirements

  Secure (no cross-user access)

  Scalable (stateless)

  Deterministic (tool-driven)

  Demo-ready

  Judge-friendly architecture

  Success Criteria

  The implementation is considered successful when:

  Users can manage todos entirely via chat

  Existing Todo functionality remains unchanged

  Chat survives server restarts

  AI always uses MCP tools
  Cohere is used correctly as LLM backend

  Frontend chatbot UI is polished and intuitive

  Judges clearly recognize agentic + MCP architecture

  Final Instruction

  Implement exactly what is specified.
  Do not add assumptions.
  Do not skip steps.
  Follow the constitution strictly.
response_text: |
  Created comprehensive specification for Todo AI Chatbot Integration feature, including:
  - User scenarios with prioritized user stories (P1-P3)
  - Functional requirements (FR-001 to FR-015)
  - Key entities (Conversation, Message, Task)
  - Success criteria (SC-001 to SC-009)
  - Edge cases for robustness
  - Quality checklist for validation
outcome: |
  Successfully created detailed specification for AI chatbot integration that follows stateless architecture,
  uses MCP tools for task operations, integrates with Cohere API, and maintains existing functionality
  while adding natural language task management capabilities.
evaluation: |
  The specification is complete, testable, and ready for the planning phase (/sp.plan).
  All requirements are clearly defined with measurable success criteria.
---