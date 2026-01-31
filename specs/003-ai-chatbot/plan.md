# Architecture Plan: Todo AI Chatbot Integration (Phase III)

## 1. High-Level Architecture Flow

```
Frontend Chat UI → Chat API Endpoint → AI Agent Runner → MCP Tools → Database
     ↑                                      ↓
   Floating       ← Conversation/Messages    ← Task Operations
   Panel                               Persisted
```

**Components Interaction:**
- Frontend: React-based chat interface with floating icon and expandable panel
- Chat API: Stateless endpoint that accepts user messages and returns AI responses
- AI Agent Runner: Cohere-powered agent that interprets natural language and selects appropriate MCP tools
- MCP Tools: Standardized interface for task operations (create, read, update, delete)
- Database: Persistent storage for conversations, messages, and existing tasks

## 2. Component & Directory Structure

```
/backend/
├── src/
│   ├── models/
│   │   ├── conversation.py     # Conversation entities
│   │   ├── message.py          # Message entities
│   │   └── task.py             # Existing task model
│   ├── schemas/
│   │   ├── conversation.py     # Conversation schemas
│   │   ├── message.py          # Message schemas
│   │   └── chat.py             # Chat request/response schemas
│   ├── api/
│   │   └── v1/
│   │       ├── chat.py         # Chat API endpoints
│       └── tasks.py            # Existing task endpoints
│   ├── services/
│   │   ├── conversation_service.py  # Conversation management
│   │   ├── message_service.py       # Message operations
│   │   └── task_service.py          # Existing task service
│   ├── mcp/
│   │   ├── server.py           # MCP server implementation
│   │   ├── tools/
│   │   │   ├── task_tools.py   # Task operation tools
│   │   │   └── __init__.py
│   ├── agents/
│   │   ├── chat_agent.py       # Main AI agent
│   │   └── runner.py           # Agent execution logic
│   └── config/
│       └── settings.py         # Configuration including Cohere API key

/frontend/
├── app/
│   └── (protected)/
│       ├── dashboard/
│       │   ├── chat-panel.tsx  # Chat panel component
│       │   └── page.tsx        # Dashboard page with chat integration
├── components/
│   └── chat/
│       ├── floating-chat-icon.tsx  # Floating chat icon
│       ├── chat-window.tsx         # Chat window interface
│       ├── message-bubble.tsx      # Individual message display
│       └── message-input.tsx       # Message input field
└── lib/
    └── api.ts                    # Chat API client functions
```

## 3. Agent Execution Lifecycle (Stateless Request Cycle)

Each chat request follows this stateless pattern:

1. **Request Arrival**: User sends message to `/api/chat`
2. **Authentication**: Validate JWT token and extract user_id
3. **Conversation Load**: Retrieve conversation history from database
4. **Context Assembly**: Combine conversation history with current message
5. **Agent Execution**: Pass context to Cohere-powered agent
6. **Tool Selection**: Agent determines appropriate MCP tool(s) to execute
7. **Tool Execution**: Execute selected tools with user context
8. **Response Generation**: Agent generates natural language response
9. **Persistence**: Save user message and AI response to database
10. **Response Return**: Send AI response back to frontend

**Key Properties:**
- No server-side session state maintained
- Each request contains all necessary context
- Conversation history retrieved from persistent storage
- All user data isolated by user_id

## 4. MCP Tool Interaction Flow

MCP (Model Context Protocol) Server acts as the single interface for all task operations:

```
AI Agent → MCP Server → MCP Tools → Task Service → Database
```

**Available MCP Tools:**
- `create_task(title: str, description: str)` → Task
- `get_tasks(filter_completed: bool = None)` → List[Task]
- `update_task(task_id: str, title: str = None, description: str = None, completed: bool = None)` → Task
- `delete_task(task_id: str)` → bool
- `toggle_task_completion(task_id: str)` → Task

**Security Enforcement:**
- Each tool validates user_id matches task's owner
- User isolation enforced at database query level
- No direct database access from agent

## 5. Frontend Chatbot UI Integration Plan

### Components:
- **Floating Chat Icon**: Fixed position button that appears on all pages
- **Expandable Chat Panel**: Slides in from bottom/right when activated
- **Chat Window**: Displays conversation history with message bubbles
- **Input Area**: Text input with send button for new messages
- **Loading States**: Visual feedback during AI processing

### User Experience:
- Smooth animations for opening/closing chat panel
- Real-time message display as they arrive
- Typing indicators during AI processing
- Error handling for API failures
- Responsive design for mobile/desktop

---

## Phase-by-Phase Implementation Plan

### Phase 1: Architecture Alignment & Environment Setup
**Duration:** Day 1
**Dependencies:** None

#### Tasks:
- [ ] Update requirements.txt with Cohere SDK and MCP server dependencies
- [ ] Add COHERE_API_KEY to environment variables
- [ ] Verify existing authentication system works with new components
- [ ] Set up development environment with Cohere API access

#### Deliverables:
- Environment properly configured with Cohere integration
- Authentication system verified for user isolation
- Development ready for implementation

### Phase 2: Database Models for Conversations & Messages
**Duration:** Day 1
**Dependencies:** Phase 1 complete

#### Tasks:
- [ ] Create Conversation model with user_id relationship
- [ ] Create Message model with conversation_id, role (user/assistant), content
- [ ] Update database initialization script to include new tables
- [ ] Implement basic CRUD operations for conversation/message entities
- [ ] Add indexes for efficient querying by user_id and conversation_id

#### Deliverables:
- New database tables for conversations and messages
- Proper indexing for performance
- Basic service layer for conversation operations

### Phase 3: MCP Server Implementation (Task Tools)
**Duration:** Day 2
**Dependencies:** Phase 2 complete

