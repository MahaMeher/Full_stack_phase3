# Todo AI Chatbot Architecture Diagram

## High-Level Architecture Flow

```
Frontend Chat UI → Chat API Endpoint → AI Agent Runner → MCP Tools → Database
     ↑                                      ↓
   Floating       ← Conversation/Messages    ← Task Operations
   Panel                               Persisted
```

## Component Interaction

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │   Backend API    │    │   AI Agent &     │
│   Components    │◄──►│   (FastAPI)      │◄──►│   MCP Server     │
│                 │    │                  │    │                  │
│ • Floating Chat │    │ • /api/chat      │    │ • Cohere Agent   │
│ • Chat Window   │    │ • Authentication │    │ • Tool Registry  │
│ • Message       │    │ • Conversation   │    │ • MCP Tools      │
│   Display       │    │   Management     │    │   (add, list,    │
│ • Message Input │    │                  │    │   update, etc.)  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                                      │
                                                      ▼
                                      ┌─────────────────────────────┐
                                      │        Database             │
                                      │                             │
                                      │ • Conversations (user_id)   │
                                      │ • Messages (conversation_id)│
                                      │ • Tasks (user_id)           │
                                      │ • Users                     │
                                      └─────────────────────────────┘
```

## Data Flow for Chat Request

```
1. User sends message to /api/chat
2. ┌─────────────────────────────────────────────────────────────────┐
   │ Authentication: Validate JWT token and extract user_id          │
   └─────────────────────────────────────────────────────────────────┘
3. ┌─────────────────────────────────────────────────────────────────┐
   │ Conversation Load: Retrieve conversation history from database  │
   └─────────────────────────────────────────────────────────────────┘
4. ┌─────────────────────────────────────────────────────────────────┐
   │ Context Assembly: Combine conversation history with message     │
   └─────────────────────────────────────────────────────────────────┘
5. ┌─────────────────────────────────────────────────────────────────┐
   │ Agent Execution: Pass context to Cohere-powered agent           │
   └─────────────────────────────────────────────────────────────────┘
6. ┌─────────────────────────────────────────────────────────────────┐
   │ Tool Selection: Agent determines appropriate MCP tool(s)        │
   └─────────────────────────────────────────────────────────────────┘
7. ┌─────────────────────────────────────────────────────────────────┐
   │ Tool Execution: Execute selected tools with user context        │
   └─────────────────────────────────────────────────────────────────┘
8. ┌─────────────────────────────────────────────────────────────────┐
   │ Response Generation: Agent generates natural language response  │
   └─────────────────────────────────────────────────────────────────┘
9. ┌─────────────────────────────────────────────────────────────────┐
   │ Persistence: Save user message and AI response to database      │
   └─────────────────────────────────────────────────────────────────┘
10.┌─────────────────────────────────────────────────────────────────┐
   │ Response Return: Send AI response back to frontend              │
   └─────────────────────────────────────────────────────────────────┘
```

## MCP Tool Interaction Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Agent      │───►│  MCP Server     │───►│  MCP Tools      │
│                 │    │                 │    │                 │
│ • Interprets    │    │ • Tool Registry │    │ • add_task()    │
│   natural       │    │ • Tool Calling  │    │ • list_tasks()  │
│   language      │    │ • Validation    │    │ • update_task() │
│ • Selects       │    │                 │    │ • complete_task()│
│   appropriate   │    │                 │    │ • delete_task() │
│   tool          │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                        ┌─────────────────────────────┐
                                        │   Task Service & Database   │
                                        │                             │
                                        │ • Validates user ownership  │
                                        │ • Performs actual task op   │
                                        │ • Enforces data isolation   │
                                        └─────────────────────────────┘
```

## Key Properties

- **Stateless Architecture**: No server-side session state maintained
- **Each request contains all necessary context**
- **Conversation history retrieved from persistent storage**
- **All user data isolated by user_id**
- **MCP Tools enforce security and validation**
- **Database as single source of truth for conversation state**