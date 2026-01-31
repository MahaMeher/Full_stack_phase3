# Todo AI Chatbot Integration (Phase III)

## Overview

This phase implements an AI-powered conversational chatbot integrated into the existing Full-Stack Todo Application. The chatbot allows authenticated users to manage their tasks using natural language commands, following an agentic, tool-driven, stateless architecture.

## Architecture

### High-Level Flow
```
Frontend Chat UI → Chat API Endpoint → AI Agent Runner → MCP Tools → Database
     ↑                                      ↓
   Floating       ← Conversation/Messages    ← Task Operations
   Panel                               Persisted
```

### Key Components
- **Frontend**: React-based chat interface with floating icon and expandable panel
- **Chat API**: Stateless endpoint that accepts user messages and returns AI responses
- **AI Agent Runner**: Cohere-powered agent that interprets natural language and selects appropriate MCP tools
- **MCP Tools**: Standardized interface for task operations (create, read, update, delete)
- **Database**: Persistent storage for conversations, messages, and existing tasks

## Features

### Natural Language Task Management
- Add tasks: "Add a task to buy groceries"
- List tasks: "Show my pending tasks"
- Update tasks: "Change task 1 to call mom tonight"
- Complete tasks: "Mark task 3 as complete"
- Delete tasks: "Delete the meeting task"

### Context-Aware Conversations
- Multi-turn conversation support
- Conversation history persistence
- Context maintenance across interactions

### User Isolation
- Complete separation of user data
- Authentication enforced at every level
- MCP tools validate user ownership

## Technical Implementation

### Backend Architecture
- **Framework**: FastAPI
- **Database**: SQLModel with SQLite
- **AI Provider**: Cohere API
- **Authentication**: JWT with Better Auth
- **Architecture**: Stateless, tool-driven agent

### Frontend Architecture
- **Framework**: Next.js with React
- **Styling**: Tailwind CSS
- **UI Components**: Custom chat interface with floating panel
- **State Management**: Client-side only

### MCP (Model Context Protocol) Server
The MCP server acts as the single interface for all task operations:
- `create_task()` - Create new tasks
- `get_tasks()` - Retrieve tasks with filters
- `update_task()` - Update task properties
- `delete_task()` - Delete tasks
- `toggle_task_completion()` - Toggle completion status

All operations enforce user isolation through validation.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- Cohere API Key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   BETTER_AUTH_SECRET=your_auth_secret
   DATABASE_URL=sqlite:///./todo_app_dev.db
   ```

4. Initialize the database:
   ```bash
   python initialize_db.py
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Chat API
- `POST /api/chat` - Send message to AI chatbot
  - Headers: `Authorization: Bearer {jwt_token}`
  - Request: `{ "message": "natural language command" }`
  - Response: `{ "response": "ai response", "conversation_id": "uuid" }`

### Existing Task API
All original task endpoints remain unchanged and fully functional.

## Security

### Authentication
- JWT-based authentication for all API requests
- User ID extracted from JWT and validated for all operations
- Session-free, stateless architecture

### Authorization
- MCP tools enforce user ownership validation
- Database queries scoped to authenticated user
- No cross-user data access possible

### Data Protection
- All sensitive data encrypted in transit (HTTPS)
- API keys stored securely in environment variables
- Input validation on all user-facing endpoints

## Testing

### Unit Tests
Run backend unit tests:
```bash
cd backend
pytest tests/
```

### Integration Tests
Test the complete chatbot workflow:
```bash
# Start both backend and frontend
# Navigate to the application and test chat functionality
```

### Security Tests
Verify user isolation:
1. Log in as User A
2. Add several tasks
3. Log out and log in as User B
4. Verify User B cannot see User A's tasks
5. Test chatbot operations as both users

## Performance

### Response Times
- AI responses: Under 3 seconds for typical queries
- Database operations: Under 100ms
- API round trips: Under 200ms

### Scalability
- Stateless architecture enables horizontal scaling
- Database connection pooling for efficiency
- Caching strategies for common operations

## Deployment

### Backend Deployment
Deploy to cloud platforms supporting Python applications (Heroku, AWS, etc.)

### Frontend Deployment
Deploy to Vercel, Netlify, or similar platforms supporting Next.js applications.

### Environment Variables
Ensure the following environment variables are set in production:
- `COHERE_API_KEY`
- `BETTER_AUTH_SECRET`
- `DATABASE_URL`
- `ALLOWED_ORIGINS` (for CORS)

## Troubleshooting

### Common Issues
1. **Cohere API Connection Errors**: Verify API key is correct and has sufficient quota
2. **Authentication Failures**: Check JWT token validity and secret configuration
3. **Database Connection Issues**: Verify database URL and connection parameters
4. **Cross-Origin Errors**: Confirm allowed origins configuration

### Logging
- Backend logs available in console output
- API request/response logging enabled
- Error tracking for debugging purposes

## Development Guidelines

### Adding New MCP Tools
1. Create new tool function in MCP tools module
2. Register tool with MCP server
3. Add proper user validation
4. Implement error handling
5. Add unit tests

### Modifying Chat Agent Behavior
1. Update agent configuration in agent runner
2. Modify prompt engineering if needed
3. Test with various natural language inputs
4. Verify user isolation still enforced

### Extending Frontend UI
1. Maintain consistent design language
2. Preserve existing functionality
3. Ensure responsive design
4. Test accessibility features

## Architecture Decisions

### Why Cohere?
- Reliable API with good natural language understanding
- Easy integration with Python applications
- Good performance for tool-use cases
- Cost-effective for our use case

### Why MCP Server?
- Centralized tool interface
- Enforced user isolation
- Standardized tool contracts
- Easy to extend with new tools

### Why Stateless Architecture?
- Better scalability
- Reduced server memory usage
- Easier debugging and monitoring
- Consistent user experience

## Future Enhancements

### Planned Features
- Voice input support
- Advanced conversation summarization
- Customizable AI personalities
- Advanced task categorization

### Performance Improvements
- Response caching for common queries
- Optimized conversation context management
- Database query optimization
- CDN for static assets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the architecture guidelines
4. Add tests for new functionality
5. Submit a pull request with detailed description

## License

This project is licensed under the MIT License - see the LICENSE file for details.