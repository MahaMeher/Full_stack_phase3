# Feature Specification: Todo Backend API

**Feature Branch**: `001-todo-backend-api`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description: "Backend for Todo Full-Stack Web Application (Phase II)

Objective:
Design and implement a secure, production-ready FastAPI backend that provides a RESTful API for a multi-user todo application and integrates seamlessly with the Next.js frontend.1~
Target consumers:
- Authenticated frontend clients (Next.js App Router)
- Internal agents following spec-driven boundaries
Core responsibilities:
- Provide secure CRUD APIs for task management
- Enforce strict user-based data isolation
- Verify and authorize users via JWT issued by Better Auth
- Persist all data in Neon Serverless PostgreSQL
Authentication & security:
- All API endpoints MUST require JWT authentication
- JWT must be verified using BETTER_AUTH_SECRET
- JWT is received via `Authorization: Bearer <token>` header
- Extract authenticated user identity from JWT
- Backend must NEVER trust frontend-provided user IDs
- All task queries MUST be filtered by authenticated user
- Unauthorized requests return 401 Unauthorized
- Cross-user access attempts return 403 Forbidden or 404 Not Found
API design:
- Base path: /api/tasks
- Endpoints to implement:
  - GET    /api/tasks              → List user tasks
  - POST   /api/tasks              → Create task
- GET    /api/tasks/{id}          → Get task details
  - PUT    /api/tasks/{id}          → Update task
  - DELETE /api/tasks/{id}          → Delete task
  - PATCH  /api/tasks/{id}/complete → Toggle completion
- Use JSON request/response format
- Return proper HTTP status codes
- Use FastAPI dependency injection for auth and DB sessions
Data & persistence:
- Use SQLModel as ORM
- Database: Neon Serverless PostgreSQL
- Connection via environment variable:
  - Neon_db_url
- Task fields:
  - id (primary key)
  - user_id (string, from JWT)
  - title (required, 1–200 chars)
  - description (optional)
  - completed (boolean)
  - created_at
  - updated_at
- Index tasks by user_id for performance
Integration requirements:
- Fully compatible with frontend API client (/lib/api.ts)
- CORS configured for frontend origin (BETTER_AUTH_URL)
- Stateless backend (JWT-only, no sessions)
- Works correctly in docker-compose setup
Environment configuration:
- Neon_db_url
- BETTER_AUTH_SECRET
- BETTER_AUTH_URL
Success criteria:
- Backend rejects unauthenticated requests
- Each user can only access their own tasks
- All CRUD operations work correctly
- JWT verification works reliably
- Frontend can fully operate using this backend
- API is stable, predictable, and demo-ready
Constraints:
- Backend-only implementation
- No frontend UI changes
- No authentication provider implementation (Better Auth is external)
- No advanced features (recurrence, reminders, AI)
- Follow clean architecture and single-responsibility principles"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management (Priority: P1)

As an authenticated user, I want to manage my personal tasks through a secure API so that I can organize my work without worrying about unauthorized access to my data.

**Why this priority**: This is the core functionality of the todo application. Without secure task management, the application has no value to users.

**Independent Test**: Can be fully tested by creating a user account, authenticating with JWT, creating tasks, viewing tasks, updating tasks, and deleting tasks. The system should ensure that users can only access their own tasks.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT, **When** they request to create a task, **Then** the task is created and associated with their user ID
2. **Given** a user is authenticated with a valid JWT, **When** they request to list their tasks, **Then** they receive only tasks associated with their user ID
3. **Given** a user is authenticated with a valid JWT, **When** they request to update a task, **Then** the update succeeds only if the task belongs to them
4. **Given** a user is authenticated with a valid JWT, **When** they request to delete a task, **Then** the deletion succeeds only if the task belongs to them

---

### User Story 2 - Authentication and Authorization (Priority: P1)

As a system administrator, I want the backend to enforce strict authentication and authorization so that unauthorized users cannot access the API and users cannot access each other's data.

**Why this priority**: Security is fundamental to the application. Without proper authentication and authorization, the entire system is vulnerable.

**Independent Test**: Can be fully tested by attempting API requests with no token, invalid tokens, and valid tokens while verifying that unauthorized access is blocked and cross-user access is prevented.

**Acceptance Scenarios**:

