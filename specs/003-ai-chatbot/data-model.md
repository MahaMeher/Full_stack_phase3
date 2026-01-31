# Data Model: Todo AI Chatbot Integration

## Overview

This document defines the data models for the AI Chatbot Integration, including new entities for conversations and messages while maintaining compatibility with existing task and user models.

## Entity Relationships

```
User (1) ←→ (Many) Conversation (1) ←→ (Many) Message
                              ↓
                         (Many) Task (existing)
```

## New Entities

### Conversation Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the conversation |
| user_id | String | Not Null, Indexed | Reference to the user who owns this conversation |
| created_at | DateTime | Not Null | Timestamp when conversation was created |
| updated_at | DateTime | Not Null | Timestamp when conversation was last updated |

**Indexes:**
- `idx_conversation_user_id`: Index on user_id for efficient user-based queries

**Foreign Keys:**
- `user_id` references `User.id`

### Message Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the message |
| conversation_id | UUID | Not Null, Indexed, Foreign Key | Reference to the conversation this message belongs to |
| role | String | Not Null, Enum: ['user', 'assistant'] | Indicates whether message is from user or AI assistant |
| content | Text | Not Null, Max 5000 chars | The actual message content |
| timestamp | DateTime | Not Null | When the message was created |
| metadata | JSON | Optional | Additional metadata for the message (tool calls, etc.) |

**Indexes:**
- `idx_message_conversation_id`: Index on conversation_id for efficient conversation-based queries
- `idx_message_timestamp`: Index on timestamp for chronological ordering

**Foreign Keys:**
- `conversation_id` references `Conversation.id`

## Existing Entity Modifications

### Task Entity (No Changes)
The Task entity remains unchanged to maintain backward compatibility:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the task |
| user_id | String | Not Null, Indexed | Reference to the user who owns this task |
| title | String | Not Null, Min 1, Max 200 chars | Task title |
| description | String | Optional, Max 1000 chars | Task description |
| completed | Boolean | Not Null, Default False | Completion status |
| created_at | DateTime | Not Null | When task was created |
| updated_at | DateTime | Not Null | When task was last updated |

### User Entity (No Changes)
The User entity remains unchanged:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String | Primary Key, Not Null | Unique identifier for the user |
| email | String | Not Null, Unique | User's email address |
| name | String | Optional | User's display name |
| password_hash | String | Not Null | Hashed password |
| is_active | Boolean | Not Null, Default True | Account activation status |
| created_at | DateTime | Not Null | When account was created |
| updated_at | DateTime | Not Null | When account was last updated |
| last_login | DateTime | Optional | Last login timestamp |

## Database Schema

### Tables

```sql
-- conversations table
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    INDEX idx_conversation_user_id (user_id)
);

-- messages table
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    metadata JSON,
    FOREIGN KEY (conversation_id) REFERENCES conversations (id),
    INDEX idx_message_conversation_id (conversation_id),
    INDEX idx_message_timestamp (timestamp)
);
```

## Data Integrity Rules

### User Isolation
- All queries must filter by user_id to ensure data isolation
- MCP tools must validate that operations are performed on user-owned resources
- Conversation access restricted to owning user

### Referential Integrity
- Messages must belong to existing conversations
- Conversations must belong to existing users
- No orphaned records allowed

### Data Validation
- Message content limited to 5000 characters
- Role field restricted to 'user' or 'assistant' values
- Timestamps automatically set by the system
- Conversation timestamps updated when new messages are added

## API Contract Implications

### Request/Response Objects

#### Conversation Objects
```typescript
// GET /api/conversations
interface Conversation {
  id: string;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
}

// POST /api/chat
interface ChatRequest {
  message: string;
}

interface ChatResponse {
  response: string;
  conversationId: string;
  timestamp: Date;
}
```

#### Message Objects
```typescript
interface Message {
  id: string;
  conversationId: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}
```

## Migration Strategy

### Database Migration Steps
1. Add conversations table with appropriate indexes
2. Add messages table with appropriate indexes and foreign keys
3. Update existing task_service to maintain compatibility
4. Test data integrity constraints
5. Verify user isolation works correctly

### Backward Compatibility
- All existing API endpoints continue to function
- Existing task operations unaffected
- User authentication remains unchanged
- No breaking changes to existing functionality

## Performance Considerations

### Query Optimization
- Proper indexing on user_id and conversation_id for fast lookups
- Efficient pagination for long conversations
- Batch operations for bulk message retrieval

### Storage Efficiency
- Message content size limits to prevent abuse
- Automatic archival of very old conversations (future enhancement)
- JSON metadata only when needed

### Scalability
- UUID primary keys for distributed systems
- Efficient foreign key relationships
- Indexes optimized for common query patterns

## Security Considerations

### Data Protection
- All user data encrypted at rest (database level)
- API requests authenticated via JWT
- Conversation access limited to owning user
- Message content validation to prevent injection

### Access Control
- MCP tools enforce user ownership validation
- Database queries always filtered by user context
- No direct access to other users' conversations
- Audit trail through timestamp tracking

## Testing Strategy

### Unit Tests
- Test all CRUD operations for conversations and messages
- Verify foreign key constraints
- Test user isolation enforcement
- Validate data integrity rules

### Integration Tests
- End-to-end conversation flow testing
- Multi-user scenario testing
- API contract validation
- Error condition handling

### Performance Tests
- Load testing with concurrent conversations
- Database query performance validation
- Memory usage monitoring
- Response time benchmarks