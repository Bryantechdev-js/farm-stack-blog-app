# Architecture Explanation - How JWT Cookies Work Now

## The Problem (Before Fixes)

### Request Flow (BROKEN ❌)
```
Browser                Frontend              Backend
  |                      |                      |
  |--login form--------->|                      |
  |                      |--POST http://localhost:8000/auth/login-->|
  |                      |                      |
  |                      |<--301 Redirect /auth/login--|
  |                      |                      |
  |<--redirect-----------|                      |
  |                      |                      |
```

**Why it failed:**
1. Frontend called full URL `http://localhost:8000/auth/login`
2. Backend middleware returned `RedirectResponse` on 401
3. Browser received redirect instead of response with Set-Cookie header
4. Cookie was never stored

### Why Cookies Weren't Stored
- Browser only stores cookies if response is 200-299 (success)
- Redirects (301/302) don't set cookies
- Even with `credentials: 'include'`, redirects break the flow

---

## The Solution (After Fixes)

### Request Flow (WORKING ✅)
```
Browser                Frontend              Next.js Proxy         Backend
  |                      |                      |                      |
  |--login form--------->|                      |                      |
  |                      |--POST /api/auth/login|                      |
  |                      |                      |--POST /auth/login--->|
  |                      |                      |                      |
  |                      |                      |<--200 + Set-Cookie---|
  |                      |<--200 + Set-Cookie--|                      |
  |<--200 + Set-Cookie---|                      |                      |
  |                      |                      |                      |
  | [Cookie stored in browser]                 |                      |
  |                      |                      |                      |
```

**Why it works now:**
1. Frontend calls relative path `/api/auth/login`
2. Next.js proxy rewrites to `http://localhost:8000/auth/login`
3. Backend returns `200 OK` with `Set-Cookie` header
4. Browser stores cookie automatically (same origin)
5. All subsequent requests include cookie

---

## Key Components

### 1. Frontend (Next.js)
**File**: `frontend/next.config.ts`
```typescript
rewrites: async () => {
  return {
    beforeFiles: [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ],
  };
}
```

**What it does:**
- Intercepts all requests to `/api/*`
- Rewrites them to `http://localhost:8000/*`
- Browser sees same origin (localhost:3000)
- Cookies are stored automatically

### 2. Frontend API Calls
**File**: `frontend/src/app/auth/login/page.tsx`
```typescript
const res = await fetch(`/api/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
  credentials: 'include',  // Include cookies
});
```

**What it does:**
- Uses relative path `/api/auth/login`
- Includes `credentials: 'include'` to send/receive cookies
- Next.js proxy handles the rewrite

### 3. Backend Response
**File**: `backend/app/api/auth.py`
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,      # Can't be accessed by JavaScript
    secure=False,       # True only in HTTPS
    samesite="lax",     # Works with local development
    max_age=3600,       # 1 hour
    path="/",           # Available for all paths
)
return {
    "message": "Login successful",
    "user": {...}
}
```

**What it does:**
- Sets httpOnly cookie (secure)
- Returns 200 OK (not redirect)
- Browser stores cookie automatically

### 4. Backend Middleware (FIXED)
**File**: `backend/app/core/middleware.py`
```python
# BEFORE (BROKEN ❌)
return RedirectResponse("/auth/login")

# AFTER (FIXED ✅)
return JSONResponse(
    status_code=401,
    content={"detail": "Not authenticated"}
)
```

**Why it matters:**
- API calls expect JSON responses
- Redirects break the API contract
- Frontend can now handle 401 properly

### 5. Frontend 401 Handling
**All pages**:
```typescript
if (res.status === 401) {
  router.push('/auth/login');
  return;
}
```

**What it does:**
- Catches 401 responses
- Redirects to login page
- Handles token expiration gracefully

---

## Cookie Flow Diagram

### Login
```
1. User enters credentials
   ↓
2. Frontend: POST /api/auth/login
   ↓
3. Next.js rewrites to: POST http://localhost:8000/auth/login
   ↓
4. Backend validates credentials
   ↓
5. Backend sets cookie: Set-Cookie: access_token=JWT; HttpOnly; Path=/
   ↓
6. Backend returns: 200 OK + user data
   ↓
7. Browser receives response with Set-Cookie header
   ↓
8. Browser stores cookie automatically
   ↓
9. Frontend redirects to dashboard
```

