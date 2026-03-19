# Admin System Setup Guide

## Overview
The blog system now has a proper admin system where:
- **The first user to sign up automatically becomes the admin**
- Subsequent users are regular users
- Admins can promote/demote other users from the admin dashboard
- The system prevents removing the last admin

## How It Works

### 1. First User Signup (Becomes Admin)
When you sign up for the first time:
1. The system checks if any users exist in the database
2. If no users exist, the new user is automatically assigned the **"admin"** role
3. All subsequent users are assigned the **"user"** role

### 2. Admin Dashboard Access
Once you're logged in as an admin:
1. Navigate to `/admin` or click the "Admin" link in the navbar
2. You'll see the admin dashboard with 4 tabs:
   - **Analytics**: System statistics and engagement metrics
   - **Users**: Manage all users and their roles
   - **Posts**: View and delete posts
   - **Comments**: View and delete comments

### 3. User Role Management
From the Users tab, admins can:
- **Promote users to admin**: Select "Admin" from the role dropdown
- **Demote admins to users**: Select "User" from the role dropdown
- **Delete users**: Remove users (also deletes their posts and comments)

### 4. Admin Protection
- **Cannot remove the last admin**: If there's only one admin, you cannot demote them
- **Error message**: "Cannot remove the last admin. Promote another user to admin first."
- **Solution**: Promote another user to admin first, then you can demote the original admin

## Setup Instructions

### Step 1: Clear Database (Optional)
If you already have users in the database and want to make the first signup an admin:
1. Delete all users from MongoDB
2. Or manually update the first user's role to "admin" in MongoDB

### Step 2: First User Signup
1. Go to `http://localhost:3000/auth/signup`
2. Create an account with any email and password
3. This user will automatically be assigned the **admin** role
4. You'll see `"is_admin": true` in the response

### Step 3: Login as Admin
1. Go to `http://localhost:3000/auth/login`
2. Login with the admin account
3. You should see the "Admin" link in the navbar
4. Click "Admin" to access the admin dashboard

### Step 4: Manage Other Users
1. Create more user accounts (they'll have "user" role)
2. Go to Admin Dashboard → Users tab
3. Promote users to admin or demote them as needed

## Admin Dashboard Features

### Analytics Tab
- **Total Users**: Count of all registered users
- **Total Posts**: Count of all blog posts
- **Total Comments**: Count of all comments
- **Posts (Last 7 Days)**: Posts created in the last week
- **Total Likes**: Sum of all likes across posts
- **Total Bookmarks**: Sum of all bookmarks across posts
- **Top Posts**: 5 most liked posts
- **Top Authors**: 5 most active authors

### Users Tab
- **View all users** with their email, role, and join date
- **Change user role**: Dropdown to promote/demote users
- **Delete users**: Remove users and their content

### Posts Tab
- **View all posts** with title, author, and engagement metrics
- **Delete posts**: Remove inappropriate or spam posts
- **Engagement stats**: Likes, comments, bookmarks per post

### Comments Tab
- **View all comments** with author, content, and date
- **Delete comments**: Remove inappropriate comments
- **Moderation**: Keep discussions clean and on-topic

## Files Modified

### Backend Changes
1. **`backend/app/api/auth.py`**
   - Modified `signup()` to check if user is first user
   - First user gets "admin" role, others get "user" role
   - Returns `is_admin` flag in response

2. **`backend/app/api/admin.py`**
   - Modified `update_user_role()` to accept JSON body with role
   - Added protection to prevent removing the last admin
   - Returns error if trying to demote the only admin

### Frontend Changes
- No changes needed - admin dashboard already checks for admin role

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password": "hashed_password",
  "role": "admin" or "user",
  "full_name": "Optional Name",
  "bio": "Optional bio",
  "avatar_url": "Optional URL",
  "created_at": ISODate
}
```

## API Endpoints

### Admin-Only Endpoints
All these endpoints require `role: "admin"`:

**Users Management**
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/{user_id}/role` - Update user role
- `DELETE /api/admin/users/{user_id}` - Delete user

**Posts Management**
- `GET /api/admin/posts` - Get all posts
- `DELETE /api/admin/posts/{post_id}` - Delete post

**Comments Management**
- `GET /api/admin/comments` - Get all comments
- `DELETE /api/admin/comments/{comment_id}` - Delete comment

**Analytics**
- `GET /api/admin/analytics` - Get system analytics

## Troubleshooting

### Issue: Can't access admin dashboard
**Solution**: 
1. Check if you're logged in as an admin
2. Go to `/api/auth/me` to verify your role
3. If role is "user", ask another admin to promote you

### Issue: "Cannot remove the last admin" error
**Solution**:
1. Promote another user to admin first
2. Then you can demote the original admin
3. This prevents the system from having no admins

### Issue: First user didn't become admin
**Solution**:
1. Check if there were already users in the database
2. Delete all users from MongoDB
3. Sign up again - the first user will be admin

### Issue: Admin link not showing in navbar
**Solution**:
1. Refresh the page
2. Check if you're logged in
3. Check your role with `/api/auth/me`
4. If role is "user", you need admin promotion

## Security Notes

- Admin role is stored in JWT token
- Token is httpOnly cookie (secure)
- Admin endpoints verify role on every request
- Cannot remove the last admin (prevents lockout)
- Admins can delete users and posts (use carefully)

## Testing Checklist

- [ ] First user signup → becomes admin
- [ ] Second user signup → becomes regular user
- [ ] Admin can access `/admin` dashboard
- [ ] Regular user redirected from `/admin` to home
- [ ] Admin can promote users to admin
- [ ] Admin can demote users to regular users
- [ ] Cannot demote the last admin
- [ ] Admin can delete users, posts, comments
- [ ] Analytics show correct data
- [ ] Admin link appears in navbar for admins only

## Next Steps

1. **First signup**: Create your admin account
2. **Login**: Login with admin credentials
3. **Access dashboard**: Click "Admin" in navbar
4. **Manage users**: Promote/demote users as needed
5. **Monitor system**: Check analytics and manage content

## Summary

The admin system is now fully functional:
- ✅ First user becomes admin automatically
- ✅ Admins can manage users, posts, and comments
- ✅ System prevents removing the last admin
- ✅ Admin dashboard shows analytics and management tools
- ✅ Role-based access control on all admin endpoints
