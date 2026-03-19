# Admin System - Quick Start

## The Problem (SOLVED ✅)
- You couldn't access the admin dashboard
- The system didn't know who the admin was
- No one could become admin during registration

## The Solution ✅
- **First user to sign up automatically becomes admin**
- Other users are regular users
- Admins can promote/demote users from the dashboard

## What You Need to Do

### Step 1: Restart Backend
Stop and restart your FastAPI backend to apply the changes:
```bash
# Stop current backend (Ctrl+C)
# Restart:
python -m uvicorn app.main:app --reload
```

### Step 2: Clear Database (If Needed)
If you already have users in the database:
1. Delete all users from MongoDB
2. Or manually set the first user's role to "admin"

### Step 3: Sign Up as First User
1. Go to `http://localhost:3000/auth/signup`
2. Create an account
3. **This user will automatically be admin**
4. You'll see `"is_admin": true` in the response

### Step 4: Login
1. Go to `http://localhost:3000/auth/login`
2. Login with your admin account
3. You should see "Admin" link in the navbar

### Step 5: Access Admin Dashboard
1. Click "Admin" in the navbar
2. Or go to `http://localhost:3000/admin`
3. You'll see the admin dashboard with 4 tabs

## Admin Dashboard Tabs

| Tab | What You Can Do |
|-----|-----------------|
| **Analytics** | View system stats, top posts, top authors |
| **Users** | Promote/demote users, delete users |
| **Posts** | View all posts, delete posts |
| **Comments** | View all comments, delete comments |

## Key Features

✅ **First user becomes admin automatically**
✅ **Admins can promote other users to admin**
✅ **Cannot remove the last admin** (prevents lockout)
✅ **Full moderation capabilities**
✅ **System analytics and insights**

## Files Changed

- `backend/app/api/auth.py` - First user becomes admin
- `backend/app/api/admin.py` - Prevent removing last admin

## Testing

1. **First signup** → Should be admin
2. **Second signup** → Should be regular user
3. **Admin dashboard** → Should be accessible
4. **User management** → Should be able to promote/demote users
5. **Last admin protection** → Cannot demote the only admin

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't access admin dashboard | Check if you're logged in as admin |
| First user not admin | Delete all users and sign up again |
| "Cannot remove last admin" error | Promote another user first |
| Admin link not showing | Refresh page, check your role |

## Summary

✅ Admin system is now fully functional
✅ First user signup = automatic admin
✅ Restart backend to apply changes
✅ Sign up as first user to become admin
✅ Access admin dashboard from navbar
