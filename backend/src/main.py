import logging
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from .config.settings import settings
from .api.v1 import tasks
from .api.v1 import users
from .api.routes import chat
import jwt


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


# Set up basic logging configuration
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Create FastAPI app instance
app = FastAPI(
    title="Todo Backend API",
    description="Secure, multi-user todo application API with JWT authentication",
    version="1.0.0"
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.better_auth_url],  # Allow the frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
    # Additional security: expose only necessary headers
    expose_headers=["Access-Control-Allow-Origin"]
)


# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/")
def read_root():
    """Root endpoint for health check"""
    return {"status": "ok", "message": "Todo Backend API is running"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/auth/token")
def generate_token(email: str = Form(...), name: str = Form(None)):
    """Development endpoint to generate JWT token for testing"""
    user_id = f"user_{email.replace('@', '_at_').replace('.', '_dot_')}"

    payload = {
        "id": user_id,
        "email": email,
        "name": name,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=1)  # 24 hours
    }

    token = jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer", "user_id": user_id}