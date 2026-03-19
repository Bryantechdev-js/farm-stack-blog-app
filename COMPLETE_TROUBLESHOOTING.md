# Complete Troubleshooting Guide

## Issue 1: Dashboard Stuck Loading

### Symptoms
- Dashboard page never finishes loading
- Spinner keeps spinning forever
- No error messages

### Root Causes
1. `/auth/me` endpoint returning 401 (not authenticated)
2. `fetchPosts` being called before user is set
3. Backend not responding
4. Network request failing

### Solutions

**Solution 1: Check Authentication**
1. Open DevTools (F12)
2. Go to Network tab
3. Refresh dashboard
4. Look for GET request to `/auth/me`
5. Check response:
   - If 401: Cookie not being sent or invalid
   - If 200: User is authenticated

**Solution 2: Check Cookie**
1. Open DevTools (F12)
2. Go to Application → Cookies
3. Look for `access_token` cookie
4. If missing: Login again
5. If present: Check it's being sent with requests

**Solution 3: Check Backend**
1. Verify backend is running: `http://localhost:8000/health`
2. Check backend logs for errors
3. Restart backend if needed

**Solution 4: Check Network**
1. Open DevTools Network tab
2. Refresh dashboard
3. Look for failed requests (red)
4. Check response status codes
5. Check for CORS errors

**Solution 5: Clear Cache**
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear cookies: DevTools → Application → Cookies → Delete all
3. Clear cache: DevTools → Application → Cache Storage → Delete all
4. Try again

---

## Issue 2: Login Access Token Not Stored in Cookies

### Symptoms
- Login successful message appears
- But cookie is not in DevTools
- `/auth/me` returns 401
- Cannot access protected pages

### Root Causes
1. Frontend and backend on different domains (localhost vs 127.0.0.1)
2. CORS not allowing credentials
3. Backend not setting cookie
4. Browser blocking cookies

### Solutions

**Solution 1: Verify Domain Consistency**

Check backend is on `localhost`:
```bash
# CORRECT
uvicorn app.main:app --reload --host localhost --port 8000

# WRONG
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Check frontend is on `localhost:3000`:
```bash
# Frontend should be on localhost:3000
# Check in browser: http://localhost:3000
# NOT http://127.0.0.1:3000
```

**Solution 2: Check CORS Configuration**

In `backend/app/main.py`, verify:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend origin
        "http://127.0.0.1:3000",  # Alternative
    ],
    allow_credentials=True,  # MUST be True
    expose_headers=["*", "Set-Cookie"],  # MUST include Set-Cookie
)
```

**Solution 3: Check Backend Logs**

When you login, backend should print:
```
Login attempt for email: user@example.com
Token created for user: user@example.com
Cookie set for user: user@example.com
Set-Cookie header: access_token=eyJ...
```

If you don't see these:
- Backend didn't receive login request
- Check frontend is calling correct URL
- Check network tab for errors

**Solution 4: Check Network Response**

1. Open DevTools Network tab
2. Login
3. Find POST request to `/auth/login`
4. Click on it
5. Go to Response Headers
6. Look for: `Set-Cookie: access_token=...`

If `Set-Cookie` is missing:
- Backend is not setting cookie
- Check backend code
- Check CORS configuration
- Restart backend

**Solution 5: Check Browser Settings**

1. Make sure cookies are enabled
2. Check if third-party cookies are blocked
3. Try incognito/private window
4. Try different browser

**Solution 6: Verify Cookie Settings**

