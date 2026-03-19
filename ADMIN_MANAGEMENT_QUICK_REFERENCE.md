# Admin Management System - Quick Reference Guide

## 🚀 Quick Start

### Access Admin Dashboard
1. Login with admin account
2. You'll be automatically redirected to `/admin/dashboard`
3. Or navigate directly to: `http://localhost:3000/admin/dashboard`

### Management Pages
From the dashboard, access management pages via quick links or direct URLs:

| Page | URL | Purpose |
|------|-----|---------|
| Users | `/admin/users` | Manage users, change roles, delete users |
| Posts | `/admin/posts` | View posts, delete posts, see engagement |
| Comments | `/admin/comments` | View comments, delete comments |
| Settings | `/admin/settings` | Update admin profile, change password |

---

## 👥 User Management

### View Users
- Navigate to `/admin/users`
- See all users in a table with email, name, role, and join date

### Search Users
- Use the search box to filter by email or name
- Search is real-time and case-insensitive

### Change User Role
1. Click "Edit" button next to user
2. Select new role (User or Admin)
3. Click "Save Changes"
4. User role is updated immediately

### Delete User
1. Click "Delete" button next to user
2. Confirm deletion in dialog
3. User and all their posts/comments are deleted

### Statistics
- **Total Users**: Count of all users
- **Admins**: Count of admin users
- **Regular Users**: Count of regular users

---

## 📝 Post Management

### View Posts
- Navigate to `/admin/posts`
- See all posts with title, content preview, author, and engagement stats

### Search Posts
- Use search box to filter by post title or author email
- Search is real-time and case-insensitive

### Sort Posts
- **Newest First**: Most recent posts at top
- **Oldest First**: Oldest posts at top
- **Most Engagement**: Posts with most likes + comments + bookmarks at top

### Delete Post
1. Click "Delete" button next to post
2. Confirm deletion in dialog
3. Post and all related comments are deleted

### Engagement Stats
Each post shows:
- ❤️ **Likes**: Number of likes
- 💬 **Comments**: Number of comments
- 🔖 **Bookmarks**: Number of bookmarks

### Statistics
- **Total Posts**: Count of all posts
- **Total Likes**: Sum of all likes across posts
- **Total Comments**: Sum of all comments across posts
- **Total Bookmarks**: Sum of all bookmarks across posts

---

## 💬 Comment Management

### View Comments
- Navigate to `/admin/comments`
- See all comments with author, content, and date

### Search Comments
- Use search box to filter by author email or comment content
- Search is real-time and case-insensitive

### Sort Comments
- **Newest First**: Most recent comments at top
- **Oldest First**: Oldest comments at top

### Delete Comment
1. Click "Delete" button next to comment
2. Confirm deletion in dialog
3. Comment is deleted and post comment count is updated

### Statistics
- **Total Comments**: Count of all comments
- **Unique Commenters**: Count of users who have commented

---

## 🔐 Security & Permissions

### Admin Requirements
- Only users with "admin" role can access admin pages
- Non-admin users are redirected to home page
- Unauthenticated users are redirected to login page

### Protected Actions
- All CRUD operations require admin authentication
- All actions are logged on the backend
- Destructive actions require confirmation

### Last Admin Protection
- System prevents removing the last admin
- At least one admin must always exist
- If you try to demote the last admin, you'll see an error message

---

## ⚠️ Important Notes

### Cascading Deletes
When you delete a user:
- All their posts are deleted
- All their comments are deleted
- All likes/bookmarks on their posts are deleted

When you delete a post:
- All comments on that post are deleted
- All likes/bookmarks on that post are deleted

When you delete a comment:
- The post's comment count is decremented
- The comment is removed from the database

### No Undo
- All deletions are permanent
- There is no trash/recycle bin
- Always confirm before deleting

### Real-time Updates
- All changes are reflected immediately
- No page refresh needed
- Statistics update automatically

---

## 🎯 Common Tasks

### Make Someone an Admin
1. Go to `/admin/users`
2. Find the user in the list
3. Click "Edit"
4. Select "Admin" role
5. Click "Save Changes"

### Remove Admin Privileges
1. Go to `/admin/users`
2. Find the admin user
3. Click "Edit"
4. Select "User" role
5. Click "Save Changes"
6. (Note: Cannot remove the last admin)

### Delete Inappropriate Content
1. Go to `/admin/posts` or `/admin/comments`
2. Find the content
3. Click "Delete"
4. Confirm deletion

### Monitor Engagement
1. Go to `/admin/dashboard`
2. View engagement charts
3. Go to `/admin/posts` to see detailed engagement per post

### View User Activity
1. Go to `/admin/users`
2. See when each user joined
3. Go to `/admin/posts` to see posts by specific author

---

## 🆘 Troubleshooting

### "Access Denied" Error
- You are not logged in as an admin
- Login with admin account
- Or ask another admin to promote your account

### "Cannot remove the last admin" Error
- You tried to demote the only admin
- Promote another user to admin first
- Then you can demote the last admin

### Page Not Loading
- Check your internet connection
- Refresh the page
- Clear browser cache
- Try logging out and back in

### Changes Not Saving
- Check for error toast notifications
- Verify you have admin permissions
- Try the action again
- Check browser console for errors

### Search Not Working
- Make sure you're typing in the search box
- Search is case-insensitive
- Try searching for partial matches
- Refresh page if search seems stuck

---

## 📊 Dashboard Overview

The admin dashboard shows:

### Key Metrics
- Total Users
- Total Posts
- Total Comments
- Total Engagement (Likes + Bookmarks)

### Charts
- **Post Engagement**: Top 5 posts with likes, comments, bookmarks
- **Active Users Trend**: User activity over last 30 days
- **Post Rate Trend**: Posts created over last 30 days

### Quick Links
- Manage Users
- Manage Posts
- Manage Comments

---

## 🔗 API Endpoints (For Developers)

All endpoints require admin authentication via JWT cookie.

### Users
```
GET    /api/admin/users                    - Get all users
PUT    /api/admin/users/{user_id}/role     - Update user role
DELETE /api/admin/users/{user_id}          - Delete user
```

### Posts
```
GET    /api/admin/posts                    - Get all posts
DELETE /api/posts/{post_id}                - Delete post
```

### Comments
```
GET    /api/admin/comments                 - Get all comments
DELETE /api/admin/comments/{comment_id}    - Delete comment
```

### Analytics
```
GET    /api/admin/analytics                - Get basic analytics
GET    /api/admin/analytics/advanced       - Get advanced analytics
```

---

## 💡 Tips & Best Practices

1. **Regular Backups**: Backup your MongoDB database regularly
2. **Monitor Activity**: Check admin dashboard regularly for insights
3. **Moderate Content**: Review comments and posts for inappropriate content
4. **Manage Users**: Keep user list clean by removing inactive accounts
5. **Promote Admins**: Have at least 2 admins for redundancy
6. **Document Changes**: Keep notes of major admin actions
7. **Test Changes**: Test on a staging environment first
8. **Review Logs**: Check backend logs for errors and issues

---

## 📞 Support

If you encounter issues:

1. Check this guide for solutions
2. Review error messages carefully
3. Check browser console (F12) for errors
4. Check backend logs for server errors
5. Verify database connection
6. Restart backend and frontend services

---

**Last Updated**: March 2026
**Version**: 1.0.0
**Status**: Production Ready ✅
