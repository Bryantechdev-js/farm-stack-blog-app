# Cookie Fix Verification Checklist

## Pre-Flight Checks

### Backend Setup
- [ ] Backend is running on `localhost:8000` (NOT `127.0.0.1:8000`)
  ```bash
  uvicorn app.main:app --reload --host localhost --port 8000
  ```
- [ ] Check backend logs show: `Uvicorn running on http://localhost:8000`
- [ ] MongoDB is connected and working
- [ ] No errors in backend console

### Frontend Setup
- [ ] Frontend is running on `localhost:3000`
  ```bash
  npm run dev
  ```
- [ ] Check frontend logs show: `ready - started server on 0.0.0.0:3000`
- [ ] All API calls use `http://localhost:8000` (verify in code)
- [ ] Build is successful with no errors

## Test 1: Cookie is Set on Login

**Steps**:
1. Open `http://localhost:3000/auth/login`
2. Create new account or login with existing credentials
3. Open DevTools (F12)
4. Go to Application tab → Cookies
5. Select `http://localhost:3000`

**Expected Result**:
- [ ] `access_token` cookie appears in the list
- [ ] Cookie has a value (long string starting with `eyJ...`)
- [ ] Cookie has `HttpOnly` flag checked
- [ ] Cookie has `Path: /`
- [ ] Cookie has `Expires` or `Max-Age` set to ~1 hour

**If Failed**:
- [ ] Check backend logs for "Cookie set for user" message
- [ ] Check that backend is on `localhost` not `127.0.0.1`
- [ ] Check CORS configuration in `backend/app/main.py`
- [ ] Clear all cookies and try again

## Test 2: Cookie is Sent with Requests

**Steps**:
1. Login (from Test 1)
2. Open DevTools (F12)
3. Go to Network tab
4. Click "+ New Post" button in dashboard
5. Fill in post details and submit
6. Look for POST request to `/posts` in Network tab
7. Click on the request
8. Go to Request Headers section

**Expected Result**:
- [ ] Request Headers include: `Cookie: access_token=eyJ...`
- [ ] Response status is 200 (success)
- [ ] Post is created successfully
- [ ] No 401 errors in console

**If Failed**:
- [ ] Check that `credentials: 'include'` is in fetch call
- [ ] Check that cookie exists (Test 1)
- [ ] Check backend logs for token validation
- [ ] Try clearing cookies and logging in again

## Test 3: User Stays Logged In After Refresh

**Steps**:
1. Login (from Test 1)
2. Go to dashboard
3. Press F5 to refresh page
4. Check if you're still logged in

**Expected Result**:
- [ ] Dashboard loads without redirecting to login
- [ ] User email is displayed in navigation
- [ ] No 401 errors in console
- [ ] Cookie still exists in DevTools

**If Failed**:
- [ ] Check that cookie has `Max-Age` set
- [ ] Check that `/auth/me` endpoint returns user data
- [ ] Check backend logs for token validation
- [ ] Verify cookie is being sent with `/auth/me` request

## Test 4: Logout Deletes Cookie

**Steps**:
1. Login (from Test 1)
2. Go to Profile page
3. Click "Logout" button
4. Check DevTools → Cookies

**Expected Result**:
- [ ] `access_token` cookie is removed from list
- [ ] Redirected to home page
- [ ] Cannot access dashboard (redirected to login)
- [ ] No errors in console

**If Failed**:
- [ ] Check backend logs for logout message
- [ ] Check that logout endpoint is being called
- [ ] Try clearing cookies manually

## Test 5: Create Post (Full Integration)

**Steps**:
1. Login
2. Go to Dashboard
3. Click "+ New Post"
4. Fill in:
   - Title: "Test Post"
   - Content: "This is a test"
   - Image: Select any image
5. Click "Publish Post"
6. Check browser console and Network tab

**Expected Result**:
- [ ] Post is created successfully
- [ ] No 401 errors
- [ ] Post appears in dashboard
- [ ] Network request shows 200 status
- [ ] Cookie is sent with request

**If Failed**:
- [ ] Check that cookie exists (Test 1)
- [ ] Check that cookie is sent (Test 2)
- [ ] Check backend logs for errors
- [ ] Check that user is authenticated

## Test 6: All Pages Load Correctly

**Pages to Check**:
- [ ] Home page (`/`) - Shows posts
- [ ] Login page (`/auth/login`) - Can login
- [ ] Signup page (`/auth/signup`) - Can signup
- [ ] Dashboard (`/dashboard`) - Can create posts
- [ ] Profile (`/profile`) - Shows user info
- [ ] Post detail (`/posts/[id]`) - Can comment/like
- [ ] Admin (`/admin`) - Shows analytics (if admin)

**Expected Result**:
- [ ] All pages load without errors
- [ ] No 401 errors
- [ ] User stays logged in across pages
- [ ] All features work

## Browser DevTools Inspection

### Check Cookies
1. Open DevTools (F12)
2. Application → Cookies → http://localhost:3000
3. Look for `access_token`

**Should See**:
```
Name: access_token
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Domain: localhost
Path: /
Expires: [future date]
HttpOnly: ✓
Secure: ✗ (OK for local development)
SameSite: Lax
```

### Check Network Requests
1. Open DevTools (F12)
2. Network tab
3. Perform an action (create post, like, etc.)
4. Click on the request
5. Go to Request Headers

**Should See**:
```
Cookie: access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Check Console
1. Open DevTools (F12)
2. Console tab
3. Perform actions

**Should See**:
- ✅ Login successful messages
- ✅ No 401 errors
- ✅ No CORS errors
- ✅ No cookie-related errors

## Backend Logs to Check

When logging in, backend should show:
```
Login attempt for email: user@example.com
Token created for user: user@example.com
Cookie set for user: user@example.com
Set-Cookie header: access_token=eyJ...
```

When accessing protected endpoints:
```
GET /auth/me
Token validated for user: user@example.com
```

## Common Issues & Solutions

### Issue: Cookie Not Stored
**Solution**:
- [ ] Verify backend is on `localhost` not `127.0.0.1`
- [ ] Verify frontend is on `localhost:3000`
- [ ] Check CORS configuration
- [ ] Clear cookies and try again

### Issue: 401 After Login
**Solution**:
- [ ] Check cookie exists (DevTools)
- [ ] Check cookie is sent (Network tab)
- [ ] Verify backend is validating token
- [ ] Check token expiration

### Issue: User Logged Out After Refresh
**Solution**:
- [ ] Check cookie has `Max-Age` set
- [ ] Check `/auth/me` endpoint works
- [ ] Verify cookie is being sent
- [ ] Check backend token validation

### Issue: CORS Errors
**Solution**:
- [ ] Check `allow_origins` includes `http://localhost:3000`
- [ ] Check `allow_credentials=True`
- [ ] Check `expose_headers` includes `Set-Cookie`
- [ ] Restart backend

## Success Criteria

All tests should pass:
- ✅ Cookie is set on login
- ✅ Cookie is sent with requests
- ✅ User stays logged in after refresh
- ✅ Logout deletes cookie
- ✅ Can create posts
- ✅ All pages load correctly
- ✅ No 401 errors
- ✅ No CORS errors

## Final Verification

Run this checklist one more time:
1. [ ] Backend running on `localhost:8000`
2. [ ] Frontend running on `localhost:3000`
3. [ ] Can login successfully
4. [ ] Cookie appears in DevTools
5. [ ] Can create post without 401 error
6. [ ] User stays logged in after refresh
7. [ ] Can logout successfully
8. [ ] All pages work correctly

If all checks pass, the cookie fix is working correctly! 🎉