In `backend/app/api/auth.py`:
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=False,  # False for local http
    samesite="lax",  # Works with localhost
    max_age=3600,
    path="/",
)
```

These settings should work. If not:
- Check backend is executing this code
- Check no exceptions are raised
- Check response is returned

---

## Issue 3: CRUD Operations Not Working

### Symptoms
- Can't create posts
- Can't edit posts
- Can't delete posts
- Can't add comments
- Can't like/bookmark

### Root Causes
1. Not authenticated (401 error)
2. Backend endpoint not working
3. Network request failing
4. Form validation failing

### Solutions

**Solution 1: Verify Authentication**
1. Check you're logged in
2. Check cookie exists in DevTools
3. Check `/auth/me` returns 200
4. If 401: Login again

**Solution 2: Check Network Requests**
1. Open DevTools Network tab
2. Perform action (create post, etc.)
3. Look for the request
4. Check response status:
   - 200: Success
   - 401: Not authenticated
   - 400: Bad request
   - 500: Server error

**Solution 3: Check Form Validation**
1. Make sure all required fields are filled
2. Check field values are correct
3. Check image is selected (for posts)
4. Check no validation errors in console

**Solution 4: Check Backend Logs**
1. Look for error messages
2. Check database connection
3. Check file upload directory exists
4. Restart backend if needed

**Solution 5: Check Response Data**
1. In Network tab, click on request
2. Go to Response tab
3. Check response includes expected data
4. Check for error messages

---

## Quick Diagnostic Checklist

### Backend
- [ ] Running on `localhost:8000`
- [ ] MongoDB connected
- [ ] No errors in logs
- [ ] `/health` endpoint returns 200
- [ ] CORS configured correctly
- [ ] Cookie settings correct

### Frontend
- [ ] Running on `localhost:3000`
- [ ] No errors in console
- [ ] API_BASE is `http://localhost:8000`
- [ ] All fetch calls include `credentials: 'include'`
- [ ] Build successful

### Network
- [ ] Login request returns 200
- [ ] Response includes `Set-Cookie` header
- [ ] `/auth/me` request includes `Cookie` header
- [ ] `/auth/me` returns 200
- [ ] CRUD requests return 200

### Browser
- [ ] Cookies enabled
- [ ] No third-party cookie blocking
- [ ] Cookie appears in DevTools
- [ ] No CORS errors in console

---

## Step-by-Step Fix Process

### Step 1: Restart Everything
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --host localhost --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Step 2: Clear Browser Data
1. Open DevTools (F12)
2. Application → Cookies → Delete all
3. Application → Cache Storage → Delete all
4. Hard refresh: Ctrl+Shift+R

### Step 3: Test Login
1. Go to `http://localhost:3000/auth/login`
2. Enter credentials
3. Check DevTools Network tab
4. Verify `Set-Cookie` header in response
5. Check cookie appears in DevTools

### Step 4: Test Dashboard
1. Go to `http://localhost:3000/dashboard`
2. Check page loads (not stuck)
3. Check posts appear
4. Check no 401 errors

### Step 5: Test CRUD
1. Create a post
2. Edit the post
3. Delete the post
4. Check all operations work

### Step 6: Check Logs
1. Backend console for errors
2. Browser console for errors
3. Network tab for failed requests

---

## Common Error Messages & Solutions

### "Module not found: Can't resolve '@vercel/turbopack-next/internal/font/google/font'"
**Solution**: Already fixed - Google Fonts import removed

### "Failed to load resource: the server responded with a status of 401"
**Solution**: 
- Check cookie exists
- Check `/auth/me` endpoint
- Login again

### "Access to fetch blocked by CORS policy"
**Solution**:
- Check CORS configuration
- Check `allow_credentials=True`
- Check frontend origin in `allow_origins`

### "Cannot POST /posts"
**Solution**:
- Check you're authenticated
- Check backend is running
- Check endpoint exists

### "Dashboard stuck loading"
**Solution**:
- Check `/auth/me` returns 200
- Check `fetchPosts` is called after user is set
- Check backend is responding

---

## Testing Commands

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -v
```

### Test /auth/me
```bash
curl http://localhost:8000/auth/me \
  -H "Cookie: access_token=YOUR_TOKEN_HERE" \
  -v
```

### Test Get Posts
```bash
curl http://localhost:8000/posts \
  -v
```

---

## When All Else Fails

1. **Restart everything**:
   - Stop backend
   - Stop frontend
   - Clear browser cache
   - Start backend
   - Start frontend

2. **Check logs**:
   - Backend console
   - Browser console
   - Network tab

3. **Verify configuration**:
   - Backend on `localhost:8000`
   - Frontend on `localhost:3000`
   - CORS configured
   - MongoDB connected

4. **Try fresh start**:
   - Delete node_modules
   - Delete .next folder
   - npm install
   - npm run build
   - npm run dev

5. **Check database**:
   - MongoDB is running
   - Database exists
   - Collections exist
   - Data is being saved

6. **Ask for help**:
   - Share backend logs
   - Share browser console errors
   - Share Network tab screenshots
   - Share CORS configuration

---

## Success Indicators

✅ All working correctly when:
- Login successful, cookie stored
- Dashboard loads without errors
- Can create posts
- Can edit posts
- Can delete posts
- Can add comments
- Can like/bookmark
- All operations show toast notifications
- No 401 errors
- No CORS errors
- No console errors