1. **Given** a request without authentication, **When** it's made to any API endpoint, **Then** a 401 Unauthorized response is returned
2. **Given** a request with an invalid JWT, **When** it's made to any API endpoint, **Then** a 401 Unauthorized response is returned
3. **Given** a user with a valid JWT, **When** they request another user's task, **Then** a 403 Forbidden or 404 Not Found response is returned

---

### User Story 3 - Task CRUD Operations (Priority: P2)

As an authenticated user, I want to perform all CRUD operations on my tasks so that I can fully manage my todo items through the API.

**Why this priority**: This provides the complete set of operations needed for task management, building on the authentication foundation.

**Independent Test**: Can be fully tested by creating, reading, updating, and deleting tasks for an authenticated user, verifying that all operations work correctly.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT, **When** they POST to /api/tasks with valid task data, **Then** a new task is created and returned with proper status code
2. **Given** a user is authenticated with a valid JWT, **When** they GET /api/tasks, **Then** a list of their tasks is returned in JSON format
3. **Given** a user is authenticated with a valid JWT and owns a task, **When** they PUT /api/tasks/{id} with updated data, **Then** the task is updated and returned
4. **Given** a user is authenticated with a valid JWT and owns a task, **When** they PATCH /api/tasks/{id}/complete, **Then** the task completion status is toggled

---

### Edge Cases

- What happens when a user tries to create a task with a title longer than 200 characters? The system should return an appropriate error response.
- How does the system handle requests when the database is unavailable? The system should return appropriate error responses with proper status codes.
- What happens when a user tries to access a task that doesn't exist? The system should return a 404 Not Found response.
- How does the system handle concurrent updates to the same task? The system should handle this gracefully with appropriate concurrency controls.
- What happens when JWT verification fails due to an invalid secret? The system should reject all requests until the configuration is corrected.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST require JWT authentication for all API endpoints under /api/tasks
- **FR-002**: System MUST verify JWT tokens using the BETTER_AUTH_SECRET environment variable
- **FR-003**: System MUST extract user identity from JWT claims to enforce data isolation
- **FR-004**: System MUST filter all task queries by the authenticated user's ID
- **FR-005**: System MUST return 401 Unauthorized for unauthenticated requests
- **FR-006**: System MUST return 403 Forbidden or 404 Not Found when users attempt to access other users' tasks
- **FR-007**: System MUST support the following endpoints: GET /api/tasks, POST /api/tasks, GET /api/tasks/{id}, PUT /api/tasks/{id}, DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete
- **FR-008**: System MUST use JSON format for all request and response bodies
- **FR-009**: System MUST return appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500, etc.)
- **FR-010**: System MUST persist task data in Neon Serverless PostgreSQL database
- **FR-011**: System MUST use SQLModel as the ORM for database operations
- **FR-012**: System MUST define Task entity with fields: id (primary key), user_id (from JWT), title (1-200 chars, required), description (optional), completed (boolean), created_at, updated_at
- **FR-013**: System MUST index tasks by user_id for performance optimization
- **FR-014**: System MUST be compatible with the frontend API client at /lib/api.ts
- **FR-015**: System MUST configure CORS to allow requests from the frontend origin specified in BETTER_AUTH_URL
- **FR-016**: System MUST be stateless, relying only on JWT for authentication without server-side sessions

### Key Entities

- **Task**: Represents a user's todo item with attributes: id (unique identifier), user_id (identifies the owner), title (text content, 1-200 characters), description (optional additional details), completed (boolean status), created_at (timestamp), updated_at (timestamp)
- **User**: Represents an authenticated user identified by their ID extracted from JWT claims; users can only access tasks associated with their user_id

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints reject unauthenticated requests with 401 Unauthorized status
- **SC-002**: Users can only access tasks associated with their authenticated user ID, with cross-user access attempts properly blocked
- **SC-003**: All CRUD operations (Create, Read, Update, Delete) function correctly for authenticated users
- **SC-004**: JWT verification works reliably with a success rate of 99.9% under normal conditions
- **SC-005**: Frontend application can successfully perform all task management operations through the backend API
- **SC-006**: API demonstrates stability and predictability suitable for demonstration purposes
- **SC-007**: System handles concurrent requests without data integrity issues
- **SC-008**: Response times for API operations remain under 500ms under normal load conditions
