from fastapi import FastAPI, Depends, HTTPException, status, Request
from contextlib import asynccontextmanager
from typing import List
from sqlmodel import Session
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from datetime import datetime
import logging
import json

# Load environment variables FIRST before importing modules that need them
load_dotenv()

# Configure structured JSON logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}',
    datefmt='%Y-%m-%dT%H:%M:%S'
)

logger = logging.getLogger(__name__)

# Now import modules that depend on environment variables
from database.session import get_session, create_db_and_tables
from models.todo import TodoTask
from schemas.todo import (
    TodoTaskRead,
    TodoTaskCreate,
    TodoTaskUpdate,
    TodoTaskToggleComplete,
    ErrorResponse
)
from core.services.todo_service import (
    get_all_tasks_for_user,
    get_task_by_id_for_user,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion
)
from core.config import get_config, init_config
from core.services.email_service import SMTPEmailService, EmailService

# Global email service instance
_email_service: EmailService = None


def get_email_service() -> EmailService:
    """
    Dependency to get the email service instance

    Returns:
        EmailService instance

    Raises:
        RuntimeError: If email service is not initialized
    """
    if _email_service is None:
        raise RuntimeError("Email service not initialized. Call init_email_service() first.")
    return _email_service


def init_email_service():
    """
    Initialize the email service with SMTP configuration
    """
    global _email_service
    try:
        config = get_config()
        _email_service = SMTPEmailService(config.smtp)
    except Exception as e:
        # Log error but don't fail startup - email service is optional
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to initialize email service: {str(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to initialize the database and email service on startup

    Validates required environment variables and fails fast if missing.
    """
    # Validate required environment variables on startup
    required_vars = ["DATABASE_URL", "JWT_SECRET_KEY", "FRONTEND_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    # Validate JWT_SECRET_KEY length (minimum 32 characters for security)
    jwt_secret = os.getenv("JWT_SECRET_KEY", "")
    if len(jwt_secret) < 32:
        error_msg = "JWT_SECRET_KEY must be at least 32 characters long"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    logger.info("Environment validation passed")

    await create_db_and_tables()
    logger.info("Database tables created/verified")

    # Initialize configuration
    try:
        init_config()
        logger.info("Configuration initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize config: {str(e)}")

    # Initialize email service
    init_email_service()
    logger.info("Email service initialized")

    logger.info("Application startup complete")

    yield


# Create FastAPI app with lifespan event handler
app = FastAPI(
    title="Todo API",
    description="REST API for todo management with JWT-based authentication and user isolation",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS with specific origin from environment
# In production, this should be set to the frontend URL (e.g., https://your-app.vercel.app)
try:
    config = get_config()
    allowed_origins = [config.frontend_url] if config.frontend_url else ["http://localhost:3000"]
except Exception:
    # Fallback to localhost for development if config not available
    allowed_origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specific origin, not wildcard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Add security headers to all responses

    Headers:
        - X-Content-Type-Options: Prevent MIME type sniffing
        - X-Frame-Options: Prevent clickjacking
        - X-XSS-Protection: Enable XSS filter
        - Strict-Transport-Security: Enforce HTTPS
        - Content-Security-Policy: Restrict resource loading
        - Referrer-Policy: Control referrer information
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

from api.tasks import router as tasks_router
from api.auth import router as auth_router

# Include the authentication API router
app.include_router(auth_router, prefix="/api", tags=["auth"])

# Include the tasks API router with user_id in path pattern
# Router already has prefix="/{user_id}/tasks", so final pattern is /api/{user_id}/tasks
app.include_router(tasks_router, prefix="/api")


@app.get("/health")
async def health_check(session: Session = Depends(get_session)):
    """
    Health check endpoint for container monitoring

    Returns:
        200 OK if healthy with status details
        503 Service Unavailable if unhealthy

    Checks:
        - Database connection is active
        - SMTP configuration is valid
    """
    status_code = 200
    health_status = "healthy"
    errors = []

    # Check database connection
    db_status = "disconnected"
    try:
        # Simple query to test database connection
        session.exec("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = "error"
        errors.append(f"Database: {str(e)}")
        health_status = "unhealthy"
        status_code = 503

    # Check SMTP configuration
    smtp_status = "not_configured"
    try:
        config = get_config()
        if config.smtp.host and config.smtp.username and config.smtp.from_email:
            smtp_status = "configured"
        else:
            smtp_status = "incomplete"
            errors.append("SMTP: Configuration incomplete")
            health_status = "unhealthy"
            status_code = 503
    except RuntimeError:
        # Config not initialized - this is okay during startup
        smtp_status = "not_initialized"
    except Exception as e:
        smtp_status = "error"
        errors.append(f"SMTP: {str(e)}")
        health_status = "unhealthy"
        status_code = 503

    response_data = {
        "status": health_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "0.1.0",
        "database": db_status,
        "smtp": smtp_status
    }

    if errors:
        response_data["errors"] = errors

    return JSONResponse(
        status_code=status_code,
        content=response_data
    )

@app.get("/")
def route_check():
    """
    Route check endpoint
    """
    return {
        "status": "healthy",
        "message": "Todo API is running",
        "version": "0.1.0"
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Global HTTP exception handler
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler for unexpected errors
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """
    Handler for value errors (like validation errors from user input)
    """
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )