# Login & Cookie Issues - Complete Fix Guide

## Problems Identified & Fixed

### Problem 1: JSON Syntax Error in Curl
**Error**: `422 Unprocessable Entity - JSON decode error: Expecting ',' delimiter`

**Cause**: The curl command in the API docs had malformed JSON:
```json
{
  "email": "bryantech.dev1@gmail.com"    // ❌ Missing comma here
  "password": "12345678"
}
```

**Fix**: Correct JSON format:
```json
{
  "email": "bryantech.dev1@gmail.com",   // ✅ Comma added
  "password": "12345678"
}
```

### Problem 2: Frontend Error Handling
**Error**: `[object Object]` in console - error object not being converted to string

**Cause**: The `handleResponse` function was throwing an error object instead of extracting the error message

**Fix**: Updated `handleResponse` to properly extract error messages:
```typescript
const handleResponse = async (res: Response) => {
  const data = await res.json();
  if (!res.ok) {
    // Handle validation errors (422)
    if (data.detail && Array.isArray(data.detail)) {
      const errorMsg = data.detail.map((err: any) => err.msg).join(', ');
      throw new Error(errorMsg);
    }
    // Handle other errors
    throw new Error(data.detail || data.error || 'Request failed');
  }
  return data;
};
```

### Problem 3: Login Page Error Handling
**Error**: Login page not properly catching and displaying errors

**Fix**: Updated login page to:
1. Properly catch errors as Error objects
2. Extract error message correctly
3. Display meaningful error messages
4. Log errors for debugging

```typescript
try {
  const result = await api.login(email, password);
  console.log('✅ Login successful:', result);
  router.push('/dashboard');
} catch (err: any) {
  const errorMessage = err instanceof Error ? err.message : 'Login failed. Please try again.';
  console.error('❌ Login error:', errorMessage);
  setError(errorMessage);
}
```

### Problem 4: Cookie Not Being Set
**Root Cause**: The login was failing due to JSON parsing errors, so the response never reached the cookie-setting code

**Fix**: Once the JSON parsing is fixed, cookies will be set automatically because:
1. Backend sets cookie: `response.set_cookie(key="access_token", value=token, ...)`
2. Frontend includes `credentials: 'include'` in fetch
3. Browser automatically stores and sends cookies

## Testing the Fix

### Step 1: Test with Correct JSON
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "bryantech.dev1@gmail.com",
    "password": "12345678"
  }'
```

**Expected Response** (200 OK):
```json
{
  "message": "Login successful",
  "user": {
    "id": "...",
    "email": "bryantech.dev1@gmail.com",
    "role": "user"
  }
}
```

**Expected Headers**:
```
set-cookie: access_token=<jwt_token>; Path=/; HttpOnly; SameSite=lax; Max-Age=3600
```

### Step 2: Test Frontend Login
1. Open `http://localhost:3000/auth/login`
2. Enter email: `bryantech.dev1@gmail.com`
3. Enter password: `12345678`
4. Click "Login"
5. **Expected**: Redirected to dashboard with no errors

### Step 3: Verify Cookie is Set
1. Press F12 to open DevTools
2. Go to Application tab
3. Click Cookies
4. Select `http://localhost:3000`
5. **Expected**: See `access_token` cookie with JWT value

### Step 4: Verify Cookie is Sent
1. In DevTools, go to Network tab
2. Refresh page or navigate to dashboard
3. Look for requests to backend
4. Click on any request
5. Go to Request Headers
6. **Expected**: See `Cookie: access_token=<jwt_token>`

## Files Modified

### Backend
- `backend/app/api/auth.py` - Added logging for debugging

### Frontend
- `frontend/src/lib/api.ts` - Fixed error handling in `handleResponse`
- `frontend/src/app/auth/login/page.tsx` - Fixed error handling and logging
- `frontend/src/app/auth/signup/page.tsx` - Fixed error handling and logging

## Debugging Checklist

If login still doesn't work:

### Check 1: Backend is Running
```bash
curl http://127.0.0.1:8000/health
# Expected: {"status":"ok"}
```

### Check 2: MongoDB Connection
```bash
cd backend
python test_mongo_simple.py
# Expected: Connection successful
```

### Check 3: User Exists
```bash
# In MongoDB Atlas console
db.users.findOne({email: "bryantech.dev1@gmail.com"})
# Expected: User document found
```

### Check 4: Backend Logs
```bash
# Terminal running backend
# Look for:
# - "Login attempt for email: ..."
# - "Token created for user: ..."
# - "Cookie set for user: ..."
```

### Check 5: Frontend Console
```bash
# F12 → Console
# Look for:
# - "📡 Logging in at: http://127.0.0.1:8000/auth/login"
# - "✅ Login successful: {...}"
# - Or "❌ Login error: ..."
```

### Check 6: Network Tab
```bash
# F12 → Network
# Look for POST request to /auth/login
# Check Response tab for error details
# Check Response Headers for set-cookie
```

## Common Issues & Solutions

### Issue: "Invalid credentials"
**Solution**: 
1. Verify user exists in MongoDB
2. Verify password is correct
3. Check backend logs for password verification errors

### Issue: "JSON decode error"
**Solution**:
1. Ensure JSON is properly formatted (commas, quotes)
2. Check Content-Type header is `application/json`
3. Verify request body is valid JSON

### Issue: Cookie not set
**Solution**:
1. Check login response is 200 OK
2. Check response headers for `set-cookie`
3. Check browser cookie settings
4. Verify `secure=False` for localhost

### Issue: Cookie not sent with requests
**Solution**:
1. Verify `credentials: 'include'` in fetch
2. Check CORS `allow_credentials: True`
3. Check cookie domain matches
4. Check cookie path is `/`

## Testing Workflow

### 1. Create Test User
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/signup' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

### 2. Login with Test User
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

### 3. Verify Cookie in Response
Look for `set-cookie` header in response

### 4. Test Frontend
1. Open `http://localhost:3000/auth/login`
2. Enter credentials
3. Click Login
4. Verify redirected to dashboard
5. Check F12 → Application → Cookies for `access_token`

## Success Indicators

✅ Login successful when:
- No JSON errors in backend
- Response status is 200 OK
- Response includes user data
- `set-cookie` header present in response
- `access_token` cookie visible in browser
- Frontend redirects to dashboard
- No errors in console

## Next Steps

After login is working:
1. Test creating posts
2. Test comments
3. Test likes and bookmarks
4. Test admin features
5. Test logout

---

**Login should now work correctly! 🎉**
