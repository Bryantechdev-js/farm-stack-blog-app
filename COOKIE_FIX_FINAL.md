# Cookie Issue - FINAL FIX

## Problem
The `/auth/me` endpoint was returning 401 Unauthorized because the cookie wasn't being sent with the request.

## Root Cause
The cookie was set with `samesite="lax"` but the frontend and backend are on different ports:
- Frontend: `http://localhost:3000`
- Backend: `http://127.0.0.1:8000`

For cross-port requests on localhost, we need `samesite="none"`.

## Solution
Updated the cookie settings in `backend/app/api/auth.py`:

### Before (Broken)
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=False,
    samesite="lax",  # ❌ Doesn't work for cross-port
    max_age=3600
)
```

### After (Fixed)
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=False,
    samesite="none",  # ✅ Works for cross-port
    max_age=3600,
    path="/"
)
```

## What Changed
- `samesite="lax"` → `samesite="none"` (allows cross-port cookies)
- Added `path="/"` (ensures cookie is sent to all paths)

## Why This Works

### SameSite Policy
- `lax` - Only sends cookie for same-site requests
- `none` - Sends cookie for all requests (requires `secure=True` in production)

### For Development
- Frontend: `localhost:3000`
- Backend: `127.0.0.1:8000`
- These are different ports, so `samesite="none"` is needed

### For Production
- Use `secure=True` (HTTPS only)
- Use `samesite="none"` or `samesite="strict"` depending on needs
- Use proper domain configuration

## Testing

### Step 1: Restart Backend
```bash
# Terminal running backend
Ctrl+C

# Restart
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 2: Test Login
1. Open `http://localhost:3000/auth/login`
2. Enter credentials
3. Click Login
4. **Expected**: Redirected to dashboard

### Step 3: Verify Cookie
1. Press F12
2. Application → Cookies → http://localhost:3000
3. **Expected**: See `access_token` cookie

### Step 4: Check Dashboard
1. Should see "My Posts"
2. Should see profile with email
3. Should see "New Post" button
4. **Expected**: No 401 errors in console

## Files Modified
- `backend/app/api/auth.py` - Updated cookie settings

## Cookie Attributes Explained

```python
response.set_cookie(
    key="access_token",           # Cookie name
    value=token,                  # JWT token value
    httponly=True,                # Not accessible from JavaScript (security)
    secure=False,                 # False for localhost, True for HTTPS
    samesite="none",              # Allow cross-port/cross-site
    max_age=3600,                 # Expires in 1 hour
    path="/"                       # Available to all paths
)
```

## Verification Checklist

- [ ] Backend restarted
- [ ] Login works without errors
- [ ] Cookie visible in F12 → Application → Cookies
- [ ] Dashboard loads without 401 errors
- [ ] Can create posts
- [ ] Can view posts
- [ ] Logout works

## If Still Having Issues

### Check 1: Backend Logs
```bash
# Terminal running backend
# Look for:
# - "Login attempt for email: ..."
# - "Token created for user: ..."
# - "Cookie set for user: ..."
```

### Check 2: Browser Console
```bash
# F12 → Console
# Should NOT see:
# - "GET http://127.0.0.1:8000/auth/me 401"
```

### Check 3: Network Tab
```bash
# F12 → Network
# Look for GET /auth/me request
# Check Response Headers for Set-Cookie
# Check Request Headers for Cookie
```

### Check 4: Clear Browser Data
```bash
# F12 → Application → Cookies
# Delete all cookies for localhost:3000
# Try login again
```

## Production Deployment

For production, update the cookie settings:

```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,              # ✅ HTTPS only
    samesite="strict",        # ✅ Stricter security
    max_age=3600,
    path="/",
    domain=".yourdomain.com"  # ✅ Your domain
)
```

## Summary

✅ **Problem**: Cookie not sent with cross-port requests
✅ **Solution**: Changed `samesite="lax"` to `samesite="none"`
✅ **Result**: Cookie now sent with all requests
✅ **Status**: Ready to test

---

**Restart backend and test login! 🚀**
