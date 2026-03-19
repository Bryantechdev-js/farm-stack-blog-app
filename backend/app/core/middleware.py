from fastapi import Request
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from app.core.security import SECRET, ALGO

async def auth_middleware(request: Request, call_next):
    # Allow CORS preflight requests (OPTIONS)
    if request.method == "OPTIONS":
        return await call_next(request)
    
    # Public endpoints that don't require authentication
    public_paths = ["/auth/login", "/auth/signup", "/health", "/docs", "/redoc", "/openapi.json"]
    if request.url.path in public_paths:
        return await call_next(request)
    
    # Check for authentication token
    token = request.cookies.get("access_token")
    if not token:
        return JSONResponse(
            status_code=401,
            content={"detail": "Not authenticated"}
        )
    
    try:
        jwt.decode(token, SECRET, algorithms=[ALGO])
        return await call_next(request)
    except JWTError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or expired token"}
        )