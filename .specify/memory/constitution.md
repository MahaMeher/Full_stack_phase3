<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- Modified principles: None (new constitution)
- Added sections: All sections
- Removed sections: None
- Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Todo AI Chatbot Constitutional Specification

## Core Principles

### I. Stateless Server Rule (Non-Negotiable)
The system shall remain stateless at server level with no in-memory session storage. Every request must be fully reconstructable from database. Conversation history fetched on each request. All conversation continuity must survive server restarts.

### II. Tool-Driven Intelligence
AI never performs direct database operations. AI can ONLY act through MCP tools. Tools are deterministic and side-effect controlled. AI is FORBIDDEN from direct SQL queries, direct ORM access, or business logic outside tools.

### III. Zero Regression Policy
Existing Todo APIs MUST NOT change behavior. Chatbot is an add-on layer. All previous frontend & backend functionality remains intact. No changes to existing API contracts.

### IV. Authentication Context Enforcement
Authentication handled exclusively by Better Auth. AI must NEVER authenticate users. Auth context is injected server-side. Every action is scoped to authenticated user_id. Cross-user access is forbidden. AI must never guess or fabricate user identity.

### V. MCP Tool Constraint Compliance
MCP Server exposes task operations as tools only. Allowed tools: add_task, list_tasks, update_task, complete_task, delete_task. AI must validate inputs strictly and persist results in database. AI returns structured JSON only.

### VI. Cohere-Powered Intelligence
Use Cohere API as the LLM engine for reasoning and intent detection. Follow OpenAI Agents SDK mental model for agent + runner pattern and tool-calling abstraction. All inference must use Cohere API.

## Database Constitution
Persisted Entities: Tasks, Conversations, Messages. All AI messages must be stored. Database is the single source of truth. Conversation continuity must survive server restarts.

## Agent Behavior Constitution
Intent Mapping Rules: Add/remember → add_task, Show/list → list_tasks, Done/complete → complete_task, Delete/remove → delete_task, Change/update → update_task. Ambiguity Resolution: If task reference unclear → list tasks first. Never assume task IDs. Ask clarification when needed.

## Conversation Flow Constitution
Receive user message → Extract authenticated user context → Fetch conversation history → Persist user message → Construct agent prompt (history + message) → Run Cohere-powered agent → Invoke MCP tools if required → Persist assistant response → Return response to frontend.

## Error Handling Constitution
Errors must be human-friendly. No stack traces exposed. Tool errors converted to natural language. AI must apologize and recover gracefully. Error responses must be polite, clear, confirmatory, professional, and concise.

## Forbidden Actions
The AI system must NEVER: Modify authentication logic, Bypass MCP tools, Access another user's data, Change existing API contracts, Store secrets in responses, Hallucinate task IDs or user info.

## Success Definition
The system is successful when: Chatbot manages todos end-to-end via conversation, No regression in existing Todo app, AI uses Cohere but behaves like OpenAI Agents SDK, MCP tools are the sole action interface, System survives restarts with full chat continuity.

## Governance
This constitution is absolute. Any implementation violating these rules is invalid. All development must verify compliance. Amendments require formal documentation and approval process. Use this constitution for all development guidance.

**Version**: 1.0.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-21