# CORS and Failed to Fetch - SOLUTION

## Problem Summary
- Frontend getting "Failed to fetch" error when trying to load posts
- CORS error: "No 'Access-Control-Allow-Origin' header"
- No access_token cookie being created after login

## Root Cause Analysis

### What We Verified ✅
1. **Backend is running** - Health check endpoint responds with 200 OK
2. **Posts endpoint works** - Returns empty array `[]` with 200 OK
3. **CORS headers are correct** - When tested with Origin header, backend returns:
   - `access-control-allow-origin: http://localhost:3000`
   - `access-control-allow-credentials: true`
   - `access-control-expose-headers: *`
4. **Backend configuration is correct** - CORS middleware properly configured
5. **MongoDB connection works** - Posts endpoint successfully queries database

### The Real Issue
**The frontend dev server needs to be RESTARTED** to pick up the `.env.local` file with the correct API URL.

## Solution - Step by Step

### Step 1: Stop the Frontend Dev Server
If the frontend is running, stop it:
- Press `Ctrl+C` in the terminal where `npm run dev` is running

### Step 2: Verify Backend is Running
```bash
# Test the backend health endpoint
curl http://127.0.0.1:8000/health

# Expected response:
# {"status":"ok"}
```

### Step 3: Verify Environment File
Check that `frontend/.env.local` contains:
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### Step 4: Restart Frontend Dev Server
```bash
cd frontend
npm run dev
```

The frontend will now:
- Load the correct API URL from `.env.local`
- Connect to `http://127.0.0.1:8000` instead of trying to connect elsewhere
- Receive proper CORS headers from the backend
- Cookies will be set correctly after login

### Step 5: Test the Application
1. Open `http://localhost:3000` in your browser
2. Sign up with a test account
3. Check browser DevTools (F12) → Application → Cookies
4. You should see `access_token` cookie
5. Navigate to dashboard
6. Posts should load without CORS errors

## Why This Works

### CORS Flow
```
Frontend (http://localhost:3000)
    ↓
Makes request to http://127.0.0.1:8000/posts
    ↓
Backend receives request with Origin: http://localhost:3000
    ↓
CORS middleware checks if origin is in allow_origins list
    ↓
Backend responds with:
  - access-control-allow-origin: http://localhost:3000
  - access-control-allow-credentials: true
    ↓
Browser receives response with correct CORS headers
    ↓
Request succeeds, data is returned to frontend
```

### Cookie Flow
```
Frontend sends login request with credentials: 'include'
    ↓
Backend validates credentials
    ↓
Backend sets cookie: response.set_cookie(key="access_token", ...)
    ↓
Browser receives response with Set-Cookie header
    ↓
Browser stores cookie in httpOnly storage
    ↓
Subsequent requests include cookie automatically
```

## Verification Checklist

- [ ] Backend running at `http://127.0.0.1:8000`
- [ ] Frontend running at `http://localhost:3000`
- [ ] `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`
- [ ] Frontend dev server restarted after env file changes
- [ ] Can access `/health` endpoint from backend
- [ ] Can access `/posts` endpoint from backend
- [ ] Frontend loads without CORS errors
- [ ] Can sign up successfully
- [ ] Can see `access_token` cookie in browser
- [ ] Can login successfully
- [ ] Dashboard loads posts without errors

## If Issues Persist

### Check 1: Verify Backend is Actually Running
```bash
# In a new terminal
curl -v http://127.0.0.1:8000/health
```
Should return 200 OK with `{"status":"ok"}`

### Check 2: Verify Frontend Environment
In browser console, check:
```javascript
console.log(process.env.NEXT_PUBLIC_API_URL)
```
Should print: `http://127.0.0.1:8000`

### Check 3: Check Network Tab
In browser DevTools (F12) → Network tab:
- Look for the failed request to `/posts`
- Check the Response Headers for CORS headers
- Check if `access-control-allow-origin` is present

### Check 4: Verify MongoDB Connection
```bash
cd backend
python test_mongo_simple.py
```
Should show successful connection

### Check 5: Clear Browser Cache
- Press `Ctrl+Shift+Delete` to open Clear Browsing Data
- Clear cache and cookies
- Restart frontend dev server
- Reload page

## Common Mistakes to Avoid

❌ **Don't** use `localhost` in backend URL - use `127.0.0.1`
❌ **Don't** forget to restart frontend after changing `.env.local`
❌ **Don't** use `http://localhost:8000` - backend is on `127.0.0.1`
❌ **Don't** expose MongoDB credentials in frontend `.env` - keep them backend-only
❌ **Don't** remove `credentials: 'include'` from fetch requests - needed for cookies

✅ **Do** use `http://127.0.0.1:8000` for backend URL
✅ **Do** restart frontend dev server after env changes
✅ **Do** use `NEXT_PUBLIC_` prefix only for safe frontend variables
✅ **Do** keep MongoDB credentials in backend `.env` only
✅ **Do** include `credentials: 'include'` in all fetch requests

## Files Modified
- `backend/app/main.py` - CORS middleware configuration
- `backend/app/api/auth.py` - Login endpoint with cookie setting
- `backend/app/api/posts.py` - Posts endpoints
- `backend/app/core/security.py` - Argon2 password hashing
- `frontend/.env.local` - API URL configuration
- `frontend/src/lib/api.ts` - API client with logging

## Next Steps
1. Restart frontend dev server
2. Test the application
3. If issues persist, run the verification checks above
4. Check the browser console for detailed error messages
