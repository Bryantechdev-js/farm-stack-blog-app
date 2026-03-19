# Testing Instructions - Complete FARM Stack Blog

## Prerequisites
- Backend running at `http://127.0.0.1:8000`
- Frontend running at `http://localhost:3000`
- MongoDB Atlas connected
- Browser with DevTools (F12)

## Test Scenario 1: User Registration & Authentication

### Step 1: Sign Up
1. Open `http://localhost:3000`
2. Click "Sign Up"
3. Enter:
   - Email: `user1@example.com`
   - Password: `TestPassword123`
4. Click "Sign Up"
5. **Expected**: Redirected to login page with success message

### Step 2: Login
1. Enter same credentials
2. Click "Login"
3. **Expected**: 
   - Redirected to home page
   - Navigation shows user email
   - "Dashboard" and "Logout" buttons visible
   - Cookie `access_token` set (check F12 → Application → Cookies)

### Step 3: Verify Current User
1. Open browser console (F12)
2. Run: `fetch('http://127.0.0.1:8000/auth/me', {credentials: 'include'}).then(r => r.json()).then(console.log)`
3. **Expected**: Returns user object with email, role, id

---

## Test Scenario 2: Create & Manage Posts

### Step 1: Create Post
1. Click "Dashboard"
2. Click "New Post"
3. Fill in:
   - Title: "My First Blog Post"
   - Content: "This is my first blog post with some content"
   - Image: Select any image file
4. Click "Publish Post"
5. **Expected**: 
   - Form clears
   - Post appears in "My Posts" section
   - No errors in console

### Step 2: View Post Details
1. Click on the post card
2. **Expected**:
   - Full post content displayed
   - Image shown
   - Author email and date visible
   - Like and bookmark buttons visible
   - Comments section visible

### Step 3: Edit Post
1. Go back to Dashboard
2. Click "Edit" on the post
3. Change title to "Updated Blog Post"
4. Click "Update Post"
5. **Expected**:
   - Post title updated
   - Form clears
   - No errors

### Step 4: Delete Post
1. Click "Delete" on the post
2. Confirm deletion
3. **Expected**:
   - Post removed from list
   - No errors

---

## Test Scenario 3: Comments System

### Step 1: Add Comment
1. Go to any post detail page
2. Scroll to comments section
3. Enter comment: "Great post!"
4. Click "Post Comment"
5. **Expected**:
   - Comment appears in list
   - Shows your email and current date
   - Comments count incremented

### Step 2: Delete Comment
1. Click "Delete" on your comment
2. Confirm deletion
3. **Expected**:
   - Comment removed
   - Comments count decremented

### Step 3: Multiple Comments
1. Create 3 different comments
2. **Expected**:
   - All comments visible
   - Sorted by date (newest first)
   - Comments count shows 3

---

## Test Scenario 4: Engagement Features

### Step 1: Like Post
1. On post detail page
2. Click heart button (❤️)
3. **Expected**:
   - Button highlights in red
   - Likes count increments
   - Button shows "liked" state

### Step 2: Unlike Post
1. Click heart button again
2. **Expected**:
   - Button returns to normal
   - Likes count decrements

### Step 3: Bookmark Post
1. Click bookmark button (🔖)
2. **Expected**:
   - Button highlights in yellow
   - Bookmarks count increments

### Step 4: Unbookmark Post
1. Click bookmark button again
2. **Expected**:
   - Button returns to normal
   - Bookmarks count decrements

---

## Test Scenario 5: Home Page

### Step 1: View All Posts
1. Click "Home" or logo
2. **Expected**:
   - All posts displayed in grid
   - Shows engagement metrics (likes, comments, bookmarks)
   - Shows author email
   - Posts sorted by date (newest first)

### Step 2: Navigation
1. Check navbar shows:
   - Blog logo/title
   - Profile button with email
   - Dashboard link
   - Logout button
   - Admin link (if admin)

---

## Test Scenario 6: User Profile

### Step 1: View Profile
1. Click profile button (👤 email)
2. **Expected**:
   - Email displayed
   - Role displayed (user or admin)
   - Join date displayed
   - Quick action links visible

### Step 2: Logout
1. Click "Logout" button
2. **Expected**:
   - Redirected to home page
   - Navigation shows "Login" and "Sign Up"
   - Cookie cleared

---

## Test Scenario 7: Admin Features

### Step 1: Create Admin User
1. In MongoDB, update a user's role to "admin":
   ```javascript
   db.users.updateOne(
     {email: "admin@example.com"},
     {$set: {role: "admin"}}
   )
   ```

### Step 2: Login as Admin
1. Login with admin account
2. **Expected**: "Admin" button visible in navbar

### Step 3: Access Admin Dashboard
1. Click "Admin" button
2. **Expected**: Admin dashboard loads with 4 tabs

### Step 4: Analytics Tab
1. Click "Analytics" tab
2. **Expected**:
   - Shows total users, posts, comments
   - Shows posts from last 7 days
   - Shows total likes and bookmarks
   - Shows top 5 posts
   - Shows top 5 authors

### Step 5: Users Tab
1. Click "Users" tab
2. **Expected**:
   - Table of all users
   - Can change user role (dropdown)
   - Can delete users
   - Changes reflected immediately

### Step 6: Posts Tab
1. Click "Posts" tab
2. **Expected**:
   - Table of all posts
   - Shows engagement metrics
   - Can delete any post

### Step 7: Comments Tab
1. Click "Comments" tab
2. **Expected**:
   - Table of all comments
   - Shows author, content, date
   - Can delete any comment

