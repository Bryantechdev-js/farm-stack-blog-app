# Image Display Fix - Post Detail Page

## Problem
Images are not displaying on the post detail page.

## Root Causes (Possible)

1. **Image path not being returned correctly from backend**
2. **Image path not being rewritten correctly by Next.js**
3. **Backend not serving the uploads directory**
4. **Image file doesn't exist on server**
5. **CORS issue preventing image load**

---

## Debugging Steps

### Step 1: Check Browser Console
1. Go to http://localhost:3000/posts/[post-id]
2. Open DevTools (F12)
3. Go to Console tab
4. Look for these logs:
   ```
   Post data received: { ... }
   Image path: /uploads/filename.jpg
   Image loaded successfully: /uploads/filename.jpg
   ```

### Step 2: Check Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Look for image requests
4. Check if they return 200 (success) or 404 (not found)

**Expected:**
- Request URL: `http://localhost:3000/uploads/filename.jpg`
- Status: 200
- Type: image/jpeg (or image/png)

**If 404:**
- Image file doesn't exist
- Path is incorrect
- Backend not serving uploads

### Step 3: Check Backend Logs
When you load a post detail page, check backend console for:

```
[GET] /api/posts/[post-id]
```

The response should include:
```json
{
  "image": "/uploads/uuid.jpg",
  ...
}
```

### Step 4: Check if Image File Exists
```bash
# Check if uploads directory exists
ls -la backend/uploads/

# Should show uploaded images:
# -rw-r--r-- 1 user group 12345 Mar 19 10:00 4b864d1f-d61c-4117-824c-1897e8543e43.jpg
# -rw-r--r-- 1 user group 12345 Mar 19 10:01 75431b69-34d0-4363-804a-4145ee8a86c6.jpg
```

### Step 5: Test Image URL Directly
Try accessing the image directly in browser:

```
http://localhost:3000/uploads/4b864d1f-d61c-4117-824c-1897e8543e43.jpg
```

**Expected:**
- Image displays in browser
- Status 200 in Network tab

**If 404:**
- Check filename is correct
- Check file exists in backend/uploads/
- Check backend is serving uploads directory

---

## Solutions

### Solution 1: Verify Backend is Serving Uploads
Check `backend/app/main.py`:

```python
# Mount uploads directory
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
```

**If missing:**
- Add the mount statement
- Restart backend

### Solution 2: Verify Next.js Rewrites
Check `frontend/next.config.ts`:

```typescript
rewrites: async () => {
  return {
    beforeFiles: [
      {
        source: '/uploads/:path*',
        destination: 'http://localhost:8000/uploads/:path*',
      },
    ],
  };
}
```

**If missing:**
- Add the rewrite
- Restart frontend

### Solution 3: Verify Image Path Format
Check `backend/app/api/posts.py` format_post():

```python
def format_post(post):
    image = post.get("image")
    # Ensure image path is correct for frontend rewrite
    if image and not image.startswith("/"):
        image = f"/{image}"
    
    return {
        "image": image,
        ...
    }
```

**If missing:**
- Add the path formatting
- Restart backend

### Solution 4: Check Image Upload
When creating a post:

1. Go to http://localhost:3000/dashboard
2. Click "+ New Post"
3. Fill in title and content
4. **Select an image file**
5. Click "Publish Post"
6. Check backend console for upload confirmation
7. Check backend/uploads/ for the file

**If file not created:**
- Check file permissions
- Check disk space
- Check backend logs for errors

---

## Complete Testing Checklist

### Test 1: Image Upload
- [ ] Go to dashboard
- [ ] Create new post with image
- [ ] Check backend/uploads/ for file
- [ ] File should exist with UUID name

### Test 2: Image Display on Home Page
- [ ] Go to home page
- [ ] Post should show image thumbnail
- [ ] Image should load without errors
- [ ] Check DevTools Network tab for 200 status

### Test 3: Image Display on Detail Page
- [ ] Click on post to view details
- [ ] Image should display at top of post
- [ ] Image should be full width
- [ ] Check DevTools Console for logs
- [ ] Check DevTools Network tab for 200 status

### Test 4: Image Path Verification
- [ ] Open DevTools Console
- [ ] Look for "Image path: /uploads/..."
- [ ] Copy the path
- [ ] Try accessing directly: http://localhost:3000/uploads/...
- [ ] Image should display

### Test 5: Backend Serving
- [ ] Try accessing: http://localhost:8000/uploads/filename.jpg
- [ ] Image should display
- [ ] If 404, check file exists in backend/uploads/

---

## Console Logs Added

The post detail page now logs:

