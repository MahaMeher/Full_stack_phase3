# MCP Server Integration Skill

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
```
MCP Server Pattern:
Client → FastAPI Endpoint → OpenAI Agent → MCP Tools → Database
         (Stateless)        (Stateless)    (Stateless)   (Persistent)
```

### Key Principle: Complete Statelessness
- Server: Holds NO state between requests
- Agent: Reconstructed with full context each request
- MCP Tools: Query/modify database directly
- Conversation State: Stored in database, fetched each request

## Implementation Steps

### 1. Infrastructure Setup
- Initialize FastAPI application with MCP configuration
- Set up OpenAI client and agent configuration
- Configure database connections and models
- Create base MCP tool framework

### 2. MCP Tool Development
- Implement database query tools
- Create business logic tools
- Develop utility tools
- Add error handling and validation

### 3. Stateless Chat Endpoint
- Create conversation state management
- Implement agent reconstruction logic
- Build response persistence mechanism
- Add proper error responses

### 4. Testing and Validation
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

## Best Practices
- Always maintain statelessness in server components
- Use proper error handling and logging for debugging
- Implement comprehensive testing for all tool functions
- Follow security best practices for API endpoints
- Optimize database queries for performance
- Document all tools with clear JSON schemas