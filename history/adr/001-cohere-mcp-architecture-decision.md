# ADR 001: Cohere-MCP Architecture for AI Chatbot Integration

## Status
Proposed

## Context
The Todo AI Chatbot Integration (Phase III) requires selecting an AI provider and architectural pattern for implementing natural language processing with task management capabilities. The requirements specify:
- Use Cohere as the LLM provider (not OpenAI or Gemini)
- Preserve OpenAI Agents SDK architectural semantics
- Implement MCP (Model Context Protocol) server for tool-driven operations
- Maintain agentic architecture with stateless design

## Decision
We will implement a Cohere-powered agent that follows OpenAI Agents SDK architectural patterns while using MCP tools for all task operations. This creates a hybrid architecture that satisfies both the technical constraint (Cohere-only) and architectural goals (agentic design).

## Alternatives Considered
1. **Direct OpenAI integration with adapters**: Would violate the "Cohere only" constraint
2. **Simple prompt-response without MCP tools**: Would violate the agentic architecture requirement
3. **Custom agent framework**: Would require significant development time and deviate from proven patterns

## Rationale
- Complies with technical constraint of using Cohere as LLM provider
- Preserves familiar OpenAI Agents SDK patterns for developer productivity
- Enables MCP tool-based architecture for secure, validated operations
- Maintains agentic design principles with stateless execution
- Allows for future migration if requirements change

## Consequences
### Positive
- Compliance with specified technology constraints
- Familiar architectural patterns for developers
- Secure, validated task operations through MCP tools
- Scalable stateless design

### Negative
- Requires adapter layer between Cohere API and OpenAI Agents SDK patterns
- Slightly increased complexity compared to direct integration
- Potential performance overhead from tool-based operations

## Implementation
- Create Cohere agent wrapper that mimics OpenAI Agents SDK interface
- Implement MCP server with task operation tools
- Connect agent to tools through standardized interfaces
- Ensure proper error handling and fallback mechanisms