```javascript
// When post data is received
console.log('Post data received:', data);
console.log('Image path:', data.image);

// When image loads successfully
console.log('Image loaded successfully:', post.image);

// When image fails to load
console.error('Image failed to load:', post.image);
```

**Check these logs in DevTools Console to debug.**

---

## Common Issues & Solutions

### Issue 1: Image Shows 404 in Network Tab
**Cause:** Image file doesn't exist or path is wrong

**Solutions:**
1. Check file exists in backend/uploads/
2. Check filename in database matches file
3. Check path format (should start with /)
4. Restart backend

### Issue 2: Image Path is null/undefined
**Cause:** Backend not returning image path

**Solutions:**
1. Check format_post() function
2. Check image is being saved to database
3. Check database has image field
4. Restart backend

### Issue 3: Image Loads on Home but Not on Detail
**Cause:** Different API endpoints returning different data

**Solutions:**
1. Check both endpoints return same format
2. Check both use format_post()
3. Check image path is consistent
4. Restart backend

### Issue 4: Image Loads Slowly
**Cause:** Large image file or network issue

**Solutions:**
1. Compress image before upload
2. Check network speed
3. Check backend performance
4. Add loading state

---

## API Response Format

### Expected Response from GET /api/posts/{id}
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Post Title",
  "content": "Post content...",
  "image": "/uploads/4b864d1f-d61c-4117-824c-1897e8543e43.jpg",
  "author_id": "507f1f77bcf86cd799439012",
  "author_email": "user@example.com",
  "created_at": "2026-03-19T10:00:00",
  "updated_at": "2026-03-19T10:00:00",
  "likes_count": 5,
  "comments_count": 2,
  "bookmarks_count": 1
}
```

**Key Points:**
- `image` field should start with `/uploads/`
- `image` should not be null or empty
- `image` should be a valid file path

---

## Database Check

### Check Image in Database
```javascript
// MongoDB
db.posts.find({ _id: ObjectId("507f1f77bcf86cd799439011") })

// Should show:
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "title": "Post Title",
  "image": "uploads/4b864d1f-d61c-4117-824c-1897e8543e43.jpg",
  ...
}
```

**Note:** In database, image path doesn't have leading `/`, but format_post() adds it.

---

## File Structure

```
backend/
├── uploads/
│   ├── 4b864d1f-d61c-4117-824c-1897e8543e43.jpg
│   ├── 75431b69-34d0-4363-804a-4145ee8a86c6.jpg
│   └── ...
├── app/
│   ├── main.py (mounts /uploads)
│   ├── api/
│   │   └── posts.py (format_post adds /)
│   └── ...
└── ...

frontend/
├── next.config.ts (rewrites /uploads/*)
├── src/
│   └── app/
│       └── posts/
│           └── [id]/
│               └── page.tsx (displays image)
└── ...
```

---

## Testing with cURL

### Get Post with Image
```bash
curl http://localhost:8000/api/posts/507f1f77bcf86cd799439011 \
  -H "Cookie: access_token=YOUR_TOKEN"

# Should return image path like:
# "image": "/uploads/4b864d1f-d61c-4117-824c-1897e8543e43.jpg"
```

### Access Image Directly
```bash
# Via Next.js (frontend)
curl http://localhost:3000/uploads/4b864d1f-d61c-4117-824c-1897e8543e43.jpg

# Via Backend (direct)
curl http://localhost:8000/uploads/4b864d1f-d61c-4117-824c-1897e8543e43.jpg

# Both should return 200 and image data
```

---

## Changes Made

### frontend/src/app/posts/[id]/page.tsx
1. Added error handling to image tag
2. Added onError handler to log failed loads
3. Added onLoad handler to log successful loads
4. Added logging to fetchPost() function
5. Added background color to image container

---

## Summary

✅ **Debugging Added**
- Console logs for image path
- Error handling for failed loads
- Network debugging info

✅ **How to Debug**
1. Check DevTools Console for logs
2. Check DevTools Network tab for requests
3. Check backend logs for API responses
4. Check backend/uploads/ for files
5. Test image URL directly

✅ **Common Causes**
- Image file doesn't exist
- Image path is incorrect
- Backend not serving uploads
- Next.js rewrites not configured
- CORS issue

---

## Next Steps

1. **Restart Backend**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **Restart Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Image Upload**
   - Go to dashboard
   - Create post with image
   - Check backend/uploads/ for file

4. **Test Image Display**
   - Go to home page
   - Click on post
   - Check DevTools Console for logs
   - Check DevTools Network tab for image request

5. **Debug if Not Working**
   - Follow debugging steps above
   - Check all configuration files
   - Check file permissions
   - Check backend logs

---

**Image display debugging is now complete!** ✅
