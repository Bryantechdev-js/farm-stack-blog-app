# Verify Admin Setup - Complete Checklist

## Step-by-Step Verification

### Step 1: Verify Backend is Running

```bash
# Check if backend is running
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status":"ok"}
```

**If not working:**
- Start backend: `python -m uvicorn app.main:app --reload`
- Make sure you're in the `backend` directory

---

### Step 2: Verify Frontend is Running

```bash
# Check if frontend is running
curl http://localhost:3000
```

**If not working:**
- Start frontend: `npm run dev` (in frontend directory)
- Make sure you're in the `frontend` directory

---

### Step 3: Verify User Exists in Database

**Option A: Using MongoDB Compass**
1. Open MongoDB Compass
2. Connect to your MongoDB instance
3. Navigate to: `blog_db` → `users`
4. Look for user with email containing "bryantech"
5. Check if the user exists

**Option B: Using MongoDB CLI**
```bash
mongosh
use blog_db
db.users.find({ email: /bryantech/ })
```

**Expected Output:**
```json
{
  "_id": ObjectId("..."),
  "email": "bryantech.dev@gmail.com",
  "password": "hashed_password",
  "role": "admin",
  "full_name": null,
  "bio": null,
  "avatar_url": null,
  "created_at": ISODate("...")
}
```

---

### Step 4: Verify User Has Admin Role

**Check the role field:**
- Should be: `"role": "admin"`
- NOT: `"role": "user"`

**If role is "user", update it:**

**Option A: Using MongoDB Compass**
1. Find the user
2. Click Edit
3. Change `"role": "user"` to `"role": "admin"`
4. Click Update

**Option B: Using MongoDB CLI**
```bash
mongosh
use blog_db
db.users.updateOne(
  { email: "bryantech.dev@gmail.com" },
  { $set: { role: "admin" } }
)
```

**Option C: Using Python Script**
```bash
python backend/set_admin.py bryantech.dev@gmail.com
```

---

### Step 5: Test Login Redirect

1. Go to `http://localhost:3000/auth/login`
2. Enter email: `bryantech.dev@gmail.com`
3. Enter password: (your password)
4. Click "Sign In"

**Expected Behavior:**
- See message: "✅ Welcome Admin! Redirecting to dashboard..."
- Automatically redirected to `http://localhost:3000/admin/dashboard`
- See admin dashboard with charts

**If not working:**
- Check browser console (F12 → Console)
- Look for error messages
- Check if redirect is happening
- Verify user role in database

---

### Step 6: Verify Admin Dashboard Loads

1. Go to `http://localhost:3000/admin/dashboard`
2. You should see:
   - Navigation bar with "📊 Admin Dashboard"
   - Key metrics cards (Users, Posts, Comments, Engagement)
   - Charts section
   - Quick links

**If you see "Access Denied":**
- User is not admin
- Run: `python backend/set_admin.py bryantech.dev@gmail.com`
- Restart backend
- Login again

**If charts are not displaying:**
- Install recharts: `npm install recharts`
- Restart frontend
- Clear browser cache

---

### Step 7: Verify Admin Settings Page

1. Go to `http://localhost:3000/admin/settings`
2. You should see:
   - Profile section with form fields
   - Security section with password change
   - Email field (read-only)
   - Role field (read-only)

**If you see "Access Denied":**
- User is not admin
- Follow Step 4 to set admin role

---

### Step 8: Test Regular User Redirect

1. Create a new user account (different email)
2. Login with that account
3. You should see: "✅ Login successful! Redirecting..."
4. Should be redirected to `http://localhost:3000/dashboard` (home page)
5. Should NOT see admin dashboard

**If regular user can access admin dashboard:**
- Check user role in database
- Make sure it's "user" not "admin"

---

## Complete Verification Checklist

### Backend
- [ ] Backend running on `http://localhost:8000`
- [ ] Health check returns `{"status":"ok"}`
- [ ] MongoDB connected
- [ ] User exists in database
- [ ] User has role: "admin"

### Frontend
- [ ] Frontend running on `http://localhost:3000`
- [ ] Recharts installed: `npm install recharts`
- [ ] Login page loads
- [ ] Admin dashboard page exists

### Login Flow
- [ ] Admin user login shows redirect message
- [ ] Admin user redirected to `/admin/dashboard`
- [ ] Regular user login shows different message
- [ ] Regular user redirected to `/dashboard`

### Admin Dashboard
- [ ] Dashboard loads without errors
- [ ] Key metrics display
- [ ] Charts display (if recharts installed)
- [ ] Quick links work
- [ ] Settings page accessible

### Admin Settings
- [ ] Profile form displays
- [ ] Can update profile
- [ ] Can change password
- [ ] Avatar preview works

---

## Troubleshooting Commands

### If user doesn't exist, create one:
```bash
# Sign up at http://localhost:3000/auth/signup
# Use email: bryantech.dev@gmail.com
# First user automatically becomes admin
```

### If user exists but is not admin:
```bash
python backend/set_admin.py bryantech.dev@gmail.com
```

### If charts not displaying:
```bash
cd frontend
npm install recharts
npm run dev
```

### If backend not responding:
```bash
# Stop current backend (Ctrl+C)
python -m uvicorn app.main:app --reload
```

### If frontend not responding:
```bash
# Stop current frontend (Ctrl+C)
cd frontend
npm run dev
```

### Clear browser cache:
- Press Ctrl+Shift+Delete
- Select "All time"
- Check "Cookies and other site data"
- Check "Cached images and files"
- Click "Clear data"

---

## Expected Results

### Admin Login
```
Email: bryantech.dev@gmail.com
Password: (your password)
↓
"✅ Welcome Admin! Redirecting to dashboard..."
↓
Redirected to: /admin/dashboard
↓
See modern dashboard with charts
```

### Regular User Login
```
Email: other@email.com
Password: (their password)
↓
"✅ Login successful! Redirecting..."
↓
Redirected to: /dashboard
↓
See home page
```

---

## Summary

✅ Follow all steps above
✅ Verify each step works
✅ Admin redirect will work
✅ Admin dashboard will display
✅ Everything will be functional

**If any step fails, check the troubleshooting section!**
