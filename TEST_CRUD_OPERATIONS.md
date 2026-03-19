# Test CRUD Operations - Complete Guide

## Prerequisites

1. Backend running on `http://localhost:8000`
2. Frontend running on `http://localhost:3000`
3. MongoDB connected
4. User account created

## Test Sequence

### 1. CREATE - Create a New Post

**Steps**:
1. Login at `http://localhost:3000/auth/login`
2. Go to Dashboard (`http://localhost:3000/dashboard`)
3. Click "+ New Post" button
4. Fill in:
   - Title: "Test Post"
   - Content: "This is a test post for CRUD operations"
   - Image: Select any image file
5. Click "Publish Post"

**Expected Result**:
- ✅ Toast shows "Post published successfully!"
- ✅ Post appears in "My Posts" list
- ✅ Post has correct title and content
- ✅ Post shows engagement metrics (0 likes, 0 comments, 0 bookmarks)

**If Failed**:
- Check browser console for errors
- Check Network tab for POST request to `/posts`
- Check response status (should be 200)
- Check backend logs for errors

### 2. READ - View All Posts

**Steps**:
1. Go to Home page (`http://localhost:3000/`)
2. Scroll through posts

**Expected Result**:
- ✅ All posts are displayed
- ✅ Post from Step 1 appears in the list
- ✅ Each post shows title, content preview, and engagement metrics
- ✅ Can click on any post to view details

**If Failed**:
- Check Network tab for GET request to `/posts`
- Check response includes your post
- Check browser console for errors

### 3. READ - View Post Details

**Steps**:
1. From Home page, click on the post created in Step 1
2. View the post detail page

**Expected Result**:
- ✅ Full post content is displayed
- ✅ Post image is shown
- ✅ Author email and date are displayed
- ✅ Like and bookmark buttons are visible
- ✅ Comments section is visible
- ✅ Can add comment if logged in

**If Failed**:
- Check Network tab for GET request to `/posts/{id}`
- Check response includes post data
- Check browser console for errors

### 4. UPDATE - Edit Your Post

**Steps**:
1. Go to Dashboard
2. Find the post created in Step 1
3. Click "Edit" button
4. Change:
   - Title: "Updated Test Post"
   - Content: "This post has been updated"
5. Click "Update Post"

**Expected Result**:
- ✅ Toast shows "Post updated successfully!"
- ✅ Post title and content are updated
- ✅ Post still appears in dashboard
- ✅ Changes are reflected on home page

**If Failed**:
- Check Network tab for PUT request to `/posts/{id}`
- Check response status (should be 200)
- Check backend logs for errors
- Refresh page to see if changes persisted

### 5. DELETE - Delete Your Post

**Steps**:
1. Go to Dashboard
2. Find the post created in Step 1
3. Click "Delete" button
4. Confirm deletion

**Expected Result**:
- ✅ Toast shows "Post deleted successfully!"
- ✅ Post disappears from dashboard
- ✅ Post no longer appears on home page
- ✅ Post detail page shows 404 or "Post not found"

**If Failed**:
- Check Network tab for DELETE request to `/posts/{id}`
- Check response status (should be 200)
- Check backend logs for errors
- Refresh page to verify deletion

## Additional CRUD Tests

### Test Comments (CREATE, READ, DELETE)

**CREATE Comment**:
1. Go to any post detail page
2. Scroll to comments section
3. Type a comment in the text area
4. Click "Post Comment"

**Expected Result**:
- ✅ Toast shows success
- ✅ Comment appears in comments list
- ✅ Comment shows your email and date

**READ Comments**:
1. View any post detail page
2. Comments section shows all comments

**Expected Result**:
- ✅ All comments are displayed
- ✅ Each comment shows author, date, and content

**DELETE Comment**:
1. On post detail page, find your comment
2. Click "Delete" button
3. Confirm deletion

**Expected Result**:
- ✅ Toast shows success
- ✅ Comment disappears from list

### Test Likes (CREATE/DELETE - Toggle)

**LIKE Post**:
1. Go to post detail page
2. Click ❤️ button

**Expected Result**:
- ✅ Button changes color (red background)
- ✅ Like count increases by 1
- ✅ Toast shows success

