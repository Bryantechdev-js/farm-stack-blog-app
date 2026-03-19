from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Load environment variables FIRST
load_dotenv()

from app.api import auth, posts, admin
from app.core.logging import setup_logging
from app.core.middleware import auth_middleware

setup_logging()
app = FastAPI(title="Secure Blog")

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

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[ERROR] Unhandled exception: {str(exc)}")
    import traceback
    traceback.print_exc()
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

# Health check endpoint (no auth required)
@app.get("/health")
async def health():
    return {"status": "ok"}