### Subsequent Requests
```
1. User navigates to dashboard
   ↓
2. Frontend: GET /api/auth/me
   ↓
3. Browser automatically includes cookie in request
   ↓
4. Next.js rewrites to: GET http://localhost:8000/auth/me
   ↓
5. Backend receives request with cookie
   ↓
6. Backend extracts JWT from cookie
   ↓
7. Backend validates JWT
   ↓
8. Backend returns: 200 OK + user data
   ↓
9. Frontend displays dashboard
```

### Logout
```
1. User clicks logout
   ↓
2. Frontend: POST /api/auth/logout
   ↓
3. Backend deletes cookie: Set-Cookie: access_token=; Max-Age=0
   ↓
4. Browser receives response with delete cookie header
   ↓
5. Browser deletes cookie
   ↓
6. Frontend redirects to home page
```

---

## Why This Architecture Works

### ✅ Same Origin Policy
- Browser sees all requests as coming from `localhost:3000`
- Cookies are stored automatically
- No CORS issues with credentials

### ✅ Security
- httpOnly cookies can't be accessed by JavaScript
- Prevents XSS attacks
- Secure flag (in production) requires HTTPS

### ✅ Simplicity
- No token in localStorage (vulnerable to XSS)
- No manual cookie handling
- Browser handles everything automatically

### ✅ Scalability
- Works with any backend URL
- Works with proxies and load balancers
- Works with Docker and Kubernetes

---

## Comparison: Before vs After

| Aspect | Before ❌ | After ✅ |
|--------|----------|---------|
| API URL | `http://localhost:8000/auth/login` | `/api/auth/login` |
| Proxy | None | Next.js rewrites |
| Middleware | Returns redirect | Returns JSON |
| Cookie Storage | Failed | Works ✅ |
| CRUD Operations | Failed | Works ✅ |
| Dashboard | Infinite loading | Loads correctly |
| Error Handling | Broken | Proper 401 handling |

---

## Production Deployment

### Local Development
```
Browser (localhost:3000)
    ↓
Next.js Dev Server (rewrites /api to localhost:8000)
    ↓
Backend (localhost:8000)
```

### Docker Compose
```
Browser (localhost:80)
    ↓
Nginx (localhost:80)
    ├─→ /api → backend:8000
    └─→ / → frontend:3000
```

### Production (AWS/Vercel)
```
Browser (example.com)
    ↓
CDN (example.com)
    ↓
API Gateway (api.example.com)
    ↓
Backend (private)
```

---

## Security Considerations

### ✅ What We Have
- httpOnly cookies (can't be stolen by XSS)
- SameSite=Lax (prevents CSRF)
- JWT expiration (1 hour)
- Argon2 password hashing

### 🔒 What to Add (Production)
- HTTPS (secure=True in cookies)
- Refresh tokens (extend session without re-login)
- CSRF tokens (for state-changing operations)
- Rate limiting (prevent brute force)
- Request logging (audit trail)
- Error tracking (Sentry)

---

## Troubleshooting Guide

### Cookie Not Stored
**Check:**
1. Is backend returning 200 (not redirect)?
2. Is Set-Cookie header present?
3. Is frontend using relative path?
4. Is credentials: 'include' set?

**Fix:**
1. Verify middleware returns JSONResponse
2. Verify next.config.ts has rewrites
3. Verify frontend uses `/api/` paths

### Dashboard Infinite Loading
**Check:**
1. Is `/api/auth/me` returning 200?
2. Is cookie being sent with request?
3. Is backend validating JWT correctly?

**Fix:**
1. Check backend logs for errors
2. Verify JWT_SECRET is set
3. Verify token is valid

### CRUD Operations Failing
**Check:**
1. Is 401 error in console?
2. Is cookie present in DevTools?
3. Is backend returning JSON (not redirect)?

**Fix:**
1. Login again to refresh token
2. Check backend middleware
3. Verify posts.py get_current_user function

---

## Summary

The JWT cookie issue was solved by:
1. **Fixing middleware** to return JSON instead of redirects
2. **Using relative paths** in frontend API calls
3. **Adding Next.js proxy** to rewrite `/api` to backend
4. **Proper 401 handling** to redirect on auth failure

This creates a clean, secure, and scalable authentication flow that works across all environments.
