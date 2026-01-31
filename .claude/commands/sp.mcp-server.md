---
description: Build and integrate MCP (Model Context Protocol) servers with OpenAI Agents SDK for stateless AI-powered applications. Use when creating MCP tools, implementing stateless chat endpoints, or connecting AI agents to custom backend operations through standardized tool interfaces.
handoffs:
  - label: Analyze Architecture
    agent: sp.architecture
    prompt: Analyze current system architecture for MCP integration points
    send: true
  - label: Generate Implementation Plan
    agent: sp.plan
    prompt: Create detailed implementation plan for MCP server integration
    send: true
  - label: Create Tasks
    agent: sp.tasks
    prompt: Generate actionable tasks for MCP server implementation
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Overview

This skill provides comprehensive guidance for building MCP (Model Context Protocol) servers that integrate with OpenAI Agents SDK to create stateless, scalable AI-powered applications.

## When to Use This Skill

Use this skill when you need to:
- Implement MCP server with custom tools
- Connect OpenAI Agents to backend operations
- Build stateless chat endpoints with database persistence
- Create standardized tool interfaces for AI agents
- Integrate FastAPI backend with OpenAI Agents SDK

## Core Architecture

MCP Server Pattern:
```
Client → FastAPI Endpoint → OpenAI Agent → MCP Tools → Database
         (Stateless)        (Stateless)    (Stateless)   (Persistent)
```

Key Principle: Complete Statelessness
- Server: Holds NO state between requests
- Agent: Reconstructed with full context each request
- MCP Tools: Query/modify database directly
- Conversation State: Stored in database, fetched each request

## Implementation Phases

### Phase 1: Infrastructure Setup
- Initialize FastAPI application with MCP configuration
- Set up OpenAI client and agent configuration
- Configure database connections and models
- Create base MCP tool framework

### Phase 2: MCP Tool Development
- Implement database query tools
- Create business logic tools
- Develop utility tools
- Add error handling and validation

### Phase 3: Stateless Chat Endpoint
- Create conversation state management
- Implement agent reconstruction logic
- Build response persistence mechanism
- Add proper error responses

### Phase 4: Testing and Validation
- Verify stateless operation
- Test conversation continuity
- Validate tool functionality
- Confirm database integrity

## Technical Requirements

### MCP Server Components
- FastAPI application with proper routing
- OpenAI Agent with system instructions
- MCP tool registration and discovery
- Database connection pooling
- Request/response logging

### Tool Interface Specifications
- JSON Schema definitions for all tools
- Proper error handling and validation
- Async execution support
- Type safety and documentation

### Database Schema Requirements
- Conversation storage model
- Message history tracking
- Metadata and context storage
- Indexing for efficient queries
- Connection pooling configuration

## Expected Artifacts

Upon completion, this skill will produce:
- MCP server implementation with FastAPI
- OpenAI Agent integration with custom tools
- Database models and persistence layer
- Stateless chat endpoint with proper error handling
- Configuration files and documentation
- Test suite for verifying functionality
- Deployment configuration files

## Validation Criteria

- [ ] MCP server starts successfully and responds to health checks
- [ ] OpenAI Agent connects and executes tools properly
- [ ] Conversation state persists correctly in database
- [ ] Stateless operation verified (no server-side session state)
- [ ] MCP tools execute with proper error handling
- [ ] Database operations complete efficiently with proper indexing
- [ ] Chat endpoint maintains conversation continuity
- [ ] Error scenarios handled gracefully with appropriate responses

Context for MCP server implementation: $ARGUMENTS

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.