---

## Test Scenario 8: RBAC (Role-Based Access Control)

### Step 1: User Can Only Edit Own Posts
1. Create post as user1
2. Login as user2
3. Try to edit user1's post (via API)
4. **Expected**: 403 Forbidden error

### Step 2: Admin Can Edit Any Post
1. Login as admin
2. Go to admin dashboard
3. Delete any user's post
4. **Expected**: Post deleted successfully

### Step 3: User Can Only Delete Own Comments
1. Create comment as user1
2. Login as user2
3. Try to delete user1's comment (via API)
4. **Expected**: 403 Forbidden error

### Step 4: Admin Can Delete Any Comment
1. Login as admin
2. Go to admin dashboard → Comments
3. Delete any comment
4. **Expected**: Comment deleted successfully

---

## Test Scenario 9: File Upload

### Step 1: Upload Image
1. Create new post
2. Select image file
3. Publish post
4. **Expected**:
   - Image uploaded successfully
   - Image displayed on post detail page
   - Image accessible at `/uploads/[uuid].ext`

### Step 2: Multiple Uploads
1. Create 3 posts with different images
2. **Expected**:
   - All images uploaded with unique names
   - All images displayed correctly
   - No conflicts or overwrites

---

## Test Scenario 10: Error Handling

### Step 1: Invalid Email
1. Try to signup with invalid email
2. **Expected**: Validation error

### Step 2: Short Password
1. Try to signup with password < 8 chars
2. **Expected**: Validation error

### Step 3: Duplicate Email
1. Try to signup with existing email
2. **Expected**: "Email already exists" error

### Step 4: Wrong Credentials
1. Try to login with wrong password
2. **Expected**: "Invalid credentials" error

### Step 5: Missing Fields
1. Try to create post without title
2. **Expected**: "Please fill title and content" error

### Step 6: Missing Image
1. Try to create post without image
2. **Expected**: "Please select an image" error

---

## Test Scenario 11: API Testing

### Test Health Endpoint
```bash
curl http://127.0.0.1:8000/health
# Expected: {"status":"ok"}
```

### Test Get Posts
```bash
curl http://127.0.0.1:8000/posts
# Expected: Array of posts
```

### Test Get Analytics (Admin)
```bash
curl -b "access_token=YOUR_TOKEN" http://127.0.0.1:8000/admin/analytics
# Expected: Analytics data
```

---

## Test Scenario 12: Performance

### Step 1: Load Time
1. Open home page
2. Check Network tab (F12)
3. **Expected**: Page loads in < 2 seconds

### Step 2: Post Creation
1. Create post
2. **Expected**: Completes in < 5 seconds

### Step 3: Comment Addition
1. Add comment
2. **Expected**: Completes in < 2 seconds

### Step 4: Admin Dashboard
1. Open admin dashboard
2. **Expected**: Loads in < 3 seconds

---

## Test Scenario 13: Browser Compatibility

### Test on Different Browsers
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Test on Different Devices
- [ ] Desktop
- [ ] Tablet
- [ ] Mobile

---

## Test Scenario 14: Data Persistence

### Step 1: Refresh Page
1. Create post
2. Refresh page (F5)
3. **Expected**: Post still visible

### Step 2: Logout & Login
1. Create post
2. Logout
3. Login again
4. **Expected**: Post still visible

### Step 3: Close Browser
1. Create post
2. Close browser
3. Reopen and login
4. **Expected**: Post still visible

---

## Debugging Tips

### Check Backend Logs
```bash
# Terminal running backend
# Look for error messages
# Check database queries
```

### Check Frontend Console
```bash
# F12 → Console
# Look for error messages
# Check API logs (🔗, 📡, ❌)
```

### Check Network Tab
```bash
# F12 → Network
# Check request/response headers
# Check CORS headers
# Check response status codes
```

### Check Cookies
```bash
# F12 → Application → Cookies
# Verify access_token is set
# Check cookie attributes (HttpOnly, SameSite)
```

### Check MongoDB
```bash
# MongoDB Atlas console
# Verify collections exist
# Check document structure
# Verify data is being saved
```

---

## Success Criteria

All tests pass when:
- ✅ User can signup and login
- ✅ User can create, edit, delete posts
- ✅ User can comment on posts
- ✅ User can like and bookmark posts
- ✅ Admin can manage users, posts, comments
- ✅ Admin can view analytics
- ✅ File uploads work
- ✅ RBAC controls work
- ✅ No errors in console
- ✅ No errors in backend logs
- ✅ All API endpoints respond correctly
- ✅ Data persists after refresh
- ✅ Performance is acceptable

---

## Troubleshooting

### Posts not loading
1. Check backend is running
2. Check MongoDB connection
3. Check browser console for errors
4. Check network tab for failed requests

### Comments not saving
1. Check user is authenticated
2. Check backend logs
3. Check MongoDB comments collection

### Admin dashboard not loading
1. Check user has admin role
2. Check backend logs
3. Check network tab

### Images not uploading
1. Check uploads directory exists
2. Check file permissions
3. Check file size
4. Check backend logs

### Cookies not set
1. Check login was successful
2. Check browser cookie settings
3. Check CORS configuration
4. Check secure flag (should be false for localhost)

---

## Next Steps

After all tests pass:
1. Deploy to production
2. Set up monitoring
3. Add more features
4. Optimize performance
5. Add security hardening

---

**Happy Testing! 🚀**