**UNLIKE Post**:
1. Click ❤️ button again

**Expected Result**:
- ✅ Button returns to normal color
- ✅ Like count decreases by 1
- ✅ Toast shows success

### Test Bookmarks (CREATE/DELETE - Toggle)

**BOOKMARK Post**:
1. Go to post detail page
2. Click 🔖 button

**Expected Result**:
- ✅ Button changes color (yellow background)
- ✅ Bookmark count increases by 1
- ✅ Toast shows success

**UNBOOKMARK Post**:
1. Click 🔖 button again

**Expected Result**:
- ✅ Button returns to normal color
- ✅ Bookmark count decreases by 1
- ✅ Toast shows success

## CRUD Operations Checklist

### Create
- [ ] Can create post with title, content, and image
- [ ] Post appears in dashboard
- [ ] Post appears on home page
- [ ] Toast shows success message
- [ ] Can create multiple posts

### Read
- [ ] Can view all posts on home page
- [ ] Can view post details
- [ ] Can view comments on post
- [ ] Can view engagement metrics
- [ ] Post data is correct

### Update
- [ ] Can edit post title
- [ ] Can edit post content
- [ ] Can update post image
- [ ] Changes are saved
- [ ] Changes appear on home page
- [ ] Toast shows success message

### Delete
- [ ] Can delete own post
- [ ] Post disappears from dashboard
- [ ] Post disappears from home page
- [ ] Post detail page shows error
- [ ] Toast shows success message
- [ ] Cannot delete other users' posts

## Network Requests to Verify

### Create Post
```
POST /posts
Content-Type: multipart/form-data
Response: 200 OK
```

### Read Posts
```
GET /posts
Response: 200 OK
Body: Array of posts
```

### Read Single Post
```
GET /posts/{id}
Response: 200 OK
Body: Post object
```

### Update Post
```
PUT /posts/{id}
Content-Type: multipart/form-data
Response: 200 OK
```

### Delete Post
```
DELETE /posts/{id}
Response: 200 OK
```

### Create Comment
```
POST /posts/{id}/comments
Content-Type: application/json
Response: 200 OK
```

### Get Comments
```
GET /posts/{id}/comments
Response: 200 OK
Body: Array of comments
```

### Delete Comment
```
DELETE /posts/{id}/comments/{comment_id}
Response: 200 OK
```

### Like Post
```
POST /posts/{id}/like
Response: 200 OK
Body: {liked: true/false}
```

### Bookmark Post
```
POST /posts/{id}/bookmark
Response: 200 OK
Body: {bookmarked: true/false}
```

## Troubleshooting CRUD Issues

### Issue: Can't Create Post
**Solutions**:
1. Check you're logged in
2. Check all fields are filled
3. Check image is selected
4. Check Network tab for errors
5. Check backend logs

### Issue: Can't Edit Post
**Solutions**:
1. Check you're the post author
2. Check all fields are filled
3. Check Network tab for PUT request
4. Check response status is 200
5. Refresh page to verify changes

### Issue: Can't Delete Post
**Solutions**:
1. Check you're the post author
2. Check confirmation dialog appears
3. Check Network tab for DELETE request
4. Check response status is 200
5. Refresh page to verify deletion

### Issue: Comments Not Showing
**Solutions**:
1. Check Network tab for GET request to `/comments`
2. Check response includes comments
3. Refresh page
4. Check browser console for errors

### Issue: Like/Bookmark Not Working
**Solutions**:
1. Check you're logged in
2. Check Network tab for POST request
3. Check response status is 200
4. Check response includes `liked` or `bookmarked` field
5. Refresh page to verify

## Success Criteria

All CRUD operations should work:
- ✅ Create post with image
- ✅ Read all posts
- ✅ Read single post details
- ✅ Update post
- ✅ Delete post
- ✅ Create comment
- ✅ Read comments
- ✅ Delete comment
- ✅ Like/unlike post
- ✅ Bookmark/unbookmark post
- ✅ All operations show toast notifications
- ✅ All operations update UI immediately
- ✅ All operations persist to database

If all tests pass, CRUD operations are working correctly! 🎉
