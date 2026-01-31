# Research: Todo Backend API

## Overview
This document captures research findings for implementing the Todo Backend API, including technology decisions, best practices, and implementation strategies.

## Technology Decisions

### FastAPI Framework
**Decision**: Use FastAPI as the web framework for the backend API.
**Rationale**: FastAPI offers excellent performance, built-in validation, automatic OpenAPI documentation, strong typing support, and async capabilities. It's ideal for building REST APIs with Python.
**Alternatives considered**: Flask, Django REST Framework
- Flask: More flexible but requires more boilerplate code
- Django REST Framework: Good but heavier than needed for this use case

### SQLModel ORM
**Decision**: Use SQLModel as the ORM for database operations.
**Rationale**: SQLModel combines the power of SQLAlchemy with Pydantic validation, allowing shared models between API schemas and database models. It's developed by the same author as FastAPI and integrates well with it.
**Alternatives considered**: SQLAlchemy, Tortoise ORM, Peewee
- SQLAlchemy: Powerful but requires separate validation layer
- Tortoise ORM: Good for async but less mature
- Peewee: Lightweight but lacks advanced features

### JWT Authentication
**Decision**: Implement JWT-based authentication using python-jose.
**Rationale**: JWT provides stateless authentication that fits the requirement for a stateless backend. It works well with Better Auth which generates the tokens.
**Alternatives considered**: Session-based auth, OAuth2 password flow with database sessions
- Session-based auth: Would violate the stateless requirement
- OAuth2 with database: Would require server-side session storage

### Neon Serverless PostgreSQL
**Decision**: Use Neon Serverless PostgreSQL as the database backend.
**Rationale**: Neon provides serverless PostgreSQL with auto-scaling, branching, and improved performance. It integrates well with modern applications and provides the required PostgreSQL functionality.
**Alternatives considered**: Regular PostgreSQL, SQLite, MongoDB
- Regular PostgreSQL: Would work but lacks serverless benefits
- SQLite: Not suitable for multi-user production applications
- MongoDB: Doesn't fit the relational data model required

## Architecture Patterns

### Dependency Injection
FastAPI's built-in dependency injection system will be used to handle:
- Database sessions
- Authentication verification
- Configuration settings
- Rate limiting

### Security Implementation
- All endpoints require JWT authentication
- User-based data isolation at the database query level
- Input validation using Pydantic models
- Proper HTTP status codes for different scenarios
- Rate limiting to prevent abuse

### Error Handling
- Custom exception handlers for different error types
- Consistent error response format
- Logging of security-relevant events
- Graceful degradation when possible

## API Design Decisions

### Endpoint Structure
- Base path: `/api/v1/tasks` (adding versioning for future compatibility)
- Methods: GET, POST, PUT, DELETE, PATCH as specified
- Authentication: Bearer token in Authorization header
- Response format: JSON with appropriate status codes

### Data Validation
- Task title: 1-200 characters
- Task description: Optional, up to reasonable length
- User ID: Extracted from JWT, not from request body
- All inputs validated using Pydantic models

## Integration Points

### Frontend Compatibility
- API endpoints designed to match frontend client expectations
- JSON request/response format
- Proper CORS configuration for frontend origin
- Consistent error handling for frontend consumption

### Better Auth Integration
- Accept JWT tokens from Better Auth
- Validate using BETTER_AUTH_SECRET
- Extract user ID from token claims
- Verify token signature and expiration

## Implementation Approach

### Phased Development
1. Foundation: Set up FastAPI app, database connection, and configuration
2. Authentication: Implement JWT verification dependency
3. Models: Create SQLModel Task model with proper relationships
4. API Routes: Implement all required endpoints with proper security
5. Testing: Add comprehensive unit and integration tests
6. Deployment: Configure Docker and environment variables

### Security Measures
- Never trust user-provided user IDs
- Always filter queries by authenticated user ID
- Return 404 instead of 403 when possible to avoid user enumeration
- Log authentication failures for monitoring