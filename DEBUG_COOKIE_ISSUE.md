# Debug Cookie Storage Issue

## Step-by-Step Debugging

### Step 1: Verify Backend is Running on localhost

**Important**: Backend MUST be on `localhost` not `127.0.0.1`

```bash
cd backend
uvicorn app.main:app --reload --host localhost --port 8000
```

Check the output shows:
```
Uvicorn running on http://localhost:8000
```

### Step 2: Verify Frontend is Running on localhost

```bash
cd frontend
npm run dev
```

Check the output shows:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### Step 3: Test Login with Browser DevTools

1. Open http://localhost:3000/auth/login
2. Open DevTools (F12)
3. Go to Network tab
4. Enter credentials and click "Sign In"
5. Look for the POST request to `/auth/login`
6. Click on it and check:
   - **Request Headers**: Should include `Content-Type: application/json`
   - **Response Headers**: Should include `Set-Cookie: access_token=...`
   - **Response Status**: Should be 200

### Step 4: Check if Cookie is Set

1. Open DevTools (F12)
2. Go to Application tab
3. Click Cookies
4. Select `http://localhost:3000`
5. Look for `access_token` cookie

**If cookie is NOT there**:
- Check Response Headers in Network tab for `Set-Cookie`
- If `Set-Cookie` is missing, backend is not setting it
- If `Set-Cookie` is there but cookie not stored, it's a browser/CORS issue

### Step 5: Check Backend Logs

When you login, backend should print:
```
Login attempt for email: user@example.com
Token created for user: user@example.com
Cookie set for user: user@example.com
Set-Cookie header: access_token=eyJ...
```

If you don't see these messages:
- Backend didn't receive the login request
- Check frontend is calling correct URL
- Check network tab for errors

### Step 6: Test /auth/me Endpoint

1. After login, open DevTools Network tab
2. Go to http://localhost:3000/dashboard
3. Look for GET request to `/auth/me`
4. Check:
   - **Request Headers**: Should include `Cookie: access_token=...`
   - **Response Status**: Should be 200 (not 401)

**If you see 401**:
- Cookie is not being sent
- Check `credentials: 'include'` in fetch call
- Check CORS configuration

## Common Issues & Solutions

### Issue 1: Cookie Not Set (No Set-Cookie Header)

**Symptoms**:
- Response doesn't include `Set-Cookie` header
- Backend logs don't show "Cookie set"

**Solutions**:
1. Check backend is running on `localhost` not `127.0.0.1`
2. Check CORS `allow_credentials=True`
3. Check CORS `expose_headers` includes `Set-Cookie`
4. Restart backend

### Issue 2: Cookie Set But Not Stored

**Symptoms**:
- Response includes `Set-Cookie` header
- But cookie doesn't appear in DevTools

**Solutions**:
1. Check frontend is on `localhost:3000` not `127.0.0.1:3000`
2. Check `samesite="lax"` in backend
3. Check `secure=False` for local development
4. Clear all cookies and try again
5. Try incognito/private window

### Issue 3: Cookie Set But Not Sent with Requests

**Symptoms**:
- Cookie appears in DevTools
- But requests don't include `Cookie` header

**Solutions**:
1. Check `credentials: 'include'` in all fetch calls
2. Check CORS `allow_credentials=True`
3. Check frontend is on same domain as cookie
4. Restart frontend

### Issue 4: Dashboard Stuck Loading

**Symptoms**:
- Dashboard page never finishes loading
- Spinner keeps spinning

**Solutions**:
1. Check browser console for errors
2. Check Network tab for failed requests
3. Check `/auth/me` endpoint returns 200
4. Check `fetchPosts` is called after user is set
5. Check backend is responding

## Manual Testing

### Test 1: Direct API Call

Open browser console and run:
```javascript
// Test login
fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'test@example.com', password: 'password123' }),
  credentials: 'include'
})
.then(r => r.json())
.then(d => console.log(d))
```

Check:
- Response includes user data
- Response status is 200
- Set-Cookie header is in response

### Test 2: Check Cookie After Login

```javascript
// Check if cookie is set
document.cookie
```

Should show:
```
access_token=eyJ...
```

### Test 3: Test /auth/me with Cookie

```javascript
// Test /auth/me endpoint
fetch('http://localhost:8000/auth/me', {
  credentials: 'include'
})
.then(r => r.json())
.then(d => console.log(d))
```

Should return user data (not 401 error)

## Network Tab Analysis

### Successful Login Request

**Request**:
```
POST /auth/login HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Origin: http://localhost:3000

{"email":"test@example.com","password":"password123"}
```

**Response**:
```
HTTP/1.1 200 OK
Set-Cookie: access_token=eyJ...; Path=/; HttpOnly; SameSite=Lax
Content-Type: application/json

{"message":"Login successful","user":{...}}
```

### Successful /auth/me Request

**Request**:
```
GET /auth/me HTTP/1.1
Host: localhost:8000
Origin: http://localhost:3000
Cookie: access_token=eyJ...
```

**Response**:
```
HTTP/1.1 200 OK
Content-Type: application/json

{"id":"...","email":"test@example.com","role":"user"}
```

## Checklist

- [ ] Backend running on `localhost:8000`
- [ ] Frontend running on `localhost:3000`
- [ ] Login request returns 200
- [ ] Response includes `Set-Cookie` header
- [ ] Cookie appears in DevTools
- [ ] `/auth/me` request includes `Cookie` header
- [ ] `/auth/me` returns 200 (not 401)
- [ ] Dashboard loads without errors
- [ ] Can create post
- [ ] Can edit post
- [ ] Can delete post

## If Still Not Working

1. **Clear everything**:
   - Clear browser cookies
   - Clear browser cache
   - Restart backend
   - Restart frontend

2. **Check logs**:
   - Backend console for errors
   - Browser console for errors
   - Network tab for failed requests

3. **Verify configuration**:
   - CORS allows `http://localhost:3000`
   - Cookie settings are correct
   - Frontend uses `localhost` not `127.0.0.1`

4. **Try incognito window**:
   - Open new incognito/private window
   - Try login again
   - Check if cookie is set

5. **Check browser settings**:
   - Make sure cookies are enabled
   - Check if third-party cookies are blocked
   - Try different browser

## Backend Cookie Settings

Current settings in `backend/app/api/auth.py`:
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=False,  # OK for local http
    samesite="lax",  # Works with localhost
    max_age=3600,
    path="/",
)
```

These settings should work for local development. If not working:
1. Check backend is actually executing this code
2. Check no exceptions are being raised
3. Check response is being returned correctly

## Production Settings

For production (HTTPS):
```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,  # HTTPS only
    samesite="strict",  # Stricter security
    max_age=3600,
    path="/",
    domain=".yourdomain.com",  # Include subdomains
)
```

## Summary

To fix cookie issues:
1. Ensure backend is on `localhost` (not `127.0.0.1`)
2. Ensure frontend is on `localhost:3000` (not `127.0.0.1:3000`)
3. Check CORS configuration
4. Check `credentials: 'include'` in fetch calls
5. Check backend logs for errors
6. Check Network tab for Set-Cookie header
7. Check DevTools Cookies for access_token
8. Clear cookies and try again
