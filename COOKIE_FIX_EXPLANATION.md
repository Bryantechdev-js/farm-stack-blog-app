# Cookie Storage Issue - Root Cause & Fix

## The Problem

When logging in, the login was successful but the cookie was NOT being stored on the user's device. This caused subsequent requests to fail with 401 Unauthorized errors.

**Symptoms**:
- ✅ Login successful message appears
- ❌ Cookie not stored in browser
- ❌ `/auth/me` endpoint returns 401
- ❌ Cannot create posts (401 error)

## Root Cause Analysis

The issue was caused by a **domain mismatch** between frontend and backend:

### Frontend
- Running on: `http://localhost:3000`
- Making API calls to: `http://127.0.0.1:8000`

### Backend
- Running on: `http://127.0.0.1:8000`
- Setting cookies for: `127.0.0.1` (implicitly)

### The Problem
Browsers treat `localhost` and `127.0.0.1` as **different domains**, even though they point to the same machine. When the frontend (on `localhost:3000`) makes a request to the backend (on `127.0.0.1:8000`), the browser considers this a **cross-origin request**.

For cross-origin requests with cookies, the browser requires:
1. `samesite="none"` on the cookie
2. `secure=True` (HTTPS only)
3. Explicit CORS headers

However, for local development with `http://` (not `https://`), `samesite="none"` with `secure=False` doesn't work in most browsers.

## The Solution

### Step 1: Use Consistent Domain
Changed all frontend API calls from `127.0.0.1` to `localhost`:

**Before**:
```typescript
const API_BASE = 'http://127.0.0.1:8000';
```

**After**:
```typescript
const API_BASE = 'http://localhost:8000';
```

This ensures both frontend and backend use the same domain (`localhost`), making them **same-origin** requests.

### Step 2: Use Correct Cookie Settings
For same-origin requests, we can use `samesite="lax"` which is more compatible:

```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=False,  # OK for local http development
    samesite="lax",  # Works with same-origin requests
    max_age=3600,
    path="/",
)
```

### Step 3: Ensure CORS Headers
The CORS middleware properly exposes the Set-Cookie header:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", ...],
    allow_credentials=True,
    expose_headers=["*", "Set-Cookie"],
)
```

## Files Updated

### Backend
- `backend/app/api/auth.py` - Updated cookie settings to use `samesite="lax"`
- `backend/app/main.py` - Ensured CORS exposes Set-Cookie header

### Frontend
- `frontend/src/app/auth/login/page.tsx` - Changed to `localhost:8000`
- `frontend/src/app/auth/signup/page.tsx` - Changed to `localhost:8000`
- `frontend/src/app/page.tsx` - Changed to `localhost:8000`
- `frontend/src/app/dashboard/page.tsx` - Changed to `localhost:8000`
- `frontend/src/app/profile/page.tsx` - Changed to `localhost:8000`
- `frontend/src/app/posts/[id]/page.tsx` - Changed to `localhost:8000`
- `frontend/src/app/admin/page.tsx` - Changed to `localhost:8000`

## How to Run

### Backend
```bash
cd backend
uvicorn app.main:app --reload --host localhost --port 8000
```

**Important**: Use `localhost` not `127.0.0.1`

### Frontend
```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## Testing the Fix

### 1. Verify Cookie is Set
1. Login at `http://localhost:3000/auth/login`
2. Open DevTools (F12)
3. Go to Application → Cookies
4. Look for `access_token` cookie
5. Verify it has a value

### 2. Verify Cookie is Sent
1. Open DevTools (F12)
2. Go to Network tab
3. Create a post in dashboard
4. Look at the POST request to `/posts`
5. Check Request Headers for `Cookie: access_token=...`

### 3. Verify User Stays Logged In
1. Login
2. Refresh page (F5)
3. You should still be logged in
4. Check DevTools → Cookies for `access_token`

## Important Notes

### For Local Development
- Use `localhost` for both frontend and backend
- Use `samesite="lax"` for cookies
- Use `secure=False` for http

### For Production
- Use HTTPS (https://)
- Use `samesite="strict"` for cookies
- Use `secure=True` for cookies
- Use your actual domain name

### Why Not Use 127.0.0.1?
While `127.0.0.1` works for direct access, it causes issues with cookies because:
1. Browsers treat `localhost` and `127.0.0.1` as different domains
2. Cross-origin cookie restrictions apply
3. `samesite="none"` requires `secure=True` (HTTPS)
4. Local development uses `http://` not `https://`

### Why Not Use samesite="none"?
`samesite="none"` is designed for third-party cookies (e.g., tracking pixels). For local development:
1. It requires `secure=True` (HTTPS only)
2. It's more complex to set up
3. `samesite="lax"` works fine for same-origin requests
4. `samesite="lax"` is more secure

## Cookie Settings Reference

### Local Development (http://)
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=False,
    samesite="lax",
    max_age=3600,
    path="/",
)
```

### Production (https://)
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,
    samesite="strict",
    max_age=3600,
    path="/",
    domain=".yourdomain.com",  # Include subdomains
)
```

## Troubleshooting

### Cookie Still Not Stored?
1. Check that frontend is using `localhost` not `127.0.0.1`
2. Check that backend is running on `localhost` not `127.0.0.1`
3. Clear browser cookies and try again
4. Check browser console for errors
5. Check backend logs for cookie setting messages

### Getting 401 After Login?
1. Verify cookie is stored (DevTools → Cookies)
2. Verify cookie is being sent (DevTools → Network → Request Headers)
3. Check that `/auth/me` endpoint is being called
4. Verify backend is validating cookie correctly

### Cookie Deleted After Logout?
This is expected behavior. The logout endpoint deletes the cookie:
```python
response.delete_cookie("access_token", path="/", samesite="lax")
```

## Summary

✅ Changed frontend API calls from `127.0.0.1` to `localhost`
✅ Updated cookie settings to use `samesite="lax"`
✅ Ensured CORS properly exposes Set-Cookie header
✅ Cookies now properly stored on user device
✅ User stays logged in after page refresh
✅ All API requests include the cookie automatically
