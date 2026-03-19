# ❌ "Failed to fetch" Error - DIAGNOSTIC & FIX

## The Error

```
Failed to fetch
at Object.getPosts (src/lib/api.ts:27:23)
at fetchPosts (src/app/dashboard/page.tsx:26:30)
```

**Meaning:** Frontend cannot reach the backend API.

---

## Root Causes (Check These)

### 1. Backend Not Running

**Check:** Is the backend running?

```bash
# Terminal 1 - Check if backend is running
curl http://127.0.0.1:8000/docs
```

**Expected:** Should show Swagger UI documentation

**If not:** Start the backend:
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Wrong API URL

**Check:** Is `frontend/.env.local` correct?

```bash
cat frontend/.env.local
```

**Should show:**
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

**If wrong:** Update it:
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 3. Frontend Not Restarted

**Check:** Did you restart the frontend after changing `.env.local`?

**If not:** Restart it:
```bash
cd frontend
npm run dev
```

### 4. Port Already in Use

**Check:** Is port 8000 already in use?

```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

**If in use:** Kill the process or use a different port:
```bash
# Use port 8001 instead
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Then update `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8001
```

### 5. CORS Issue

**Check:** Browser console for CORS errors

**If you see:** `Access to XMLHttpRequest blocked by CORS policy`

**Fix:** Backend CORS is misconfigured. Check `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://frontend:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Diagnostic Steps

### Step 1: Check Backend is Running

```bash
curl http://127.0.0.1:8000/docs
```

**Expected:** HTML page with Swagger UI

**If error:** Backend is not running. Start it:
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 2: Check API URL in Frontend

```bash
cat frontend/.env.local
```

**Should show:**
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### Step 3: Check Browser Console

1. Open `http://localhost:3000`
2. Press F12 (Developer Tools)
3. Go to Console tab
4. Look for error messages

**You should see:**
```
🔗 API Base URL: http://127.0.0.1:8000
📡 Fetching posts from: http://127.0.0.1:8000/posts
```

**If you see CORS error:** Backend CORS is wrong

### Step 4: Test API Directly

```bash
curl http://127.0.0.1:8000/posts
```

**Expected:** JSON array of posts (or empty array)

**If error:** Backend has an issue

### Step 5: Restart Everything

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## Quick Checklist

- [ ] Backend is running at `http://127.0.0.1:8000`
- [ ] `frontend/.env.local` has correct API URL
- [ ] Frontend is restarted after changing `.env.local`
- [ ] Port 8000 is not in use by another process
- [ ] No CORS errors in browser console
- [ ] Can access `http://127.0.0.1:8000/docs`
- [ ] Can access `http://localhost:3000`

---

## Common Scenarios

### Scenario 1: Backend Not Running

**Error:** `Failed to fetch`

**Fix:**
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Scenario 2: Wrong API URL

**Error:** `Failed to fetch`

**Fix:**
```bash
# Update frontend/.env.local
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Restart frontend
cd frontend
npm run dev
```

### Scenario 3: Port Already in Use

**Error:** `Failed to fetch` or backend won't start

**Fix:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

### Scenario 4: CORS Error

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Fix:** Check `backend/app/main.py` has correct CORS configuration

### Scenario 5: Frontend Not Restarted

**Error:** `Failed to fetch` after changing `.env.local`

**Fix:**
```bash
# Stop frontend (Ctrl+C)
# Restart frontend
cd frontend
npm run dev
```

---

## Debugging with Console Logs

The API client now logs all requests. Check browser console (F12):

```
🔗 API Base URL: http://127.0.0.1:8000
📡 Fetching posts from: http://127.0.0.1:8000/posts
❌ Failed to fetch posts: TypeError: Failed to fetch
```

This tells you:
- What URL it's trying to reach
- What error occurred

---

## Still Not Working?

1. **Check backend logs** - Look at terminal where backend is running
2. **Check browser console** - Press F12, go to Console tab
3. **Check Network tab** - See what requests are being made
4. **Test API directly** - Use curl to test backend
5. **Restart everything** - Kill and restart both backend and frontend

---

## Files Updated

- `frontend/src/lib/api.ts` - Added logging and error handling

---

**Status: Added diagnostic logging to help identify the issue**

Check browser console (F12) to see what URL the frontend is trying to reach and what error it's getting.
