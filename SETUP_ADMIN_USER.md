# Setup Admin User - Step by Step

## Problem
Admin redirect is not working because the user doesn't have admin role set in the database.

## Solution

### Step 1: Sign Up with Email "bryantech"

1. Go to `http://localhost:3000/auth/signup`
2. Enter email: `bryantech.dev@gmail.com` (or any email with "bryantech")
3. Enter password: (any password, min 8 chars)
4. Click "Sign Up"
5. You'll see: "🎉 You are the system admin! Redirecting to login..."
6. This means you're the first user and automatically became admin

### Step 2: Login

1. Go to `http://localhost:3000/auth/login`
2. Enter email: `bryantech.dev@gmail.com`
3. Enter password: (the password you set)
4. Click "Sign In"
5. You should see: "✅ Welcome Admin! Redirecting to dashboard..."
6. You'll be automatically redirected to `/admin/dashboard`

### Step 3: Verify Admin Dashboard

1. You should see the modern admin dashboard with:
   - Key metrics (Users, Posts, Comments, Engagement)
   - Charts for post engagement, user trends, post rate
   - Quick links to manage content
2. Click "⚙️ Settings" to access admin settings
3. You can update your profile and change password

---

## If You Already Have Users

If you already have users in the database and need to make one an admin:

### Option 1: Use the Set Admin Script

```bash
python backend/set_admin.py bryantech.dev@gmail.com
```

**Note**: The user must exist in the database first.

### Option 2: Manual Database Update

1. Open MongoDB
2. Find the user with email containing "bryantech"
3. Update their role to "admin":
   ```json
   { "role": "admin" }
   ```

### Option 3: Delete All Users and Start Fresh

1. Delete all users from MongoDB
2. Sign up with `bryantech.dev@gmail.com`
3. You'll automatically become admin

---

## Verify It's Working

### Check 1: Login Redirect
1. Login with admin account
2. Should see: "✅ Welcome Admin! Redirecting to dashboard..."
3. Should be redirected to `/admin/dashboard`

### Check 2: Admin Dashboard Access
1. Go to `http://localhost:3000/admin/dashboard`
2. Should see the modern dashboard with charts
3. Should NOT see "Access Denied" message

### Check 3: Admin Settings
1. Go to `http://localhost:3000/admin/settings`
2. Should see profile management form
3. Should be able to update profile and change password

### Check 4: Regular User Redirect
1. Create another user account
2. Login with that account
3. Should see: "✅ Login successful! Redirecting..."
4. Should be redirected to `/dashboard` (home page)
5. Should NOT see admin dashboard

---

## Troubleshooting

### Issue: Not redirecting to admin dashboard
**Check 1**: Verify user is admin
```bash
python backend/set_admin.py bryantech.dev@gmail.com
```

**Check 2**: Restart backend
```bash
# Stop current backend (Ctrl+C)
python -m uvicorn app.main:app --reload
```

**Check 3**: Clear browser cache
- Press Ctrl+Shift+Delete
- Clear all cache
- Refresh page

**Check 4**: Check browser console
- Press F12
- Go to Console tab
- Look for error messages
- Check if redirect is happening

### Issue: "Access Denied" on admin dashboard
**Solution**: User is not admin
1. Run: `python backend/set_admin.py bryantech.dev@gmail.com`
2. Restart backend
3. Login again

### Issue: Charts not displaying
**Solution**: Install recharts
```bash
cd frontend
npm install recharts
```

### Issue: Login page not showing redirect message
**Solution**: Check backend logs
1. Look at backend console output
2. Should see: `[LOGIN] Token created for user: bryantech.dev@gmail.com`
3. If not, backend might not be running

---

## Quick Checklist

- [ ] Backend is running on `http://localhost:8000`
- [ ] Frontend is running on `http://localhost:3000`
- [ ] MongoDB is connected
- [ ] User with "bryantech" email exists in database
- [ ] User has role: "admin" in database
- [ ] Recharts is installed: `npm install recharts`
- [ ] Login with admin account
- [ ] See redirect message
- [ ] Redirected to `/admin/dashboard`
- [ ] Admin dashboard displays correctly
- [ ] Can access `/admin/settings`

---

## Summary

✅ Admin redirect is implemented and working
✅ Just need to ensure user has admin role
✅ First user to sign up automatically becomes admin
✅ Or use `python backend/set_admin.py bryantech.dev@gmail.com`
✅ Login will automatically redirect to admin dashboard

**Follow these steps and the admin redirect will work!**
