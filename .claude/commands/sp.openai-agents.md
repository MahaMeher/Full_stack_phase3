---
description: Build AI agents using OpenAI Agents SDK with natural language understanding, tool calling, and conversation management. Use when implementing conversational AI, creating chatbots with tool integration, or building agentic workflows with OpenAI models.
handoffs:
  - label: Analyze Requirements
    agent: sp.clarify
    prompt: Clarify agent requirements and capabilities needed
    send: true
  - label: Generate Implementation Plan
    agent: sp.plan
    prompt: Create detailed implementation plan for OpenAI Agents SDK integration
    send: true
  - label: Create Tasks
    agent: sp.tasks
    prompt: Generate actionable tasks for OpenAI Agents SDK implementation
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Overview

This skill provides comprehensive guidance for building AI agents using the OpenAI Agents SDK, focusing on natural language understanding, tool integration, and stateless conversation management.

## When to Use This Skill

Use this skill when you need to:
- Build conversational AI agents with OpenAI models
- Implement natural language to tool calling
- Create stateless chat systems with conversation history
- Integrate AI agents with custom backend operations
- Handle multi-turn conversations with context awareness

## Core Concepts

### Agent Architecture
```
User Message → Agent (Instructions + Tools) → OpenAI Model → Tool Calls → Response
```

### Key Components
- **Agent**: Orchestrates conversation and tool usage
- **Instructions**: System prompt defining agent behavior
- **Tools**: Functions the agent can call
- **Messages**: Conversation history array
- **Runner**: Executes agent with streaming or complete responses

## Implementation Steps

### 1. Agent Configuration
- Define system instructions and agent persona
- Configure model selection (gpt-4, gpt-3.5-turbo, etc.)
- Set up agent parameters (temperature, max tokens, etc.)
- Configure tool access and permissions

### 2. Tool Development
- Create function definitions with JSON Schema
- Implement tool functions with proper error handling
- Register tools with the agent
- Test individual tool functionality

### 3. Conversation Management
- Implement message history handling
- Create conversation state management
- Handle multi-turn conversations
- Implement context awareness

### 4. Response Processing
- Parse tool call responses
- Generate natural language responses
- Handle streaming vs complete responses
- Implement proper error messaging

## Technical Requirements

### Agent Configuration
- OpenAI API key and client setup
- Model selection and parameter configuration
- System instruction template
- Tool registration and schema validation

### Tool Interface Specifications
- JSON Schema definitions for all tools
- Proper error handling and validation
- Async execution support
- Type safety and documentation

### Conversation Management
- Message history storage and retrieval
- Context window management
- Session state handling
- Thread management for concurrent conversations

## Best Practices

### Security Considerations
- Validate and sanitize all inputs
- Implement proper authentication for sensitive tools
- Use rate limiting to prevent abuse
- Log all agent interactions for audit trails

### Performance Optimization
- Cache frequently used responses
- Optimize token usage in system instructions
- Implement efficient message history management
- Use appropriate model selection based on task complexity

### Error Handling
- Implement graceful fallback mechanisms
- Provide informative error messages to users
- Log errors for debugging and monitoring
- Handle API failures and retries appropriately

## Expected Artifacts
- Agent configuration with system instructions
- Custom tools with proper JSON Schema definitions
- Conversation management system
- Error handling and logging implementation
- Documentation for agent capabilities
- Test suite for agent functionality

## Validation Criteria

- [ ] Agent responds appropriately to natural language inputs
- [ ] Tool calling functions work correctly with proper error handling
- [ ] Conversation history is maintained across turns
- [ ] Agent handles edge cases and invalid inputs gracefully
- [ ] Performance meets expected response time requirements
- [ ] Security measures are implemented for sensitive operations
- [ ] Error logging and monitoring are properly configured
- [ ] Documentation covers all agent capabilities and limitations

Context for OpenAI Agents SDK implementation: $ARGUMENTS

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