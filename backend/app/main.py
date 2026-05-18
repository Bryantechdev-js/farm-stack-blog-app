from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
import os
import logging

# Load environment variables FIRST
load_dotenv()

from app.api import auth, posts, admin, admin_analytics
from app.core.logging import setup_logging
from app.core.middleware import auth_middleware

logger = setup_logging()
app = FastAPI(title="Secure Blog")

logger.info("FastAPI application initialized")

# Add CORS middleware FIRST and ONLY (before everything else)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*", "Set-Cookie"],
    max_age=3600,
)

# Add auth middleware
app.middleware("http")(auth_middleware)

# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_messages = []
    for error in errors:
        field = error.get("loc", ["unknown"])[-1]
        msg = error.get("msg", "Invalid value")
        error_messages.append(f"{field}: {msg}")
    
    detail = " | ".join(error_messages) if error_messages else "Invalid request"
    logger.warning(f"Validation error: {detail}")
    
    return JSONResponse(
        status_code=422,
        content={"detail": detail}
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Mount uploads directory
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(admin.router)
app.include_router(admin_analytics.router)

# Health check endpoint (no auth required)
@app.get("/health")
async def health():
    return {"status": "ok"}