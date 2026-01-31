# Quickstart Guide: Todo AI Chatbot Integration

## Getting Started

This guide will help you set up and run the Todo AI Chatbot application locally.

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn package manager
- Cohere API Key (free tier available)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Hackathon-2_phase-3
```

### 2. Backend Setup

Navigate to the backend directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory with your Cohere API key:

```env
COHERE_API_KEY=your_cohere_api_key_here
BETTER_AUTH_SECRET=your_random_secret_key
DATABASE_URL=sqlite:///./todo_app_dev.db
LOG_LEVEL=INFO
```

Initialize the database:

```bash
python initialize_db.py
```

Start the backend server:

```bash
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup

Open a new terminal, navigate to the frontend directory and install dependencies:

```bash
cd frontend  # from root directory
npm install
```

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Start the frontend development server:

```bash
npm run dev
```

## Running the Application

1. Make sure both backend (port 8000) and frontend (port 3000) servers are running
2. Open your browser and navigate to `http://localhost:3000`
3. Sign up or log in to the application
4. Look for the floating chat icon in the bottom-right corner of the screen
5. Click the icon to open the chat panel and start interacting with the AI

## Sample Commands

Try these sample commands with the chatbot:

- "Add a task to buy groceries"
- "Show my pending tasks"
- "Mark task 1 as complete"
- "Update task 1 to call mom tomorrow"
- "Delete the meeting task"
- "What tasks do I have?"

## Development Mode

To enable hot reloading during development:

Backend:
```bash
uvicorn src.main:app --reload --port 8000
```

Frontend:
```bash
npm run dev
```

## Testing the API

You can test the chat API directly using curl:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}'
```

## Troubleshooting

### Common Issues

1. **Cohere API Key Not Working**
   - Verify your API key is correct
   - Check that you have sufficient quota
   - Ensure the environment variable is properly set

2. **Database Connection Issues**
   - Verify the DATABASE_URL is correct
   - Check that the database file has proper permissions
   - Run `python initialize_db.py` again

3. **Frontend Cannot Connect to Backend**
   - Ensure backend is running on port 8000
   - Verify NEXT_PUBLIC_API_BASE_URL is set correctly
   - Check browser console for CORS errors

4. **Authentication Errors**
   - Make sure you're logged in through the UI first
   - Verify JWT token is being sent with requests
   - Check that BETTER_AUTH_SECRET matches between frontend and backend

### Verifying Setup

To verify everything is working:

1. Visit `http://localhost:8000/health` - should return a health status
2. Visit `http://localhost:3000` - should load the application
3. Try logging in and adding a task manually
4. Open the chat panel and try a simple command like "Show my tasks"

## Next Steps

Once you have the application running:

1. Explore the different task management commands
2. Test user isolation by creating multiple accounts
3. Review the code structure in the `specs/004-ai-chatbot/` directory
4. Check out the API documentation at `http://localhost:8000/docs`