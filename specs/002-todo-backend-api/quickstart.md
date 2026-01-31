# Quickstart Guide: Todo Backend API

## Overview
This guide provides instructions for setting up, running, and testing the Todo Backend API.

## Prerequisites
- Python 3.11+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- Better Auth configured (external dependency)
- Docker and Docker Compose (optional, for containerized deployment)

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development/testing
```

### 4. Environment Variables
Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
NEON_DB_URL=postgresql://username:password@host:port/database

# Better Auth Configuration
BETTER_AUTH_SECRET=your-better-auth-secret-key
BETTER_AUTH_URL=https://your-domain.better-auth.com

# Optional: Development/Production settings
DEBUG=true  # Set to false for production
LOG_LEVEL=info
```

## Running the Application

### Development Mode
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
cd backend
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker
```bash
docker-compose up --build
```

## API Endpoints

### Authentication Required
All endpoints require a valid JWT in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Available Endpoints

#### List User Tasks
```
GET /api/tasks
```
Returns a list of tasks belonging to the authenticated user.

#### Create Task
```
POST /api/tasks
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description (optional)",
  "completed": false
}
```

#### Get Task Details
```
GET /api/tasks/{task_id}
```
Returns details of a specific task owned by the user.

#### Update Task
```
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

#### Delete Task
```
DELETE /api/tasks/{task_id}
```
Deletes a specific task owned by the user.

#### Toggle Task Completion
```
PATCH /api/tasks/{task_id}/complete
```
Toggles the completion status of a task.

## Testing

### Running Tests
```bash
cd backend
pytest tests/ -v
```

### Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
```

## Database Migrations

### Create Migration
```bash
alembic revision --autogenerate -m "Migration description"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Downgrade
```bash
alembic downgrade -1
```

## Configuration

### Settings Location
Configuration is managed in `src/config/settings.py` and loads from environment variables.

### Key Configuration Options
- `NEON_DB_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret for JWT verification
- `BETTER_AUTH_URL`: Origin for CORS configuration
- `DEBUG`: Enable/disable debug mode

## Troubleshooting

### Common Issues

#### JWT Authentication Fails
- Verify `BETTER_AUTH_SECRET` matches the one used by Better Auth
- Check that JWT tokens are properly formatted
- Ensure tokens are not expired

#### Database Connection Issues
- Verify `NEON_DB_URL` is correct
- Check that PostgreSQL server is accessible
- Confirm database credentials are valid

#### CORS Issues
- Ensure `BETTER_AUTH_URL` is correctly set
- Verify frontend origin matches configured CORS settings

### Logs
Application logs are output to stdout in JSON format for easy parsing and monitoring.

## Deployment

### Docker Compose
Use the provided `docker-compose.yml` for easy deployment:
```bash
docker-compose up -d
```

### Environment Variables for Production
Ensure the following environment variables are set in production:
- `NEON_DB_URL`
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_URL`
- `DEBUG=false`
- `LOG_LEVEL=warning`