#### Tasks:
- [ ] Implement MCP server following Model Context Protocol standards
- [ ] Create task operation tools that wrap existing TaskService
- [ ] Add user validation to ensure data isolation
- [ ] Implement tool registration and discovery mechanisms
- [ ] Add error handling and validation for all tools
- [ ] Unit tests for MCP tools

#### Deliverables:
- Functional MCP server
- Secure task operation tools
- Proper user isolation enforcement
- Comprehensive test coverage

### Phase 4: AI Agent & Runner Implementation (Cohere-Powered)
**Duration:** Day 2-3
**Dependencies:** Phase 3 complete

#### Tasks:
- [ ] Implement Cohere-powered chat agent
- [ ] Create agent runner with conversation context management
- [ ] Implement tool selection and execution logic
- [ ] Add conversation history assembly from database
- [ ] Handle multi-turn conversations and context management
- [ ] Implement error recovery and fallback responses
- [ ] Unit tests for agent functionality

#### Deliverables:
- Production-ready AI agent
- Proper context management
- Tool execution capability
- Robust error handling

### Phase 5: Stateless Chat API Endpoint
**Duration:** Day 1
**Dependencies:** Phase 4 complete

#### Tasks:
- [ ] Create `/api/chat` endpoint in FastAPI
- [ ] Implement JWT authentication and user extraction
- [ ] Add conversation persistence logic
- [ ] Implement request/response validation
- [ ] Add rate limiting and security measures
- [ ] API documentation and testing

#### Deliverables:
- Secure, stateless chat API
- Proper authentication and authorization
- Complete API documentation

### Phase 6: Frontend Chatbot UI Integration
**Duration:** Day 2-3
**Dependencies:** Phase 5 complete

#### Tasks:
- [ ] Create floating chat icon component
- [ ] Implement expandable chat panel with animations
- [ ] Build chat window with message bubbles
- [ ] Create message input with send functionality
- [ ] Implement real-time message display
- [ ] Add loading states and error handling
- [ ] Integrate with backend chat API
- [ ] Responsive design for all screen sizes
- [ ] Accessibility compliance

#### Deliverables:
- Polished, user-friendly chat interface
- Smooth animations and transitions
- Fully integrated with backend API
- Responsive and accessible design

### Phase 7: End-to-End Validation & Demo Readiness
**Duration:** Day 1
**Dependencies:** All previous phases complete

#### Tasks:
- [ ] Complete end-to-end testing of all chat functionalities
- [ ] Validate user isolation (can't access other users' tasks)
- [ ] Test conversation persistence across server restarts
- [ ] Performance testing and optimization
- [ ] Security validation and penetration testing
- [ ] Demo preparation and documentation
- [ ] Clean up and code review

#### Deliverables:
- Fully functional and tested chatbot
- Validated security and user isolation
- Optimized performance
- Demo-ready application

---

## Identified Risks & Mitigations

### Technical Risks

**Risk 1: Cohere API Rate Limits**
- **Impact**: Chat functionality becomes unavailable during high usage
- **Mitigation**: Implement request queuing, caching, and graceful degradation

**Risk 2: Long Conversation Context Exceeding Token Limits**
- **Impact**: AI becomes unable to process long conversations
- **Mitigation**: Implement conversation summarization and context window management

**Risk 3: Database Performance with Growing Conversation History**
- **Impact**: Slow response times as conversation history grows
- **Mitigation**: Proper indexing, pagination, and archival strategies

**Risk 4: Authentication Bypass in MCP Tools**
- **Impact**: Users could access other users' tasks
- **Mitigation**: Multiple layers of validation, extensive testing, code reviews

### Operational Risks

**Risk 5: Cohere API Downtime**
- **Impact**: Chat functionality unavailable
- **Mitigation**: Fallback messaging, graceful degradation to manual task management

**Risk 6: Misinterpretation of User Intentions**
- **Impact**: Incorrect task operations based on misunderstood commands
- **Mitigation**: Confidence scoring, confirmation prompts for destructive operations

---

## Readiness Checklist for Phase III Completion

### Functional Requirements
- [ ] Users can add tasks via natural language: "Add a task to buy groceries"
- [ ] Users can list tasks via natural language: "Show my pending tasks"
- [ ] Users can update tasks via natural language: "Change task 1 to call mom tonight"
- [ ] Users can complete tasks via natural language: "Mark task 3 as complete"
- [ ] Users can delete tasks via natural language: "Delete the meeting task"
- [ ] User isolation maintained - cannot access other users' tasks
- [ ] All operations routed through MCP tools only
- [ ] Conversations persist across server restarts

### Non-Functional Requirements
- [ ] Stateless architecture - no server-side session memory
- [ ] Response times under 3 seconds for typical queries
- [ ] Cohere API properly integrated with environment variables
- [ ] Floating chat icon available on all application pages
- [ ] Modern, responsive chat panel interface
- [ ] Proper error handling and user feedback
- [ ] Existing task functionality unchanged and working

### Security Requirements
- [ ] JWT authentication validated for all requests
- [ ] User ID properly extracted and enforced in all operations
- [ ] Database queries properly scoped to user_id
- [ ] MCP tools validate user ownership of tasks
- [ ] No direct database access from AI agent

### Quality Requirements
- [ ] Unit tests covering >80% of new code
- [ ] Integration tests for end-to-end workflows
- [ ] Error handling for all edge cases
- [ ] Code review completed by team member
- [ ] Performance benchmarks met
- [ ] Security scanning passed

### Documentation Requirements
- [ ] API documentation updated
- [ ] Architecture diagram created
- [ ] Deployment instructions updated
- [ ] User guide for chat functionality
- [ ] Troubleshooting guide for common issues