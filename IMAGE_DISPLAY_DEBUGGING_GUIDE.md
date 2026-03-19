# Image Display Debugging Guide

## Issue
Images are not displaying on the post detail page (`/posts/[id]`), but they work on the home page.

## Debugging Steps

### Step 1: Check Browser Console
1. Open the post detail page
2. Open DevTools (F12 or Right-click → Inspect)
3. Go to the **Console** tab
4. Look for these logs:
   - `Post data received: { ... }` - Shows the full post object
   - `Image path: /uploads/...` - Shows the image path from the backend
   - `Image exists: true/false` - Whether the image field exists
   - `Image type: string` - Should be "string"
   - `Testing image URL: /uploads/...` - The URL being tested
   - `Image URL is valid and accessible` - If this appears, the URL works
   - `Image URL is NOT accessible: /uploads/...` - If this appears, the URL is broken

### Step 2: Check Network Tab
1. In DevTools, go to the **Network** tab
2. Reload the page
3. Look for requests to `/uploads/...` or `/api/posts/...`
4. Check the status codes:
   - **200** = Success (image loaded)
   - **404** = File not found
   - **500** = Server error
   - **CORS error** = Cross-origin issue

### Step 3: Verify Backend is Running
1. Check if the backend is running on `http://localhost:8000`
2. Try accessing `http://localhost:8000/health` in your browser
3. Should see: `{"status":"ok"}`

### Step 4: Verify Uploads Directory
1. Check if `backend/uploads/` directory exists
2. Check if image files are in the directory:
   ```bash
   ls -la backend/uploads/
   ```
3. Should see files like:
   - `4b864d1f-d61c-4117-824c-1897e8543e43.jpg`
   - `4d9f36d2-dd9c-4987-ae11-0040860200d9.jpg`
   - etc.

### Step 5: Test Direct Image Access
1. In your browser, try accessing an image directly:
   - `http://localhost:8000/uploads/4b864d1f-d61c-4117-824c-1897e8543e43.jpg`
   - Should display the image
2. If it doesn't work, the backend isn't serving uploads correctly

### Step 6: Check Database
1. The image path should be stored in MongoDB as `uploads/filename.jpg`
2. The frontend receives it as `/uploads/filename.jpg` (with leading slash added)
3. The Next.js rewrite converts `/uploads/*` to `http://localhost:8000/uploads/*`

## Common Issues & Solutions

### Issue: Image path is null/undefined
**Solution**: The post doesn't have an image. Check if the image was uploaded when creating the post.

### Issue: 404 error in Network tab
**Solution**: 
- The image file doesn't exist in `backend/uploads/`
- The image path in the database is incorrect
- The backend isn't serving the uploads directory

### Issue: CORS error
**Solution**: 
- Check `backend/app/main.py` - CORS middleware should allow `http://localhost:3000`
- Verify `allow_credentials=True` is set

### Issue: Image loads on home page but not on detail page
**Solution**: 
- The image path format might be different
- Check the console logs to compare the paths
- The detail page might have a different image height/width issue

## Quick Test

Create a test post with an image:
1. Go to Dashboard
2. Create a new post with an image
3. Check the console logs to see the image path
4. Verify the file exists in `backend/uploads/`
5. Try accessing the image directly in the browser

## If Still Not Working

1. **Restart the backend**: Stop and restart the FastAPI server
2. **Clear browser cache**: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
3. **Check file permissions**: Ensure `backend/uploads/` is readable
4. **Check Next.js rewrites**: Verify `frontend/next.config.ts` has the correct rewrites
5. **Check middleware**: Verify `/uploads/*` is not blocked by auth middleware

## Files to Check

- `backend/app/main.py` - Uploads mount and CORS
- `backend/app/api/posts.py` - Image path formatting
- `frontend/next.config.ts` - Rewrites configuration
- `frontend/src/app/posts/[id]/page.tsx` - Image display
- `backend/app/core/middleware.py` - Auth middleware (should allow `/uploads/*`)
